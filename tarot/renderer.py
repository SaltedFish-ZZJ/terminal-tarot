"""
Pixel Art → Terminal True Color Renderer
Uses ANSI 24-bit color + half-block character (▀) for pixel-perfect rendering.
One character cell = two vertical pixels (fg = top, bg = bottom).
"""
import re
import sys
import os
from typing import Optional

from tarot.style import C, rgb, bg_rgb, RESET, BOLD, DIM, CLEAR, display_width, strip_ansi, term_width, term_height, center_line


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert '#RRGGBB' to (r, g, b)."""
    h = hex_color.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# ═══════════════════════════════════════════════════════════════
#  Core Renderer
# ═══════════════════════════════════════════════════════════════

def render_ascii_art(
    ascii_art: list[str],
    color_map: dict[str, str],
    scale: int = 2,
    bg_color: tuple[int, int, int] = C.BG_CARD,
) -> str:
    """
    Render ASCII pixel art to ANSI true-color terminal output.

    Uses half-block character ▀ (U+2580):
      - Foreground color = top pixel color
      - Background color = bottom pixel color
      - Each character row represents 2 pixel rows

    Args:
        ascii_art: List of strings, each char is a pixel key.
        color_map: Dict mapping char -> '#RRGGBB'.
        scale: Horizontal scale (1=normal, 2=double width, etc.)
        bg_color: Default background color (r,g,b).

    Returns:
        ANSI-escaped string ready for terminal output.
    """
    if not ascii_art:
        return ""

    # Pre-convert color map to RGB tuples for speed
    rgb_map: dict[str, tuple[int, int, int]] = {}
    for ch, hex_c in color_map.items():
        rgb_map[ch] = hex_to_rgb(hex_c)

    default_color = bg_color
    height = len(ascii_art)
    width = max(len(row) for row in ascii_art)

    output_lines: list[str] = []

    # Process two pixel rows at a time
    for y in range(0, height, 2):
        line_parts: list[str] = []
        for x in range(width):
            # Top pixel
            top_ch = ascii_art[y][x] if x < len(ascii_art[y]) else '.'
            top_rgb = rgb_map.get(top_ch, default_color)

            # Bottom pixel (might be out of bounds for odd heights)
            if y + 1 < height:
                bot_ch = ascii_art[y + 1][x] if x < len(ascii_art[y + 1]) else '.'
            else:
                bot_ch = '.'
            bot_rgb = rgb_map.get(bot_ch, default_color)

            # Skip fully transparent (bg-colored) pixels for cleanliness
            # Actually, keep them for the card background effect

            # Build ANSI escape: fg=top, bg=bottom, char=▀
            cell = (
                f"\033[38;2;{top_rgb[0]};{top_rgb[1]};{top_rgb[2]}m"
                f"\033[48;2;{bot_rgb[0]};{bot_rgb[1]};{bot_rgb[2]}m"
                "▀"
            )
            # Horizontal scale: repeat the character
            line_parts.append(cell * scale)

        output_lines.append("".join(line_parts) + RESET)

    return "\n".join(output_lines)


# ═══════════════════════════════════════════════════════════════
#  Card Frame Renderer
# ═══════════════════════════════════════════════════════════════

def render_card(
    ascii_art: list[str],
    color_map: dict[str, str],
    title_en: str,
    title_cn: str,
    number: str,
    is_reversed: bool = False,
    scale: int = 2,
) -> str:
    """
    Render a complete card with border, title, and number.

    Returns multi-line ANSI string.
    """
    art_width = len(ascii_art[0]) * scale if ascii_art else 0
    art_height = (len(ascii_art) + 1) // 2  # half-block rows

    # Card inner width (art + padding)
    inner_w = art_width + 4 * scale  # 2px padding each side

    lines: list[str] = []

    # ── Top border ──
    gold = C.s(C.GOLD)
    bg = C.bg(C.BG_CARD)
    border_top = gold + bg + "╔" + "═" * inner_w + "╗" + RESET
    lines.append(border_top)

    # ── Top padding ──
    pad_line = gold + bg + "║" + " " * inner_w + "║" + RESET
    lines.append(pad_line)

    # ── Render pixel art with left/right border ──
    art_lines = render_ascii_art(ascii_art, color_map, scale=scale).split('\n')

    # Pad art to centered position
    left_pad = 2 * scale  # 2 pixel padding
    right_pad = inner_w - art_width - left_pad

    for art_line in art_lines:
        border_line = (
            gold + bg + "║" + RESET
            + bg + " " * left_pad + RESET
            + art_line
            + bg + " " * right_pad + RESET
            + gold + bg + "║" + RESET
        )
        lines.append(border_line)

    # ── Bottom padding ──
    lines.append(pad_line)

    # ── Divider ──
    divider = gold + bg + "╠" + "═" * inner_w + "╣" + RESET
    lines.append(divider)

    # ── Title area ──
    # "THE FOOL · 愚者"
    if is_reversed:
        orientation = f" {C.s(C.REVERSED)}逆位{RESET}"
    else:
        orientation = f" {C.s(C.UPRIGHT)}正位{RESET}"

    title_display = f"{title_en} · {title_cn}"
    title_line = self_center_text(title_display, inner_w, C.s(C.ACCENT) + bg)
    lines.append(gold + bg + "║" + RESET + title_line + gold + bg + "║" + RESET)

    # Number + orientation
    num_display = f"{number}  {orientation}"
    num_line = self_center_text(num_display, inner_w, C.s(C.TEXT) + bg)
    lines.append(gold + bg + "║" + RESET + num_line + gold + bg + "║" + RESET)

    # ── Bottom padding ──
    lines.append(pad_line)

    # ── Bottom border ──
    border_bot = gold + bg + "╚" + "═" * inner_w + "╝" + RESET
    lines.append(border_bot)

    return "\n".join(lines)


def render_three_cards_horizontal(
    cards_data: list[dict],
    scale: int = 1,
) -> str:
    """
    Render three cards side by side for the three-card spread.
    
    cards_data: list of {"ascii": [...], "color_map": {...}, "name_en": str, 
                         "name_cn": str, "number": str, "reversed": bool, "position": str}
    """

    # Render each card individually
    card_strings = []
    for cd in cards_data:
        card_str = render_card(
            cd["ascii"], cd["color_map"],
            cd["name_en"], cd["name_cn"], cd["number"],
            is_reversed=cd.get("reversed", False),
            scale=scale,
        )
        card_strings.append(card_str)
    
    # Split into lines
    card_lines = [s.split('\n') for s in card_strings]
    
    # Find max lines
    max_lines = max(len(lines) for lines in card_lines)
    
    # Pad shorter cards
    for lines in card_lines:
        while len(lines) < max_lines:
            lines.append("")
    
    # Get visible width of each card (strip ANSI)
    card_widths = []
    for lines in card_lines:
        if lines:
            clean = strip_ansi(lines[0])
            card_widths.append(len(clean))
        else:
            card_widths.append(0)
    
    # Concatenate side by side with 2-char gap
    gap = "  "
    result_lines = []
    for i in range(max_lines):
        parts = []
        for j, lines in enumerate(card_lines):
            line = lines[i]
            # Pad to card width
            clean = strip_ansi(line)
            visible_len = display_width(clean)
            target_w = card_widths[j]
            if visible_len < target_w:
                line = line + " " * (target_w - visible_len)
            parts.append(line)
        result_lines.append(gap.join(parts))
    
    return "\n".join(result_lines)


def _prepare_card_renders(
    cards_data: list[dict], scale: int
) -> tuple[list[list[str]], list[int]]:
    """准备卡牌渲染数据，返回 (渲染行列表, 宽度列表)。"""
    card_renders = []
    for cd in cards_data:
        card_str = render_card(
            cd["ascii"], cd["color_map"],
            cd["name_en"], cd["name_cn"], cd["number"],
            is_reversed=cd.get("reversed", False),
            scale=scale,
        )
        card_renders.append(card_str.split('\n'))

    # 统一高度
    max_lines = max(len(lines) for lines in card_renders)
    for lines in card_renders:
        while len(lines) < max_lines:
            lines.append("")

    # 计算宽度
    card_widths = []
    for lines in card_renders:
        if lines:
            clean = strip_ansi(lines[0])
            card_widths.append(len(clean))
        else:
            card_widths.append(0)

    return card_renders, card_widths


def _build_position_map(positions: list[dict]) -> dict[tuple[int, int], int]:
    """构建位置映射: (row, col) -> card_index。"""
    return {(pos["row"], pos["col"]): i for i, pos in enumerate(positions)}


def _place_card_on_grid(
    output: list[list[str]],
    ansi_grid: list[list[str]],
    lines: list[str],
    col_start: int,
    row_start: int,
    total_w: int,
    total_h: int,
):
    """将单张卡牌放置到网格指定位置。"""
    for ly, line in enumerate(lines):
        row = row_start + ly
        if row >= total_h:
            break

        ansi_parts = re.split(r'(\033\[[0-9;]*m)', line)
        out_col = col_start
        current_style = ""

        for part in ansi_parts:
            if part.startswith('\033['):
                current_style = part
            else:
                for ch in part:
                    if 0 <= out_col < total_w:
                        output[row][out_col] = ch
                        ansi_grid[row][out_col] = current_style
                    out_col += 1


def _grid_to_lines(output: list[list[str]], ansi_grid: list[list[str]]) -> list[str]:
    """将网格转换为带 ANSI 样式的字符串行。"""
    result_lines = []
    for row in range(len(output)):
        parts = []
        for col in range(len(output[row])):
            ch = output[row][col]
            style = ansi_grid[row][col]
            if ch != ' ' and style:
                parts.append(style + ch + "\033[0m")
            else:
                parts.append(ch)
        result_lines.append("".join(parts))
    return result_lines


def render_celtic_cross(
    cards_data: list[dict],
    positions: list[dict],
    scale: int = 1,
) -> str | None:
    """
    Render the Celtic Cross spread (10 cards).

    Layout grid (7 columns × 8 rows):
           [10]
            |
     [9]    |    [8]
            |
     [7] [1][4][5]
            |
           [2]
            |
           [3]
            |
           [6]

    Returns None if the grid exceeds terminal size (caller should fallback to list).
    """
    GRID_COLS = 7
    GRID_ROWS = 8

    # 准备卡牌数据
    card_renders, card_widths = _prepare_card_renders(cards_data, scale)
    pos_map = _build_position_map(positions)

    # 计算网格尺寸
    card_h = len(card_renders[0]) if card_renders else 0
    card_w = max(card_widths) if card_widths else 38
    gap = 2
    cell_h = card_h
    cell_w = card_w + gap
    total_h = GRID_ROWS * cell_h
    total_w = GRID_COLS * cell_w

    # 检测终端尺寸，超出时降级
    term_w = term_width()
    term_h = term_height()
    if total_w > term_w or total_h > term_h:
        return None

    # 创建空网格
    output = [[' '] * total_w for _ in range(total_h)]
    ansi_grid = [[''] * total_w for _ in range(total_h)]

    # 放置每张卡牌
    for (gr, gc), idx in pos_map.items():
        if idx >= len(card_renders):
            continue
        cw = card_widths[idx] if idx < len(card_widths) else card_w
        col_start = gc * cell_w + (cell_w - cw) // 2
        row_start = gr * cell_h

        _place_card_on_grid(
            output, ansi_grid, card_renders[idx],
            col_start, row_start, total_w, total_h,
        )

    return "\n".join(_grid_to_lines(output, ansi_grid))


def self_center_text(text: str, width: int, style_prefix: str = "") -> str:
    """居中文字到固定宽度，带 ANSI 样式前缀和右填充。"""
    clean = strip_ansi(text)
    visible_len = display_width(clean)
    if visible_len >= width:
        return style_prefix + text + RESET

    centered = center_line(text, width)
    right = width - visible_len - max(0, (width - visible_len) // 2)
    return style_prefix + centered + ' ' * max(0, right) + RESET


# ═══════════════════════════════════════════════════════════════
#  Animation Helpers
# ═══════════════════════════════════════════════════════════════

def print_centered(text: str, width: Optional[int] = None):
    """Print text centered in the terminal."""
    if width is None:
        width = term_width()
    clean = strip_ansi(text)
    visible_len = display_width(clean)
    padding = max(0, (width - visible_len) // 2)
    print(" " * padding + text)


def print_line(color: tuple[int, int, int] = C.BORDER, char: str = "─", width: Optional[int] = None):
    """Print a horizontal line."""
    if width is None:
        width = term_width()
    fg_str = C.s(color)
    line = fg_str + char * width + RESET
    print(line)


def clear_screen():
    """Clear the terminal screen."""
    print(CLEAR, end='', flush=True)
