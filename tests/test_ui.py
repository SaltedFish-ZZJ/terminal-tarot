"""UI 测试 — 测试渲染输出"""
import pytest
from io import StringIO
from unittest.mock import patch, MagicMock

from tarot.deck import ALL_CARDS
from tarot.renderer import (
    render_ascii_art, render_card, render_three_cards_horizontal,
    hex_to_rgb, self_center_text, print_centered, clear_screen
)
from tarot.animations import (
    card_back_raw, question_raw, text_card_raw,
    _build_progress_bar, _build_shuffling_text, PROGRESS_STYLES
)
from tarot.style import C, RESET, display_width, strip_ansi, CARD_WIDTH


# ═══════════════════════════════════════════════════════════════
#  渲染器测试
# ═══════════════════════════════════════════════════════════════

class TestHexToRgb:
    """测试 hex_to_rgb 函数"""

    def test_red(self):
        assert hex_to_rgb("#FF0000") == (255, 0, 0)

    def test_green(self):
        assert hex_to_rgb("#00FF00") == (0, 255, 0)

    def test_blue(self):
        assert hex_to_rgb("#0000FF") == (0, 0, 255)

    def test_without_hash(self):
        assert hex_to_rgb("FFFFFF") == (255, 255, 255)

    def test_lowercase(self):
        assert hex_to_rgb("#ff0000") == (255, 0, 0)


class TestRenderAsciiArt:
    """测试 render_ascii_art 函数"""

    def test_empty_input(self):
        """空输入返回空字符串"""
        result = render_ascii_art([], {})
        assert result == ""

    def test_simple_art(self):
        """简单像素艺术渲染"""
        art = ["##", ".."]
        color_map = {"#": "#FF0000", ".": "#000000"}
        result = render_ascii_art(art, color_map, scale=1)
        assert "▀" in result
        assert "\033[" in result  # 包含 ANSI 转义序列

    def test_scale_2(self):
        """scale=2 时字符重复"""
        art = ["#"]
        color_map = {"#": "#FF0000"}
        result = render_ascii_art(art, color_map, scale=2)
        # 每个像素应该重复2次，但中间有 ANSI 转义序列
        # 检查输出包含 ▀ 字符
        assert "▀" in result
        # 检查输出包含两个 ▀（通过计算出现次数）
        assert result.count("▀") == 2


class TestRenderCard:
    """测试 render_card 函数"""

    def test_card_with_border(self):
        """卡牌有边框"""
        art = ["##", ".."]
        color_map = {"#": "#FF0000", ".": "#000000"}
        result = render_card(art, color_map, "THE FOOL", "愚者", "0")
        assert "╔" in result
        assert "╗" in result
        assert "╚" in result
        assert "╝" in result

    def test_card_with_title(self):
        """卡牌包含标题"""
        art = ["##", ".."]
        color_map = {"#": "#FF0000", ".": "#000000"}
        result = render_card(art, color_map, "THE FOOL", "愚者", "0")
        assert "THE FOOL" in result
        assert "愚者" in result

    def test_card_with_number(self):
        """卡牌包含编号"""
        art = ["##", ".."]
        color_map = {"#": "#FF0000", ".": "#000000"}
        result = render_card(art, color_map, "THE FOOL", "愚者", "0")
        assert "0" in result

    def test_reversed_card(self):
        """逆位卡牌显示'逆位'"""
        art = ["##", ".."]
        color_map = {"#": "#FF0000", ".": "#000000"}
        result = render_card(art, color_map, "THE FOOL", "愚者", "0", is_reversed=True)
        assert "逆位" in result

    def test_upright_card(self):
        """正位卡牌显示'正位'"""
        art = ["##", ".."]
        color_map = {"#": "#FF0000", ".": "#000000"}
        result = render_card(art, color_map, "THE FOOL", "愚者", "0", is_reversed=False)
        assert "正位" in result


class TestSelfCenterText:
    """测试 self_center_text 函数"""

    def test_center_basic(self):
        """基本居中功能"""
        result = self_center_text("hello", 20)
        clean = strip_ansi(result)
        assert display_width(clean) == 20

    def test_center_with_style(self):
        """带样式前缀的居中"""
        result = self_center_text("hello", 20, "\033[31m")
        assert "\033[31m" in result

    def test_center_longer_than_width(self):
        """文字比宽度长时直接返回"""
        result = self_center_text("hello world", 5)
        clean = strip_ansi(result)
        assert display_width(clean) >= 11


# ═══════════════════════════════════════════════════════════════
#  动画渲染测试
# ═══════════════════════════════════════════════════════════════

class TestCardBackRaw:
    """测试 card_back_raw 函数"""

    def test_returns_string(self):
        """返回字符串"""
        result = card_back_raw()
        assert isinstance(result, str)

    def test_has_border(self):
        """包含边框"""
        result = card_back_raw()
        assert "╔" in result
        assert "╗" in result
        assert "╚" in result
        assert "╝" in result

    def test_cached(self):
        """结果被缓存"""
        result1 = card_back_raw()
        result2 = card_back_raw()
        assert result1 is result2


class TestQuestionRaw:
    """测试 question_raw 函数"""

    def test_returns_string(self):
        """返回字符串"""
        result = question_raw()
        assert isinstance(result, str)

    def test_has_border(self):
        """包含边框"""
        result = question_raw()
        assert "╔" in result
        assert "╗" in result

    def test_cached(self):
        """结果被缓存"""
        result1 = question_raw()
        result2 = question_raw()
        assert result1 is result2


