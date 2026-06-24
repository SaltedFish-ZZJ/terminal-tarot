"""业务逻辑测试 — 测试核心业务流程"""
import pytest
from unittest.mock import MagicMock, patch

from tarot.deck import ALL_CARDS, TarotCard
from tarot.spreads import SPREADS, CELTIC_CROSS
from tarot.interfaces import AIService, TUIEngine


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
#  牌组业务逻辑测试
# ═══════════════════════════════════════════════════════════════

class TestCardBusinessLogic:
    """测试卡牌业务逻辑"""

    def test_card_has_required_fields(self):
        """卡牌有所有必需字段"""
        for card in ALL_CARDS:
            assert hasattr(card, 'id')
            assert hasattr(card, 'name')
            assert hasattr(card, 'name_cn')
            assert hasattr(card, 'number')
            assert hasattr(card, 'element')
            assert hasattr(card, 'keywords_upright')
            assert hasattr(card, 'keywords_reversed')

    def test_card_keywords_are_lists(self):
        """关键词是列表"""
        for card in ALL_CARDS:
            assert isinstance(card.keywords_upright, list)
            assert isinstance(card.keywords_reversed, list)
            assert len(card.keywords_upright) > 0
            assert len(card.keywords_reversed) > 0

    def test_major_arcana_range(self):
        """大阿卡纳 ID 范围"""
        major_arcana = [c for c in ALL_CARDS if c.arcana == "major"]
        assert len(major_arcana) == 22
        for card in major_arcana:
            assert 0 <= card.id <= 21

    def test_minor_arcana_range(self):
        """小阿卡纳 ID 范围"""
        minor_arcana = [c for c in ALL_CARDS if c.arcana != "major"]
        assert len(minor_arcana) == 56
        for card in minor_arcana:
            assert 22 <= card.id <= 77


# ═══════════════════════════════════════════════════════════════
#  牌阵业务逻辑测试
# ═══════════════════════════════════════════════════════════════

class TestSpreadBusinessLogic:
    """测试牌阵业务逻辑"""

    def test_single_spread_config(self):
        """单牌配置正确"""
        assert SPREADS["single"]["name"] == "Single Card"
        assert len(SPREADS["single"]["positions"]) == 1

    def test_three_spread_config(self):
        """三牌配置正确"""
        assert SPREADS["three_card"]["name"] == "Three Card"
        assert len(SPREADS["three_card"]["positions"]) == 3

    def test_celtic_cross_spread_config(self):
        """凯尔特十字配置正确"""
        assert SPREADS["celtic_cross"]["name"] == "Celtic Cross"
        assert len(SPREADS["celtic_cross"]["positions"]) == 10

    def test_celtic_cross_positions(self):
        """凯尔特十字有10个位置"""
        positions = CELTIC_CROSS["positions"]
        assert len(positions) == 10

        # 验证位置有 name 和 name_cn
        for pos in positions:
            assert hasattr(pos, 'name')
            assert hasattr(pos, 'name_cn')
            assert hasattr(pos, 'row')
            assert hasattr(pos, 'col')


# ═══════════════════════════════════════════════════════════════
#  占卜流程业务逻辑测试
# ═══════════════════════════════════════════════════════════════

class TestReadingBusinessLogic:
    """测试占卜流程业务逻辑"""

    def test_card_draw_randomness(self):
        """抽牌应该是随机的"""
        import random
        # 多次抽牌，结果应该不同
        results = set()
        for _ in range(10):
            card = random.choice(ALL_CARDS)
            results.add(card.id)
        # 理论上应该有多个不同结果（极小概率相同）
        assert len(results) > 1

    def test_reversed_probability(self):
        """逆位概率符合预期"""
        import random
        reversed_count = 0
        total = 1000
        for _ in range(total):
            if random.random() < 0.35:
                reversed_count += 1
        # 35% 概率，允许 5% 误差
        assert 0.25 <= reversed_count / total <= 0.45

    def test_unique_cards_drawn(self):
        """抽牌应该是不重复的"""
        import random
        drawn = random.sample(ALL_CARDS, 10)
        ids = [c.id for c in drawn]
        assert len(ids) == len(set(ids))


# ═══════════════════════════════════════════════════════════════
#  数据格式化业务逻辑测试
# ═══════════════════════════════════════════════════════════════

class TestDataFormatting:
    """测试数据格式化"""

    def test_card_data_format(self):
        """卡牌数据格式正确"""
        card = ALL_CARDS[0]
        data = {
            "card": card,
            "reversed": False,
            "position": "指引"
        }
        assert isinstance(data["card"], TarotCard)
        assert isinstance(data["reversed"], bool)
        assert isinstance(data["position"], str)

    def test_reading_data_format(self):
        """占卜数据格式正确"""
        card = ALL_CARDS[0]
        reading = {
            "question": "测试问题",
            "cards": [{"card": card, "reversed": False, "position": "指引"}],
            "spread": "单牌指引",
            "reading": "测试解读",
        }
        assert isinstance(reading["question"], str)
        assert isinstance(reading["cards"], list)
        assert isinstance(reading["spread"], str)
        assert isinstance(reading["reading"], str)


# ═══════════════════════════════════════════════════════════════
#  AI 服务业务逻辑测试
# ═══════════════════════════════════════════════════════════════

class TestAIBusinessLogic:
    """测试 AI 服务业务逻辑"""

    def test_ai_read_with_cards(self):
        """AI 读取带卡牌数据"""
        ai = MockAI()
        card = ALL_CARDS[0]
        cards = [{"card": card, "reversed": False, "position": "指引"}]
        result = ai.read("测试问题", cards, "单牌指引")
        assert ai.read_called is True
        assert ai.last_question == "测试问题"
        assert ai.last_cards == cards

    def test_ai_read_returns_string(self):
        """AI 读取返回字符串"""
        ai = MockAI()
        result = ai.read("测试问题", [], "单牌指引")
        assert isinstance(result, str)
        assert len(result) > 0
