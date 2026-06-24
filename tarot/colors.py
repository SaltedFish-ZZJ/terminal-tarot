"""
Terminal color definitions - 暗色+金色美学
"""
import re

# ═══════════════════════════════════════════════════════════════
#  ANSI 基础函数
# ═══════════════════════════════════════════════════════════════

def rgb(r: int, g: int, b: int) -> str:
    """Convert RGB to ANSI foreground escape sequence."""
    return f"\033[38;2;{r};{g};{b}m"


def bg_rgb(r: int, g: int, b: int) -> str:
    """Convert RGB to ANSI background escape sequence."""
    return f"\033[48;2;{r};{g};{b}m"


# ═══════════════════════════════════════════════════════════════
#  ANSI 常量
# ═══════════════════════════════════════════════════════════════

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
CLEAR = "\033[2J\033[H"  # Clear screen + move cursor to top-left


# ═══════════════════════════════════════════════════════════════
#  Color palette
# ═══════════════════════════════════════════════════════════════

class C:
    """Theme colors as (r, g, b) tuples and ANSI strings."""
    # Backgrounds
    BG           = (10, 17, 29)        # #0a111d  深空背景
    BG_CARD      = (13, 13, 13)        # #0d0d0d  牌面背景
    BG_PANEL     = (15, 20, 32)        # #0f1420  面板背景

    # Gold system
    GOLD         = (218, 183, 114)     # #dab772  主金色
    GOLD_LIGHT   = (255, 220, 120)     # #ffdc78  亮金
    GOLD_DARK    = (165, 128, 64)      # #a58040  暗金
    GOLD_DIM     = (100, 80, 40)       # #645028  暗淡金

    # Text
    TEXT         = (240, 224, 176)     # #f0e0b0  主文字（米白）
    TEXT_DIM     = (80, 100, 104)      # #506468  暗色文字
    TEXT_BRIGHT  = (255, 240, 200)     # #fff0c8  亮文字

    # Semantic
    UPRIGHT      = (78, 205, 196)      # #4ecdc4  正位（青色）
    REVERSED     = (255, 107, 107)     # #ff6b6b  逆位（红色）
    ACCENT       = (232, 196, 124)     # #e8c47c  强调色
    BORDER       = (42, 42, 58)        # #2a2a3a  分割线
    GLOW         = (255, 220, 120)     # #ffdc78  发光效果
    SKIN         = (240, 208, 160)     # #f0d0a0  皮肤色
    RED          = (139, 37, 0)        # #8b2500  深红
    WHITE        = (255, 255, 255)     # 纯白

    # ── ANSI string shortcuts ──
    @staticmethod
    def s(color_tuple):
        """Convert (r,g,b) to ANSI fg escape."""
        return rgb(*color_tuple)

    @staticmethod
    def bg(color_tuple):
        """Convert (r,g,b) to ANSI bg escape."""
        return bg_rgb(*color_tuple)

    @staticmethod
    def fg_bg(fg_tuple, bg_tuple):
        """Combined fg + bg escape."""
        return rgb(*fg_tuple) + bg_rgb(*bg_tuple)

    @staticmethod
    def rich(color_tuple) -> str:
        """Convert (r,g,b) to Rich markup style string 'rgb(r,g,b)'."""
        return f"rgb({color_tuple[0]},{color_tuple[1]},{color_tuple[2]})"


# ── Rich style constants (single source) ─────────────────────
# Used by app.py, tui.py, animations.py — import from here only.
S_GOLD = C.rich(C.GOLD)
S_ACCENT = C.rich(C.ACCENT)
S_DIM = C.rich(C.TEXT_DIM)
S_BRIGHT = C.rich(C.TEXT_BRIGHT)
S_BORDER = C.rich(C.BORDER)
S_UPRIGHT = C.rich(C.UPRIGHT)
S_REVERSED = C.rich(C.REVERSED)


# ── Card back pattern colors ──
CARD_BACK_FG = C.GOLD_DARK
CARD_BACK_BG = C.BG_CARD


# ── Regex patterns ──
_ANSI_RE = re.compile(r'\033\[[0-9;]*m')
_ANSI_SPLIT_RE = re.compile(r'(\033\[[0-9;]*m)')  # 带捕获组，用于分割

__all__ = [
    # 函数
    "rgb", "bg_rgb",
    # 常量
    "RESET", "BOLD", "DIM", "ITALIC", "UNDERLINE", "CLEAR",
    # 颜色类
    "C",
    # Rich 样式常量
    "S_GOLD", "S_ACCENT", "S_DIM", "S_BRIGHT", "S_BORDER", "S_UPRIGHT", "S_REVERSED",
    # 卡片背面颜色
    "CARD_BACK_FG", "CARD_BACK_BG",
    # 正则表达式（内部使用）
    "_ANSI_RE", "_ANSI_SPLIT_RE",
]