class TestTextCardRaw:
    """测试 text_card_raw 函数"""

    def test_returns_string(self):
        """返回字符串"""
        card = ALL_CARDS[0]
        result = text_card_raw(card, False)
        assert isinstance(result, str)

    def test_contains_card_name(self):
        """包含卡牌名称"""
        card = ALL_CARDS[0]
        result = text_card_raw(card, False)
        assert card.name in result
        assert card.name_cn in result

    def test_contains_number(self):
        """包含编号"""
        card = ALL_CARDS[0]
        result = text_card_raw(card, False)
        assert card.number in result

    def test_reversed_symbol(self):
        """逆位显示不同符号"""
        card = ALL_CARDS[0]
        upright = text_card_raw(card, False)
        reversed_card = text_card_raw(card, True)
        assert "★★★" in upright
        assert "☆☆☆" in reversed_card


# ═══════════════════════════════════════════════════════════════
#  进度条测试
# ═══════════════════════════════════════════════════════════════

class TestProgressBar:
    """测试进度条构建"""

    def test_build_progress_bar_zero(self):
        """进度为0时全空"""
        style = PROGRESS_STYLES[0]
        result = _build_progress_bar(0.0, 10, style)
        assert "░" * 10 in result
        assert "█" not in result

    def test_build_progress_bar_full(self):
        """进度为1时全满"""
        style = PROGRESS_STYLES[0]
        result = _build_progress_bar(1.0, 10, style)
        assert "█" * 10 in result

    def test_build_progress_bar_half(self):
        """进度为0.5时一半"""
        style = PROGRESS_STYLES[0]
        result = _build_progress_bar(0.5, 10, style)
        assert "█" * 5 in result
        assert "░" * 5 in result

    def test_build_shuffling_text(self):
        """洗牌文本包含符号"""
        style = PROGRESS_STYLES[0]
        result = _build_shuffling_text(0, style)
        assert "洗牌中" in result
        assert "◆" in result or "◇" in result


# ═══════════════════════════════════════════════════════════════
#  三牌并排渲染测试
# ═══════════════════════════════════════════════════════════════

class TestRenderThreeCardsHorizontal:
    """测试三牌并排渲染"""

    def test_basic_render(self):
        """基本渲染"""
        cards_data = []
        for i in range(3):
            cards_data.append({
                "ascii": ["##", ".."],
                "color_map": {"#": "#FF0000", ".": "#000000"},
                "name_en": f"CARD {i}",
                "name_cn": f"牌{i}",
                "number": str(i),
                "reversed": False,
            })
        result = render_three_cards_horizontal(cards_data, scale=1)
        assert "CARD 0" in result
        assert "CARD 1" in result
        assert "CARD 2" in result

    def test_with_reversed(self):
        """逆位卡牌"""
        cards_data = [{
            "ascii": ["##", ".."],
            "color_map": {"#": "#FF0000", ".": "#000000"},
            "name_en": "CARD",
            "name_cn": "牌",
            "number": "0",
            "reversed": True,
        }]
        result = render_three_cards_horizontal(cards_data, scale=1)
        assert "逆位" in result


# ═══════════════════════════════════════════════════════════════
#  凯尔特十字终端检测测试
# ═══════════════════════════════════════════════════════════════

class TestCelticCrossTerminalDetection:
    """测试凯尔特十字终端尺寸检测"""

    def test_returns_none_when_too_small(self):
        """终端太小时返回 None"""
        from tarot.renderer import render_celtic_cross
        from tarot.spreads import CELTIC_CROSS

        # 创建 10 张卡牌数据
        cards_data = []
        for i in range(10):
            cards_data.append({
                "ascii": ["#" * 32] * 40,
                "color_map": {"#": "#FF0000"},
                "name_en": f"CARD {i}",
                "name_cn": f"牌{i}",
                "number": str(i),
                "reversed": False,
            })

        positions = [{"row": p.row, "col": p.col} for p in CELTIC_CROSS["positions"]]

        # 模拟小终端 (80x24)
        with patch('tarot.renderer.term_width', return_value=80), \
             patch('tarot.renderer.term_height', return_value=24):
            result = render_celtic_cross(cards_data, positions, scale=1)
            assert result is None

    def test_returns_string_when_large_enough(self):
        """终端足够大时返回字符串"""
        from tarot.renderer import render_celtic_cross
        from tarot.spreads import CELTIC_CROSS

        # 创建 10 张卡牌数据
        cards_data = []
        for i in range(10):
            cards_data.append({
                "ascii": ["#" * 32] * 40,
                "color_map": {"#": "#FF0000"},
                "name_en": f"CARD {i}",
                "name_cn": f"牌{i}",
                "number": str(i),
                "reversed": False,
            })

        positions = [{"row": p.row, "col": p.col} for p in CELTIC_CROSS["positions"]]

        # 模拟大终端 (400x300) - 需要足够大以容纳网格
        with patch('tarot.renderer.term_width', return_value=400), \
             patch('tarot.renderer.term_height', return_value=300):
            result = render_celtic_cross(cards_data, positions, scale=1)
            assert isinstance(result, str)
            assert len(result) > 0
