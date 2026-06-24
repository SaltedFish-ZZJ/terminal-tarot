"""
动画效果 — 洗牌、翻牌、牌背、问号帧
v2.1 - 多种进度条洗牌动画
"""
import sys
import time
import random

from tarot.deck import TarotCard
from tarot.style import (
    C, RESET, display_width, strip_ansi, term_width, center_line,
    S_GOLD, S_ACCENT, S_DIM, S_BORDER,
    CARD_WIDTH, CARD_HEIGHT, FLIP_DURATION,
)
from tarot.renderer import render_card

# ── 模块级缓存 ──
_cached_card_back: str | None = None
_cached_question: str | None = None

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════
#  辅助函数
# ══════════════════════════════════════════════════════════════════

def _center_write(text):
    sys.stdout.write(center_line(text, term_width()) + "\n")


def _clear():
    from tarot.style import CLEAR
    sys.stdout.write(CLEAR)
    sys.stdout.flush()


def _g():
    """金色"""
    return C.s(C.GOLD)


def _a():
    """强调色"""
    return C.s(C.ACCENT)


def _d():
    """暗色"""
    return C.s(C.TEXT_DIM)


# ══════════════════════════════════════════════════════════════════
#  洗牌动画 — 多种进度条样式
# ══════════════════════════════════════════════════════════════════

# 进度条样式定义
PROGRESS_STYLES = [
    {
        "name": "classic",
        "fill": "█",
        "empty": "░",
        "bracket_l": "[",
        "bracket_r": "]",
        "symbols": ["◆", "◇", "✦", "✧", "★", "☆"],
    },
    {
        "name": "dots",
        "fill": "●",
        "empty": "○",
        "bracket_l": "【",
        "bracket_r": "】",
        "symbols": ["♠", "♥", "♦", "♣"],
    },
    {
        "name": "line",
        "fill": "━",
        "empty": "─",
        "bracket_l": "◀",
        "bracket_r": "▶",
        "symbols": ["★", "☆", "✧", "✦"],
    },
    {
        "name": "diamond",
        "fill": "◆",
        "empty": "◇",
        "bracket_l": "(",
        "bracket_r": ")",
        "symbols": ["✦", "★", "◈", "◉"],
    },
    {
        "name": "block",
        "fill": "▓",
        "empty": "░",
        "bracket_l": "「",
        "bracket_r": "」",
        "symbols": ["★", "☆", "◆", "◇"],
    },
]


def _build_progress_bar(progress: float, width: int, style: dict) -> str:
    """构建进度条字符串"""
    filled = int(progress * width)
    empty = width - filled

    bar = style["fill"] * filled + style["empty"] * empty
    return f"{style['bracket_l']}{bar}{style['bracket_r']}"


def _build_shuffling_text(frame: int, style: dict) -> str:
    """构建洗牌中的动态文本"""
    symbols = style["symbols"]
    # 旋转符号
    idx = frame % len(symbols)
    left = symbols[idx]
    right = symbols[(idx + 2) % len(symbols)]
    return f"{left} 洗牌中 {right}"


def shuffle_animation(console):
    """洗牌动画 — 随机选择一种进度条样式，完全居中显示"""
    from tarot.style import vpad

    g = _g()
    a = _a()
    d = _d()

    # 随机选择样式
    style = random.choice(PROGRESS_STYLES)

    # 动画参数
    total_frames = 30
    bar_width = 25
    # 动画区域总行数（标题 + 空行 + 进度条 + 空行 + 符号）
    total_lines = 7

    for frame in range(total_frames):
        _clear()

        progress = (frame + 1) / total_frames
        pct = int(progress * 100)

        # 构建元素
        progress_bar = _build_progress_bar(progress, bar_width, style)
        shuffling_text = _build_shuffling_text(frame, style)

        # 垂直居中
        sys.stdout.write(vpad(total_lines))

        # 水平居中输出
        _center_write(f"{g}  ✦ {shuffling_text} ✦  {RESET}")
        sys.stdout.write("\n")
        _center_write(f"{a}{progress_bar}{RESET} {d}{pct}%{RESET}")
        sys.stdout.write("\n")

        # 随机显示一些卡牌符号
        if frame > 5:
            symbols = style["symbols"]
            num_show = min(frame - 5, 8)
            scatter = "  ".join(random.sample(symbols, min(num_show, len(symbols))))
            _center_write(f"{d}{scatter}{RESET}")
        else:
            sys.stdout.write("\n")

        sys.stdout.flush()
        time.sleep(0.08)

    # 完成闪烁
    for _ in range(3):
        _clear()
        sys.stdout.write(vpad(3))
        _center_write(f"{g}  ✦ 洗牌完成 ✦  {RESET}")
        sys.stdout.write("\n\n")
        sys.stdout.flush()
        time.sleep(0.12)

        _clear()
        sys.stdout.write(vpad(3))
        _center_write(f"{a}  ✦ 洗牌完成 ✦  {RESET}")
        sys.stdout.write("\n\n")
        sys.stdout.flush()
        time.sleep(0.12)


