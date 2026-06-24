"""
The Fool (愚者) - Major Arcana 0
Pixel art: 32×40 grid, adapted from fool-data.js
"""

# Character → hex color mapping
FOOL_COLOR_MAP = {
    '.': '#0a111d',  # void/black
    'W': '#f0e0b0',  # cream/white highlight
    'g': '#dab772',  # gold (main)
    'G': '#a58040',  # dark gold
    'R': '#8b2500',  # dark red (rose)
    'S': '#f0d0a0',  # skin/peach
    'B': '#506468',  # blue-gray
    't': '#506468',  # teal (same as B)
    'Y': '#ffdc78',  # bright sun gold
}

# 32×40 pixel illustration (each string = one row, 32 chars wide)
FOOL_ART = [
    "................................",  # 0
    "..W.....Y.Y.Y.Y.Y.Y.Y.Y.......",  # 1  stars + sun rays
    "......Y...W...Y.Y.Y.Y.Y.Y.....",  # 2  sun
    ".....W..Y.Y.Y.Y.Y.Y.Y.Y...W...",  # 3  stars + sun
    "............Y.Y.Y.Y.Y.........",  # 4  sun rays
    "..............G...............",  # 5  hat tip
    ".............GGG..............",  # 6  hat
    "............GGGGG.............",  # 7  hat brim
    "............WSSW..............",  # 8  head
    "............WSSW..............",  # 9  head
    "..........GGWWWWGG............",  # 10 body top
    "..........GWWWWWWG............",  # 11 body
    "..........GWWWWWWG....R.......",  # 12 body + rose hand
    ".........GGWWWWWWGG..RR.......",  # 13 arms out
    "........GWGWWWWWWGWG.R........",  # 14 arms + rose
    "........G..WWWWWW..G.R........",  # 15 arms
    "........G..WWWWWW..G..........",  # 16 body lower
    "........G..WWWWWW..G..........",  # 17 body lower
    "..........W.GGGG.W............",  # 18 staff held
    "..........W..GG..W............",  # 19 legs
    "..........W..GG..W............",  # 20 legs
    "..........W..GG..W............",  # 21 legs
    "..........W..GG..W............",  # 22 legs
    "..........W..GG..W............",  # 23 legs
    "..........WW.GG.WW............",  # 24 feet
    "..........GGGGGGGG............",  # 25 ground
    "........GGGGGGGGGGGG..........",  # 26 ground
    "......GGGGGGGGGGGGGGGG........",  # 27 ground wide
    "....GGGGGGGGGGGGGGGGGGGG......",  # 28 ground wide
    "..GGGGGGGGGGGGGGGGGGGGGGGG....",  # 29 ground wide
    "GGGGGGGGGGGGGGGGGGGGGGGGGG....",  # 30 ground full
    ".WWWWWGGGGGGGGGGGGGGGGGGG.....",  # 31 dog
    "W...WWGGGGGGGGGGGGGGGGGG......",  # 32 dog
    ".W..W.GGGGGGGGGGGGGGGG........",  # 33 dog legs
    "WW...WGGGGGGGGGGGGGG..........",  # 34 dog legs
    "..W..WGGGGGGGGGGGGG...........",  # 35 dog tail
    "....WGGGGGGGGGGGG.............",  # 36 cliff edge
    "......GGGGGGGGGG..............",  # 37 cliff
    "........GGGGGGG................",  # 38 cliff
    "..........GGGG.................",  # 39 cliff tip
]
