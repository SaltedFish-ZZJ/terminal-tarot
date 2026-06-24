"""style.py 测试 — 颜色工具和 display_width"""
from tarot.style import rgb, bg_rgb, display_width, C, RESET


def test_rgb():
    assert rgb(255, 0, 0) == "\033[38;2;255;0;0m"


def test_bg_rgb():
    assert bg_rgb(0, 0, 0) == "\033[48;2;0;0;0m"


def test_display_width_ascii():
    assert display_width("hello") == 5


def test_display_width_cjk():
    assert display_width("你好") == 4


def test_display_width_mixed():
    assert display_width("hi你好") == 6


def test_display_width_empty():
    assert display_width("") == 0


def test_color_class():
    assert C.BG == (10, 17, 29)
    assert C.GOLD == (218, 183, 114)
    assert isinstance(C.s(C.GOLD), str)
    assert isinstance(C.bg(C.BG), str)


def test_reset():
    assert RESET == "\033[0m"