# ══════════════════════════════════════════════════════════════════
#  翻牌动画
# ══════════════════════════════════════════════════════════════════


def _render_frame(frame_lines, position=""):
    _clear()
    if position:
        _center_write(f"{C.s(C.ACCENT)}【{position}】{RESET}")
        sys.stdout.write("\n")
    for line in frame_lines:
        _center_write(line)
    sys.stdout.flush()


def _get_card_lines(card: TarotCard, is_reversed: bool) -> list[str]:
    """获取卡牌渲染行（像素艺术或纯文字 fallback）。"""
    from tarot.cards import CARD_ART

    if card.id in CARD_ART:
        art_data = CARD_ART[card.id]
        card_str = render_card(
            art_data["ascii"], art_data["color_map"],
            card.name, card.name_cn, card.number,
            is_reversed=is_reversed, scale=1,
        )
        return card_str.split('\n')
    return text_card_raw(card, is_reversed).split('\n')


def _clip_line(line: str, show_w: int, card_w: int = CARD_WIDTH) -> str:
    """裁剪 ANSI 行到指定可见宽度，居中显示。"""
    result = []
    vis = 0
    in_ansi = False
    for ch in line:
        if ch == '\033':
            in_ansi = True
            result.append(ch)
        elif in_ansi:
            result.append(ch)
            if ch == 'm':
                in_ansi = False
        else:
            if vis < show_w:
                result.append(ch)
                vis += 1
    pad = max(0, (card_w - show_w) // 2)
    return " " * pad + "".join(result)


def _flip_animation(back_lines: list[str], art_lines: list[str], position: str):
    """翻转动画 — 牌背收缩 → 卡牌展开。"""
    CARD_W = CARD_WIDTH
    flip_frames = 8

    for f in range(flip_frames):
        progress = (f + 1) / flip_frames
        if progress < 0.5:
            show_w = int(CARD_W * (1 - progress * 2))
            frame = [_clip_line(line, show_w, CARD_W) for line in back_lines]
        else:
            expand = (progress - 0.5) * 2
            show_w = int(CARD_W * expand)
            frame = [_clip_line(line, show_w, CARD_W) for line in art_lines]
        _render_frame(frame, position)
        time.sleep(FLIP_DURATION)


def _flash_effect(art_lines: list[str], position: str):
    """边框闪光效果。"""
    for _ in range(4):
        _clear()
        if position:
            _center_write(f"{C.s(C.ACCENT)}【{position}】{RESET}")
            sys.stdout.write("\n")
        for line in art_lines:
            _center_write(line)
        sys.stdout.flush()
        time.sleep(0.08)


def _show_keywords(card: TarotCard, is_reversed: bool):
    """显示关键词。"""
    if is_reversed:
        kw = card.keywords_reversed
        orient = f"{C.s(C.REVERSED)}逆位{RESET}"
    else:
        kw = card.keywords_upright
        orient = f"{C.s(C.UPRIGHT)}正位{RESET}"
    kw_str = "、".join(kw)
    _center_write(f"  {orient}  {C.s(C.TEXT_DIM)}{kw_str}{RESET}")
    sys.stdout.write("\n")
    sys.stdout.flush()


def reveal_card(card: TarotCard, is_reversed: bool, position: str = ""):
    """翻牌动画 — 牌背 → 问号 → 翻转 → 闪光。"""
    art_lines = _get_card_lines(card, is_reversed)
    back_lines = card_back_raw().split('\n')
    question_lines = question_raw().split('\n')

    # Frame 1: 牌背 (0.5s)
    _render_frame(back_lines, position)
    time.sleep(0.5)

    # Frame 2: 问号 (0.3s)
    _render_frame(question_lines, position)
    time.sleep(0.3)

    # Frame 3-10: 翻转动画
    _flip_animation(back_lines, art_lines, position)

    # Frame 11: 完整揭示
    _render_frame(art_lines, position)

    # Frame 12-14: 边框闪光
    _flash_effect(art_lines, position)

    # 关键词
    _show_keywords(card, is_reversed)


# ── 卡牌原始渲染（无像素艺术时的 fallback）──

def card_back_raw() -> str:
    """牌背 — 曼陀罗花纹 + 边框（带缓存）。"""
    global _cached_card_back
    if _cached_card_back is not None:
        return _cached_card_back

    w = CARD_WIDTH - 2  # 减去边框字符
    g = C.s(C.GOLD)
    d = C.s(C.GOLD_DIM)
    b = C.s(C.ACCENT)
    bg = C.bg(C.BG_CARD)
    lines = []
    lines.append(f"{g}{bg}╔{'═' * w}╗{RESET}")
    for y in range(18):
        row = ""
        for x in range(w):
            cx, cy = x - w // 2, y - 9
            dist = abs(cx) + abs(cy)
            adist = max(abs(cx), abs(cy))
            if dist == 0:
                row += f"{b}✦{RESET}"
            elif dist <= 2:
                row += f"{b}◆{RESET}"
            elif 5 <= dist <= 7:
                row += f"{d}◇{RESET}"
            elif 10 <= dist <= 12:
                row += f"{g}·{RESET}"
            elif abs(cx) <= 1 and 3 <= abs(cy) <= 8:
                row += f"{g}│{RESET}"
            elif abs(cy) <= 1 and 3 <= abs(cx) <= 12:
                row += f"{g}─{RESET}"
            elif adist >= 13 and dist <= 16:
                row += f"{d}✧{RESET}"
            else:
                row += " "
        lines.append(f"{g}{bg}║{RESET}{bg}{row}{g}{bg}║{RESET}")
    lines.append(f"{g}{bg}╚{'═' * w}╝{RESET}")
    _cached_card_back = "\n".join(lines)
    return _cached_card_back


def question_raw() -> str:
    """问号帧 — 发光球体 + 边框（带缓存）。"""
    global _cached_question
    if _cached_question is not None:
        return _cached_question

    w = CARD_WIDTH - 2  # 减去边框字符
    g = C.s(C.GOLD)
    b = C.s(C.GOLD_LIGHT)
    d = C.s(C.GOLD_DIM)
    bg = C.bg(C.BG_CARD)
    lines = []
    lines.append(f"{g}{bg}╔{'═' * w}╗{RESET}")
    for y in range(18):
        row = ""
        for x in range(w):
            cx, cy = x - w // 2, y - 9
            dist = (cx * cx + cy * cy) ** 0.5
            if dist < 2.5:
                row += f"{b}?{RESET}"
            elif 2.5 <= dist < 4:
                row += f"{b}·{RESET}"
            elif 4 <= dist < 5.5:
                row += f"{g}✦{RESET}"
            elif 5.5 <= dist < 7:
                row += f"{d}✧{RESET}"
            elif 7 <= dist < 8:
                row += f"{d}·{RESET}"
            else:
                row += " "
        lines.append(f"{g}{bg}║{RESET}{bg}{row}{g}{bg}║{RESET}")
    lines.append(f"{g}{bg}╚{'═' * w}╝{RESET}")
    _cached_question = "\n".join(lines)
    return _cached_question


def _center_plain(text: str, width: int) -> str:
    """按显示宽度居中纯文本（CJK 双宽）。"""
    dw = display_width(strip_ansi(text))
    pad = max(0, (width - dw) // 2)
    return " " * pad + text


def text_card_raw(card: TarotCard, is_reversed: bool) -> str:
    """纯文字卡牌（无像素艺术时的 fallback）。"""
    w = CARD_WIDTH
    border = "═" * w
    g = C.s(C.GOLD)
    symbol = "★" * 3 if not is_reversed else "☆" * 3
    sc = C.s(C.UPRIGHT) if not is_reversed else C.s(C.REVERSED)
    lines = [
        f"{g}╔{border}╗{RESET}",
        f"{g}║{' ' * w}║{RESET}",
        f"{g}║{RESET}{sc}{_center_plain(symbol, w)}{RESET}{g}║{RESET}",
        f"{g}║{' ' * w}║{RESET}",
        f"{g}║{RESET}{C.s(C.ACCENT)}{_center_plain(card.name, w)}{RESET}{g}║{RESET}",
        f"{g}║{RESET}{C.s(C.TEXT_BRIGHT)}{_center_plain(card.name_cn, w)}{RESET}{g}║{RESET}",
        f"{g}║{RESET}{C.s(C.GOLD)}{_center_plain(card.number, w)}{RESET}{g}║{RESET}",
        f"{g}║{' ' * w}║{RESET}",
        f"{g}╚{border}╝{RESET}",
    ]
    return "\n".join(lines)
