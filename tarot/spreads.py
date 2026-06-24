"""
Tarot Spread Definitions
Defines card layouts for different spreads.
"""
from dataclasses import dataclass


@dataclass
class SpreadPosition:
    name: str
    name_cn: str
    description: str
    # Layout position for terminal rendering (row, col) in grid units
    row: int
    col: int


# ═══════════════════════════════════════════════════════════════
#  Single Card
# ═══════════════════════════════════════════════════════════════

SINGLE = {
    "name": "Single Card",
    "name_cn": "单牌指引",
    "description": "快速抽一张牌，获取当下的核心提示",
    "positions": [
        SpreadPosition("Guidance", "指引", "当下的核心提示", 0, 0),
    ],
}


# ═══════════════════════════════════════════════════════════════
#  Three Card
# ═══════════════════════════════════════════════════════════════

THREE_CARD = {
    "name": "Three Card",
    "name_cn": "三牌占卜",
    "description": "过去 · 现在 · 未来",
    "positions": [
        SpreadPosition("Past", "过去", "事件的根源", 0, 0),
        SpreadPosition("Present", "现在", "当前的处境", 0, 1),
        SpreadPosition("Future", "未来", "可能的方向", 0, 2),
    ],
}


# ═══════════════════════════════════════════════════════════════
#  Celtic Cross (凯尔特十字)
#  
#  Layout (10 positions):
#
#           [10] 审判
#            |
#    [9] 希望 | [8] 环境
#            |
#  [7] 自我 [1] 现状 [4] 过去 [5] 可能
#            |
#           [2] 挑战
#            |
#           [3] 根源
#            |
#           [6] 近未来
#
# ═══════════════════════════════════════════════════════════════

CELTIC_CROSS = {
    "name": "Celtic Cross",
    "name_cn": "凯尔特十字",
    "description": "十张牌的深度解读牌阵",
    "positions": [
        SpreadPosition("Present",    "现状",  "你和你的情况",          3, 2),
        SpreadPosition("Challenge",  "挑战",  "你面前的障碍",          4, 2),
        SpreadPosition("Root",       "根源",  "问题的根源",            5, 2),
        SpreadPosition("Past",       "过去",  "已过去的影响",          3, 4),
        SpreadPosition("Possible",   "可能",  "最好的可能结果",        3, 5),
        SpreadPosition("Near Future","近未来","即将发生的事",          6, 2),
        SpreadPosition("Self",       "自我",  "你的态度",              3, 0),
        SpreadPosition("Environment","环境",  "外部影响",              3, 6),
        SpreadPosition("Hope",       "希望",  "你希望的/恐惧的",       2, 0),
        SpreadPosition("Outcome",    "结局",  "最终结果",              1, 2),
    ],
}


# ═══════════════════════════════════════════════════════════════
#  Spread Registry
# ═══════════════════════════════════════════════════════════════

SPREADS = {
    "single": SINGLE,
    "three_card": THREE_CARD,
    "celtic_cross": CELTIC_CROSS,
}


def get_spread(name: str) -> dict:
    """Get spread definition by name."""
    return SPREADS.get(name, SINGLE)
