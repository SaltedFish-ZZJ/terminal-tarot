"""
Terminal utility functions - 工具函数
"""
import shutil
import unicodedata

from tarot.colors import (
    _ANSI_RE,
    S_ACCENT,
    S_BRIGHT,
    S_DIM,
    S_REVERSED,
    S_UPRIGHT,
)

# ═══════════════════════════════════════════════════════════════
#  显示宽度计算
# ═══════════════════════════════════════════════════════════════

def display_width(s: str) -> int:
    """计算终端显示宽度，CJK/emoji 算 2 列。"""
    w = 0
    for ch in s:
        eaw = unicodedata.east_asian_width(ch)
        w += 2 if eaw in ('W', 'F') else 1
    return w


def strip_ansi(s: str) -> str:
    """去除 ANSI 转义序列，返回纯文本。"""
    return _ANSI_RE.sub('', s)


# ═══════════════════════════════════════════════════════════════
#  终端尺寸
# ═══════════════════════════════════════════════════════════════

def term_width() -> int:
    """终端列数。"""
    return shutil.get_terminal_size().columns


def term_height() -> int:
    """终端行数。"""
    return shutil.get_terminal_size().lines


# ═══════════════════════════════════════════════════════════════
#  文本处理
# ═══════════════════════════════════════════════════════════════

def center_line(text: str, width: int) -> str:
    """将文本居中到指定宽度（考虑 CJK 显示宽度）。"""
    dw = display_width(strip_ansi(text))
    pad = max(0, (width - dw) // 2)
    return ' ' * pad + text


def vpad(content_lines: int) -> str:
    """返回垂直居中所需的顶部空行字符串。"""
    n = max(0, (term_height() - content_lines) // 2)
    return "\n" * n


# ═══════════════════════════════════════════════════════════════
#  卡片格式化
# ═══════════════════════════════════════════════════════════════

def format_card_line(position: str, name_cn: str, is_reversed: bool,
                     keywords: list[str] | None = None, kw_limit: int = 40):
    """统一的卡片信息行格式化（消除多处重复）。"""
    from rich.text import Text
    orient = "逆位" if is_reversed else "正位"
    orient_c = S_REVERSED if is_reversed else S_UPRIGHT
    t = Text()
    t.append(f"  【{position}】", style=S_ACCENT)
    t.append(name_cn, style=S_BRIGHT)
    t.append(f" · {orient}", style=orient_c)
    if keywords:
        t.append(f"  {'  '.join(keywords)[:kw_limit]}", style=S_DIM)
    return t


__all__ = [
    # 显示宽度
    "display_width", "strip_ansi",
    # 终端尺寸
    "term_width", "term_height",
    # 文本处理
    "center_line", "vpad",
    # 卡片格式化
    "format_card_line",
]
