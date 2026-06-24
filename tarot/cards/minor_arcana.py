"""
Minor Arcana Pixel Art Generator v3
32×40 cards with LARGE suit symbols that fill the card.
"""
from typing import Optional

# ═══════════════════════════════════════════════════════════════
#  Color Palettes
# ═══════════════════════════════════════════════════════════════

SUIT_PALETTES = {
    "wands": {
        ".": "#0a111d", "S": "#e67e22", "s": "#d35400",
        "F": "#ff6b35", "G": "#a58040", "Y": "#ffdc78",
    },
    "cups": {
        ".": "#0a111d", "S": "#3498db", "s": "#2980b9",
        "F": "#5dade2", "G": "#1abc9c", "Y": "#76d7c4",
    },
    "swords": {
        ".": "#0a111d", "S": "#bdc3c7", "s": "#95a5a6",
        "F": "#ecf0f1", "G": "#506468", "Y": "#aab7b8",
    },
    "pentacles": {
        ".": "#0a111d", "S": "#27ae60", "s": "#1e8449",
        "F": "#2ecc71", "G": "#dab772", "Y": "#f0e0b0",
    },
}

# ═══════════════════════════════════════════════════════════════
#  LARGE Suit Symbols (28×32 - fills most of 32×40 card)
# ═══════════════════════════════════════════════════════════════

# Wand: tall staff with flame crown
WAND = [
    "...........FF...........",
    "..........F..F..........",
    ".........F.FF.F.........",
    ".........F.SS.F.........",
    "..........SSSS..........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "...........SS...........",
    "..........SSSS..........",
    ".........GGGGGG.........",
    "........GGGGGGGG........",
    ".......GGGGGGGGGG.......",
    "......GGGGGGGGGGGG......",
    ".....GGGGGGGGGGGGGG.....",
    "....GGGGGGGGGGGGGGGG....",
    "........................",
]

