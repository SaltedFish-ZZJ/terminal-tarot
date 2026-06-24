"""集成测试 — 测试模块间协作"""
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from io import StringIO

from tarot.deck import ALL_CARDS, CARD_BY_ID, ELEMENT_INFO
from tarot.interfaces import AIService, TUIEngine
from tarot.spreads import CELTIC_CROSS, SPREADS


# ═══════════════════════════════════════════════════════════════
#  Mock 对象
# ═══════════════════════════════════════════════════════════════

class MockAI(AIService):
    """Mock AI 服务"""

    def __init__(self):
        self.read_called = False
        self.last_question = None
        self.last_cards = None

    def is_configured(self) -> bool:
        return True

    def read(self, question: str, cards: list[dict], spread_name: str = "单牌指引") -> str:
        self.read_called = True
        self.last_question = question
        self.last_cards = cards
        return f"AI 解读: {question}"

    def close(self) -> None:
        pass


class MockTUI(TUIEngine):
    """Mock TUI 引擎"""

    def __init__(self):
        self.clear_called = False
        self.printed_texts = []
        self.console = MagicMock()

    def clear(self) -> None:
        self.clear_called = True

    def print(self, *args, **kwargs) -> None:
        self.printed_texts.append(args)

    def print_centered(self, text, style=None) -> None:
        self.printed_texts.append((text, style))

    def print_rule(self, color=None) -> None:
        self.printed_texts.append(("rule", color))

    def get_input(self, prompt: str = "▸ ") -> str:
        return "测试输入"

    def get_centered_input(self, prompt: str = "▸ ") -> str:
        return "测试输入"

    def get_choice(self, prompt: str = "▸ ", valid: list[str] = None) -> str:
        return ""

    def pause(self, msg: str = "按 Enter 继续...", skip_key: str = "") -> bool:
        return False


# ═══════════════════════════════════════════════════════════════
#  接口实现测试
# ═══════════════════════════════════════════════════════════════

class TestAIServiceInterface:
    """测试 AIService 接口"""

    def test_mock_ai_implements_interface(self):
        """MockAI 正确实现 AIService 接口"""
        ai = MockAI()
        assert isinstance(ai, AIService)

    def test_mock_ai_is_configured(self):
        """MockAI.is_configured 返回 True"""
        ai = MockAI()
        assert ai.is_configured() is True

    def test_mock_ai_read(self):
        """MockAI.read 被正确调用"""
        ai = MockAI()
        result = ai.read("测试问题", [], "单牌指引")
        assert ai.read_called is True
        assert "测试问题" in result

    def test_mock_ai_close(self):
        """MockAI.close 不抛出异常"""
        ai = MockAI()
        ai.close()  # 不应该抛出异常


class TestTUIEngineInterface:
    """测试 TUIEngine 接口"""

    def test_mock_tui_implements_interface(self):
        """MockTUI 正确实现 TUIEngine 接口"""
        tui = MockTUI()
        assert isinstance(tui, TUIEngine)

    def test_mock_tui_clear(self):
        """MockTUI.clear 被正确调用"""
        tui = MockTUI()
        tui.clear()
        assert tui.clear_called is True

    def test_mock_tui_print(self):
        """MockTUI.print 记录输出"""
        tui = MockTUI()
        tui.print("测试文本")
        assert len(tui.printed_texts) == 1

    def test_mock_tui_print_centered(self):
        """MockTUI.print_centered 记录输出"""
        tui = MockTUI()
        tui.print_centered("测试居中")
        assert len(tui.printed_texts) == 1

    def test_mock_tui_get_input(self):
        """MockTUI.get_input 返回输入"""
        tui = MockTUI()
        result = tui.get_input()
        assert result == "测试输入"

    def test_mock_tui_get_choice(self):
        """MockTUI.get_choice 返回选择"""
        tui = MockTUI()
        result = tui.get_choice()
        assert result == ""

    def test_mock_tui_pause(self):
        """MockTUI.pause 返回 False"""
        tui = MockTUI()
        result = tui.pause()
        assert result is False


# ═══════════════════════════════════════════════════════════════
#  牌组数据集成测试
# ═══════════════════════════════════════════════════════════════

class TestDeckIntegration:
    """测试牌组数据集成"""

    def test_card_by_id_matches_all_cards(self):
        """CARD_BY_ID 与 ALL_CARDS 一致"""
        for card in ALL_CARDS:
            assert card.id in CARD_BY_ID
            assert CARD_BY_ID[card.id] is card

    def test_element_info_complete(self):
        """ELEMENT_INFO 包含所有元素"""
        elements = {"fire", "water", "air", "earth"}
        info_elements = set(ELEMENT_INFO.keys())
        assert elements.issubset(info_elements)

    def test_card_has_element(self):
        """每张牌都有元素（大阿卡纳可能为空）"""
        valid_elements = {"fire", "water", "air", "earth", ""}
        for card in ALL_CARDS:
            assert card.element in valid_elements


# ═══════════════════════════════════════════════════════════════
#  牌阵配置集成测试
# ═══════════════════════════════════════════════════════════════

class TestSpreadsIntegration:
    """测试牌阵配置集成"""

    def test_spreads_exist(self):
        """SPREADS 包含三种牌阵"""
        assert "single" in SPREADS
        assert "three_card" in SPREADS
        assert "celtic_cross" in SPREADS

    def test_celtic_cross_has_positions(self):
        """凯尔特十字有10个位置"""
        assert len(CELTIC_CROSS["positions"]) == 10

    def test_celtic_cross_positions_have_coords(self):
        """凯尔特十字位置有 row 和 col"""
        for pos in CELTIC_CROSS["positions"]:
            assert hasattr(pos, "row")
            assert hasattr(pos, "col")


# ═══════════════════════════════════════════════════════════════
#  日志模块集成测试
# ═══════════════════════════════════════════════════════════════

class TestLogIntegration:
    """测试日志模块集成"""

    def test_save_and_read_integration(self):
        """保存和读取记录集成测试"""
        import tempfile
        import os
        from unittest.mock import patch
        from tarot.log import save_reading, get_recent_readings

        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            path = f.name

        try:
            with patch('tarot.log.LOG_FILE', path):
                # 创建 mock card
                class FakeCard:
                    name = "The Fool"
                    name_cn = "愚者"
                    id = 0

                card_data = [{"card": FakeCard(), "reversed": False, "position": "指引"}]

                # 保存记录
                ts = save_reading("集成测试问题", card_data, "单牌指引", "集成测试解读")
                assert ts

                # 读取记录
                readings = get_recent_readings(10)
                assert len(readings) >= 1
                assert readings[-1]["question"] == "集成测试问题"
                assert readings[-1]["spread"] == "单牌指引"
        finally:
            os.unlink(path)
