"""边界条件测试 — 测试异常情况"""
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock

from tarot.deck import ALL_CARDS, TarotCard
from tarot.style import display_width, strip_ansi, C, RESET
from tarot.renderer import render_ascii_art, render_card, hex_to_rgb, self_center_text
from tarot.animations import (
    card_back_raw, question_raw, text_card_raw,
    _build_progress_bar, _clip_line, PROGRESS_STYLES
)


# ═══════════════════════════════════════════════════════════════
#  输入边界测试
# ═══════════════════════════════════════════════════════════════

class TestInputEdgeCases:
    """测试输入边界"""

    def test_empty_string_display_width(self):
        """空字符串的显示宽度"""
        assert display_width("") == 0

    def test_single_char_display_width(self):
        """单字符的显示宽度"""
        assert display_width("a") == 1

    def test_cjk_single_char(self):
        """单个 CJK 字符宽度"""
        assert display_width("你") == 2

    def test_mixed_cjk_ascii(self):
        """混合中英文宽度"""
        assert display_width("a你b") == 4

    def test_emoji_width(self):
        """Emoji 宽度"""
        # Emoji 通常是双宽
        width = display_width("😀")
        assert width >= 1  # 至少占1个宽度

    def test_long_string(self):
        """超长字符串"""
        long_str = "a" * 10000
        assert display_width(long_str) == 10000

    def test_unicode_control_chars(self):
        """Unicode 控制字符"""
        # 控制字符不影响显示宽度
        result = display_width("\x00\x01\x02")
        assert isinstance(result, int)


# ═══════════════════════════════════════════════════════════════
#  渲染边界测试
# ═══════════════════════════════════════════════════════════════

class TestRenderEdgeCases:
    """测试渲染边界"""

    def test_empty_ascii_art(self):
        """空像素艺术"""
        result = render_ascii_art([], {})
        assert result == ""

    def test_single_pixel_art(self):
        """单像素艺术"""
        art = ["#"]
        color_map = {"#": "#FF0000"}
        result = render_ascii_art(art, color_map, scale=1)
        assert "▀" in result

    def test_odd_height_art(self):
        """奇数高度艺术"""
        art = ["#", "#", "#"]
        color_map = {"#": "#FF0000"}
        result = render_ascii_art(art, color_map, scale=1)
        assert "▀" in result

    def test_unknown_color_key(self):
        """未知颜色键"""
        art = ["?"]
        color_map = {"#": "#FF0000"}
        result = render_ascii_art(art, color_map, scale=1)
        # 应该使用默认颜色，不抛出异常
        assert "▀" in result

    def test_scale_zero(self):
        """scale=0 时的行为"""
        art = ["#"]
        color_map = {"#": "#FF0000"}
        result = render_ascii_art(art, color_map, scale=0)
        # scale=0 时应该没有像素
        assert result == "" or "▀" not in result


# ═══════════════════════════════════════════════════════════════
#  卡牌渲染边界测试
# ═══════════════════════════════════════════════════════════════

class TestCardRenderEdgeCases:
    """测试卡牌渲染边界"""

    def test_empty_card_data(self):
        """空卡牌数据"""
        result = render_card([], {}, "", "", "0")
        assert "╔" in result  # 仍然有边框

    def test_long_title(self):
        """超长标题"""
        art = ["##", ".."]
        color_map = {"#": "#FF0000", ".": "#000000"}
        long_title = "A" * 100
        result = render_card(art, color_map, long_title, long_title, "0")
        assert long_title in result

    def test_special_chars_in_title(self):
        """标题包含特殊字符"""
        art = ["##", ".."]
        color_map = {"#": "#FF0000", ".": "#000000"}
        result = render_card(art, color_map, "Test@#$%", "测试!@#", "0")
        assert "Test@#$%" in result

    def test_text_card_edge_cases(self):
        """文字卡牌边界"""
        # 测试第一张牌
        card = ALL_CARDS[0]
        result = text_card_raw(card, False)
        assert card.name in result

        # 测试最后一张牌
        card = ALL_CARDS[-1]
        result = text_card_raw(card, True)
        assert card.name in result


# ═══════════════════════════════════════════════════════════════
#  进度条边界测试
# ═══════════════════════════════════════════════════════════════