# Cup: wide chalice
CUP = [
    "..SSSSSSSSSSSSSSSSSS....",
    ".SS..................SS.",
    "S......................S",
    "S......................S",
    "S......................S",
    ".S....................S.",
    ".S....................S.",
    "..S..................S..",
    "..S..................S..",
    "...S................S...",
    "...SSSSSSSSSSSSSSSSSS...",
    ".........SSSSSS.........",
    ".........SSSSSS.........",
    ".........SSSSSS.........",
    ".........SSSSSS.........",
    ".........SSSSSS.........",
    ".........SSSSSS.........",
    "........SSSSSSSS........",
    ".......SSSSSSSSSS.......",
    "......SSSSSSSSSSSS......",
    ".....SSSSSSSSSSSSSS.....",
    "....SSSSSSSSSSSSSSSS....",
    "...SSSSSSSSSSSSSSSSSS...",
    "..SSSSSSSSSSSSSSSSSSSS..",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

# Sword: long blade with crossguard
SWORD = [
    "............S...........",
    "............S...........",
    "...........FSF..........",
    "...........FSF..........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    ".....SS.....S.....SS....",
    "....SSS.....S....SSS....",
    ".....SS.....S.....SS....",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "............S...........",
    "...........GGG..........",
    "..........GGGGG.........",
    ".........GGGGGGG........",
    "........GGGGGGGGG.......",
    ".......GGGGGGGGGGG......",
    "........................",
]

# Pentacle: large circle with star
PENTACLE = [
    "......SSSSSSSSSS........",
    "....SSS........SSS......",
    "...SS............SS.....",
    "..S................S....",
    ".S..................S...",
    "S....................S..",
    "S.......YYYY.........S..",
    "S......YYYYYY........S..",
    "S.....YY....YY.......S..",
    "S.....YY....YY.......S..",
    "S......YYYYYY........S..",
    "S.......YYYY.........S..",
    "S....................S..",
    ".S..................S...",
    "..S................S....",
    "...SS............SS.....",
    "....SSS........SSS......",
    "......SSSSSSSSSS........",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
]

SYMBOLS = {"wands": WAND, "cups": CUP, "swords": SWORD, "pentacles": PENTACLE}

# ═══════════════════════════════════════════════════════════════
#  Number Layout: smaller symbols for higher numbers
# ═══════════════════════════════════════════════════════════════

CARD_W, CARD_H = 32, 40

def _place(grid, symbol, cx, cy):
    """Place symbol centered at (cx, cy) on grid."""
    sh = len(symbol)
    sw = max(len(r) for r in symbol)
    for sy, row in enumerate(symbol):
        for sx, ch in enumerate(row):
            gx, gy = cx - sw // 2 + sx, cy - sh // 2 + sy
            if 0 <= gx < CARD_W and 0 <= gy < CARD_H and ch != '.':
                grid[gy][gx] = ch

def _place_small(grid, symbol, cx, cy, scale=0.5):
    """Place a scaled-down symbol."""
    sh = len(symbol)
    sw = max(len(r) for r in symbol)
    new_h = int(sh * scale)
    new_w = int(sw * scale)
    for ny in range(new_h):
        for nx in range(new_w):
            orig_x = int(nx / scale)
            orig_y = int(ny / scale)
            if orig_y < sh and orig_x < len(symbol[orig_y]):
                ch = symbol[orig_y][orig_x]
                gx, gy = cx - new_w // 2 + nx, cy - new_h // 2 + ny
                if 0 <= gx < CARD_W and 0 <= gy < CARD_H and ch != '.':
                    grid[gy][gx] = ch


def generate_number_card(suit: str, number: int) -> tuple[list[str], dict]:
    palette = SUIT_PALETTES[suit]
    symbol = SYMBOLS[suit]
    grid = [['.' for _ in range(CARD_W)] for _ in range(CARD_H)]

    if number == 1:
        # Ace: one large symbol centered
        _place(grid, symbol, CARD_W // 2, CARD_H // 2)
    elif number <= 3:
        # 2-3: stacked vertically, medium size
        positions = [(CARD_W // 2, 10 + i * 10) for i in range(number)]
        for px, py in positions:
            _place_small(grid, symbol, px, py, 0.7)
    elif number <= 6:
        # 4-6: 2-column layout, smaller
        positions = []
        rows = (number + 1) // 2
        for r in range(rows):
            for c in range(2):
                if len(positions) < number:
                    positions.append((10 + c * 12, 8 + r * 12))
        for px, py in positions:
            _place_small(grid, symbol, px, py, 0.5)
    elif number <= 10:
        # 7-10: 2 or 3 column layout, small
        positions = []
        cols = 3 if number >= 9 else 2
        rows_needed = (number + cols - 1) // cols
        for r in range(rows_needed):
            for c in range(cols):
                if len(positions) < number:
                    x = 8 + c * (CARD_W - 16) // max(cols - 1, 1)
                    y = 6 + r * (CARD_H - 12) // max(rows_needed - 1, 1)
                    positions.append((x, y))
        for px, py in positions:
            _place_small(grid, symbol, px, py, 0.35)

    ascii_art = [''.join(row) for row in grid]
    return ascii_art, palette


# ═══════════════════════════════════════════════════════════════
#  Face Card Portraits
# ═══════════════════════════════════════════════════════════════

PAGE = [
    "........SS........",
    ".......SSSS.......",
    ".......SSSS.......",
    "........SS........",
    ".......SSSS.......",
    "......SS..SS......",
    "......SS..SS......",
    ".......SSSS.......",
    ".......SSSS.......",
    "........SS........",
    "........SS........",
    ".......SS.SS......",
    "......SS...SS.....",
    ".....SS.....SS....",
]

KNIGHT = [
    ".......SS.........",
    "......SSSS........",
    "......SSSS........",
    ".......SS.........",
    "......SSSS........",
    ".....SS..SS.......",
    ".....SS..SS.......",
    "......SSSS........",
    "......SSSS........",
    ".....SS..SS.......",
    "....SS....SS......",
    "....SS....SS......",
    "...SS......SS.....",
    "..................",
]

QUEEN = [
    ".......Y.Y........",
    ".......YYY........",
    "........SS........",
    ".......SSSS.......",
    ".......SSSS.......",
    "........SS........",
    ".......SSSS.......",
    ".....SS....SS.....",
    ".....SS....SS.....",
    "......SSSSSS......",
    ".......SSSS.......",
    "........SS........",
    ".......SS.SS......",
    ".......SS.SS......",
]

KING = [
    ".....Y.Y.Y.......",
    ".....YYYYY.......",
    "......SS.........",
    ".....SSSS........",
    ".....SSSS........",
    ".....SSSS........",
    "....SSSSSS.......",
    "....SS..SS.......",
    "....SS..SS.......",
    ".....SSSS........",
    "......SS.........",
    ".....SS.SS.......",
    "....SS...SS......",
    "....SS...SS......",
]

FACE_FIGURES = {"page": PAGE, "knight": KNIGHT, "queen": QUEEN, "king": KING}


def generate_face_card(suit: str, rank: str) -> tuple[list[str], dict]:
    palette = SUIT_PALETTES[suit]
    figure = FACE_FIGURES[rank]
    grid = [['.' for _ in range(CARD_W)] for _ in range(CARD_H)]

    # Place figure centered
    fig_h = len(figure)
    fig_w = max(len(r) for r in figure)
    sx = (CARD_W - fig_w) // 2
    sy = (CARD_H - fig_h) // 2 - 2
    for y, row in enumerate(figure):
        for x, ch in enumerate(row):
            gx, gy = sx + x, sy + y
            if 0 <= gx < CARD_W and 0 <= gy < CARD_H and ch != '.':
                grid[gy][gx] = ch

    # Place suit symbol in corners
    _place_small(grid, SYMBOLS[suit], 6, 6, 0.4)
    _place_small(grid, SYMBOLS[suit], CARD_W - 6, CARD_H - 10, 0.4)

    ascii_art = [''.join(row) for row in grid]
    return ascii_art, palette


# ═══════════════════════════════════════════════════════════════
#  Batch Export
# ═══════════════════════════════════════════════════════════════

SUIT_NAMES = ["wands", "cups", "swords", "pentacles"]

def generate_all_minor_arcana() -> dict[int, tuple[list[str], dict]]:
    result = {}
    card_id = 22
    for suit in SUIT_NAMES:
        for num in range(1, 11):
            result[card_id] = generate_number_card(suit, num)
            card_id += 1
        for rank in ["page", "knight", "queen", "king"]:
            result[card_id] = generate_face_card(suit, rank)
            card_id += 1
    return result

MINOR_ARCANA_ART = generate_all_minor_arcana()
