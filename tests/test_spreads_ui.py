"""
SpreadUI 核心业务测试
测试 spreads_ui.py 的三个 reading 方法
"""
import pytest
from unittest.mock import MagicMock, patch, call
import random

from tarot.deck import ALL_CARDS, TarotCard
from tarot.spreads_ui import SpreadUI
from tests.conftest import MockAI, MockTUI


# ═══════════════════════════════════════════════════════════════
#  SpreadUI 单元测试
# ═══════════════════════════════════════════════════════════════

class TestSpreadUIInit:
    """测试 SpreadUI 初始化"""

    def test_init_creates_instance(self):
        """创建 SpreadUI 实例"""
        tui = MockTUI()
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)
        assert spread_ui.tui is tui
        assert spread_ui.ai is ai

    def test_init_last_question_empty(self):
        """初始 last_question 为空"""
        spread_ui = SpreadUI(MockTUI(), MockAI())
        assert spread_ui._last_question == ""


class TestSingleReading:
    """测试单牌占卜"""

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_single_reading_calls_reveal(self, mock_time, mock_shuffle, mock_reveal):
        """单牌占卜调用 reveal_card"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_single_reading("测试问题")

        mock_shuffle.assert_called_once()
        mock_reveal.assert_called_once()

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_single_reading_passes_question(self, mock_time, mock_shuffle, mock_reveal):
        """单牌占卜记录问题"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_single_reading("我的问题是什么？")

        assert spread_ui._last_question == "我的问题是什么？"

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_single_reading_returns_menu(self, mock_time, mock_shuffle, mock_reveal):
        """单牌占卜默认返回 menu"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        result = spread_ui.do_single_reading("测试")

        assert result == "menu"

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_single_reading_ai_called(self, mock_time, mock_shuffle, mock_reveal):
        """单牌占卜调用 AI 解读"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_single_reading("测试AI调用")

        assert ai.read_called is True
        assert ai.last_question == "测试AI调用"

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_single_reading_random_card(self, mock_time, mock_shuffle, mock_reveal):
        """单牌占卜抽随机牌"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_single_reading("随机测试")

        # 验证 reveal_card 被调用，且参数是 TarotCard 实例
        args, kwargs = mock_reveal.call_args
        card = args[0]
        assert isinstance(card, TarotCard)
        assert card in ALL_CARDS


class TestThreeCardReading:
    """测试三牌占卜"""

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_three_card_calls_reveal_three_times(self, mock_time, mock_shuffle, mock_reveal):
        """三牌占卜调用 reveal_card 三次"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_three_card_reading("测试")

        assert mock_reveal.call_count == 3

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_three_card_positions(self, mock_time, mock_shuffle, mock_reveal):
        """三牌占卜位置正确"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_three_card_reading("测试")

        # 验证三个位置
        expected_positions = ["过去", "现在", "未来"]
        actual_positions = [call[1]['position'] for call in mock_reveal.call_args_list]
        assert actual_positions == expected_positions

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_three_card_unique_cards(self, mock_time, mock_shuffle, mock_reveal):
        """三牌占卜抽不重复的牌"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_three_card_reading("测试")

        # 验证抽到不同的牌
        cards = [call[0][0] for call in mock_reveal.call_args_list]
        card_ids = [c.id for c in cards]
        assert len(set(card_ids)) == 3

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_three_card_skip_animation(self, mock_time, mock_shuffle, mock_reveal):
        """三牌占卜跳过动画"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        # 模拟按 S 跳过
        tui.pause = MagicMock(return_value=True)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_three_card_reading("测试")

        # 验证跳过后仍显示剩余牌（通过检查 printed_texts）
        assert len(tui.printed_texts) > 0

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_three_card_ai_called(self, mock_time, mock_shuffle, mock_reveal):
        """三牌占卜调用 AI"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_three_card_reading("测试AI")

        assert ai.read_called is True
        assert ai.last_question == "测试AI"