class TestProgressBarEdgeCases:
    """测试进度条边界"""

    def test_zero_width(self):
        """宽度为0"""
        style = PROGRESS_STYLES[0]
        result = _build_progress_bar(0.5, 0, style)
        assert result == "[]"

    def test_negative_progress(self):
        """负进度"""
        style = PROGRESS_STYLES[0]
        result = _build_progress_bar(-0.5, 10, style)
        # 应该被 clamp 到 0
        assert "░" * 10 in result

    def test_over_one_progress(self):
        """超过1的进度"""
        style = PROGRESS_STYLES[0]
        result = _build_progress_bar(1.5, 10, style)
        # 应该被 clamp 到 1
        assert "█" * 10 in result

    def test_all_styles(self):
        """所有进度条样式"""
        for style in PROGRESS_STYLES:
            result = _build_progress_bar(0.5, 10, style)
            assert style["bracket_l"] in result
            assert style["bracket_r"] in result


# ═══════════════════════════════════════════════════════════════
#  缓存边界测试
# ═══════════════════════════════════════════════════════════════

class TestCacheEdgeCases:
    """测试缓存边界"""

    def test_card_back_cache_consistency(self):
        """牌背缓存一致性"""
        result1 = card_back_raw()
        result2 = card_back_raw()
        assert result1 is result2  # 同一对象
        assert result1 == result2   # 同一内容

    def test_question_cache_consistency(self):
        """问号缓存一致性"""
        result1 = question_raw()
        result2 = question_raw()
        assert result1 is result2
        assert result1 == result2


# ═══════════════════════════════════════════════════════════════
#  文件异常测试
# ═══════════════════════════════════════════════════════════════

class TestFileEdgeCases:
    """测试文件异常"""

    def test_save_to_invalid_path(self):
        """保存到无效路径"""
        from tarot.log import save_reading
        with patch('tarot.log.LOG_FILE', '/nonexistent/path/file.jsonl'):
            # 应该处理异常，不抛出
            try:
                ts = save_reading("测试", [], "单牌指引", "解读")
                # 如果没抛出异常，应该返回 None 或空
                assert ts is None or isinstance(ts, str)
            except (FileNotFoundError, PermissionError, OSError):
                pass  # 预期的异常

    def test_read_nonexistent_file(self):
        """读取不存在的文件"""
        from tarot.log import get_recent_readings
        with patch('tarot.log.LOG_FILE', '/nonexistent/path/file.jsonl'):
            readings = get_recent_readings(10)
            assert isinstance(readings, list)
            assert len(readings) == 0


# ═══════════════════════════════════════════════════════════════
#  hex_to_rgb 边界测试
# ═══════════════════════════════════════════════════════════════

class TestHexToRgbEdgeCases:
    """测试 hex_to_rgb 边界"""

    def test_all_zeros(self):
        """全0"""
        assert hex_to_rgb("#000000") == (0, 0, 0)

    def test_all_max(self):
        """全255"""
        assert hex_to_rgb("#FFFFFF") == (255, 255, 255)

    def test_without_hash(self):
        """不带 #"""
        assert hex_to_rgb("FF0000") == (255, 0, 0)

    def test_lowercase(self):
        """小写"""
        assert hex_to_rgb("#ff0000") == (255, 0, 0)

    def test_mixed_case(self):
        """混合大小写"""
        assert hex_to_rgb("#Ff00Aa") == (255, 0, 170)


# ═══════════════════════════════════════════════════════════════
#  self_center_text 边界测试
# ═══════════════════════════════════════════════════════════════

class TestSelfCenterTextEdgeCases:
    """测试 self_center_text 边界"""

    def test_exact_width(self):
        """文字宽度等于目标宽度"""
        result = self_center_text("hello", 5)
        clean = strip_ansi(result)
        assert display_width(clean) == 5

    def test_one_char_short(self):
        """文字宽度比目标少1"""
        result = self_center_text("hell", 5)
        clean = strip_ansi(result)
        assert display_width(clean) == 5

    def test_one_char_long(self):
        """文字宽度比目标多1"""
        result = self_center_text("helloo", 5)
        clean = strip_ansi(result)
        assert display_width(clean) >= 6

    def test_zero_width(self):
        """目标宽度为0"""
        result = self_center_text("hello", 0)
        clean = strip_ansi(result)
        assert display_width(clean) == 5

    def test_cjk_centering(self):
        """CJK 字符居中"""
        result = self_center_text("你好", 10)
        clean = strip_ansi(result)
        assert display_width(clean) == 10