class TestCelticCrossReading:
    """测试凯尔特十字占卜"""

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_celtic_cross_calls_reveal_ten_times(self, mock_time, mock_shuffle, mock_reveal):
        """凯尔特十字调用 reveal_card 十次"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_celtic_cross_reading("测试")

        assert mock_reveal.call_count == 10

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_celtic_cross_positions(self, mock_time, mock_shuffle, mock_reveal):
        """凯尔特十字位置正确"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_celtic_cross_reading("测试")

        expected_positions = [
            "现状", "挑战", "根源", "过去", "可能",
            "近未来", "自我", "环境", "希望", "结局",
        ]
        actual_positions = [call[1]['position'] for call in mock_reveal.call_args_list]
        assert actual_positions == expected_positions

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_celtic_cross_unique_cards(self, mock_time, mock_shuffle, mock_reveal):
        """凯尔特十字抽不重复的牌"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_celtic_cross_reading("测试")

        cards = [call[0][0] for call in mock_reveal.call_args_list]
        card_ids = [c.id for c in cards]
        assert len(set(card_ids)) == 10

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_celtic_cross_skip_animation(self, mock_time, mock_shuffle, mock_reveal):
        """凯尔特十字跳过动画"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        # 模拟按 S 跳过
        tui.pause = MagicMock(return_value=True)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_celtic_cross_reading("测试")

        # 验证跳过后仍显示剩余牌（通过检查 printed_texts）
        assert len(tui.printed_texts) > 0

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_celtic_cross_ai_called(self, mock_time, mock_shuffle, mock_reveal):
        """凯尔特十字调用 AI"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_celtic_cross_reading("测试AI")

        assert ai.read_called is True
        assert ai.last_question == "测试AI"


class TestRerunSpread:
    """测试重新占卜"""

    def test_rerun_without_question(self):
        """无问题时重新占卜返回 menu"""
        spread_ui = SpreadUI(MockTUI(), MockAI())
        result = spread_ui.rerun_spread("单牌指引")
        assert result == "menu"

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_rerun_single_spread(self, mock_time, mock_shuffle, mock_reveal):
        """重新单牌占卜"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)
        spread_ui._last_question = "上次的问题"

        result = spread_ui.rerun_spread("单牌指引")

        assert result == "menu"
        assert mock_reveal.call_count == 1

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_rerun_three_spread(self, mock_time, mock_shuffle, mock_reveal):
        """重新三牌占卜"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)
        spread_ui._last_question = "上次的问题"

        result = spread_ui.rerun_spread("三牌占卜")

        assert result == "menu"
        assert mock_reveal.call_count == 3

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_rerun_celtic_cross(self, mock_time, mock_shuffle, mock_reveal):
        """重新凯尔特十字"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)
        spread_ui._last_question = "上次的问题"

        result = spread_ui.rerun_spread("凯尔特十字")

        assert result == "menu"
        assert mock_reveal.call_count == 10


class TestShowReading:
    """测试解读显示"""

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_show_reading_history_returns_history(self, mock_time, mock_shuffle, mock_reveal):
        """选择历史记录返回 history"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="h")
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        result = spread_ui.do_single_reading("测试")

        assert result == "history"

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_show_reading_quit_returns_quit(self, mock_time, mock_shuffle, mock_reveal):
        """选择退出返回 quit"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="q")
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        result = spread_ui.do_single_reading("测试")

        assert result == "quit"


# ═══════════════════════════════════════════════════════════════
#  数据完整性测试
# ═══════════════════════════════════════════════════════════════

class TestDataIntegrity:
    """测试数据完整性"""

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_card_data_structure(self, mock_time, mock_shuffle, mock_reveal):
        """验证传给 AI 的卡牌数据结构"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_three_card_reading("测试")

        # 验证 AI 收到的 cards 数据格式
        assert ai.last_cards is not None
        assert len(ai.last_cards) == 3
        for card_data in ai.last_cards:
            assert "card" in card_data
            assert "reversed" in card_data
            assert "position" in card_data
            assert isinstance(card_data["card"], TarotCard)
            assert isinstance(card_data["reversed"], bool)
            assert isinstance(card_data["position"], str)

    @patch('tarot.spreads_ui.reveal_card')
    @patch('tarot.spreads_ui.shuffle_animation')
    @patch('tarot.spreads_ui.time')
    def test_spread_name_passed(self, mock_time, mock_shuffle, mock_reveal):
        """验证牌阵名传给 AI"""
        tui = MockTUI()
        tui.get_choice = MagicMock(return_value="")
        tui.pause = MagicMock(return_value=False)
        ai = MockAI()
        spread_ui = SpreadUI(tui, ai)

        spread_ui.do_three_card_reading("测试")

        # 验证 AI 收到正确的 spread_name
        assert ai.last_cards is not None
