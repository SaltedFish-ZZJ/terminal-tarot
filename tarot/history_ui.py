"""
Terminal Tarot - History UI Module
Handles all history-related UI: history list, reading detail, and keyword highlighting.
"""
import sys
import time
from typing import Optional

from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box

from tarot.style import (
    C, RESET, display_width, term_width, center_line, strip_ansi, vpad,
    S_GOLD, S_ACCENT, S_DIM, S_BRIGHT, S_BORDER, S_UPRIGHT, S_REVERSED,
)
from tarot.tui import TUI
from tarot.log import save_reading, get_recent_readings, get_reading_count


def _format_card_line(position: str, name_cn: str, reversed: bool,
                      keywords: list[str] | None = None, kw_limit: int = 40) -> Text:
    """统一的卡片信息行格式化（消除 4 处重复）。"""
    orient = "逆位" if reversed else "正位"
    orient_c = S_REVERSED if reversed else S_UPRIGHT
    t = Text()
    t.append(f"  【{position}】", style=S_ACCENT)
    t.append(name_cn, style=S_BRIGHT)
    t.append(f" · {orient}", style=orient_c)
    if keywords:
        t.append(f"  {'  '.join(keywords)[:kw_limit]}", style=S_DIM)
    return t


class HistoryUI:
    """历史 UI 管理器 - 处理所有历史记录相关的界面。"""

    def __init__(self, tui: TUI):
        self.tui = tui

    def show_history(self) -> str:
        """显示历史列表，返回 'menu' 或继续查看。"""
        while True:
            self.tui.clear()
            sys.stdout.write(vpad(28))
            sys.stdout.flush()

            readings = get_recent_readings(20)
            panel = self.tui.build_history_panel(readings)
            self.tui.print_centered(panel)
            print()

            choice = self.tui.get_choice(
                "▸ 输入编号查看详情 / Enter返回: ",
                valid=[str(i) for i in range(1, len(readings) + 1)] + [""]
            )

            if choice is None or choice == "":
                return "menu"

            # Show detail for selected reading
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(readings):
                    self._show_reading_detail(readings[idx])
            except ValueError:
                pass

    def _show_reading_detail(self, reading: dict):
        """Show full detail of a single reading."""
        self.tui.clear()
        sys.stdout.write(vpad(25))
        sys.stdout.flush()

        # Header
        self.tui.print_centered(Text("═" * 50, style=S_GOLD))
        self.tui.print_centered(Text("✦ 占卜记录详情 ✦", style=S_GOLD))
        self.tui.print_centered(Text("═" * 50, style=S_GOLD))
        print()

        # Metadata
        ts = reading.get("timestamp", "?")
        question = reading.get("question", "?")
        spread = reading.get("spread", "?")

        self.tui.print_centered(Text.from_markup(
            f"[{S_DIM}]时间：[/][{S_BRIGHT}]{ts}[/]"
        ))
        self.tui.print_centered(Text.from_markup(
            f"[{S_DIM}]牌阵：[/][{S_BRIGHT}]{spread}[/]"
        ))
        self.tui.print_centered(Text.from_markup(
            f"[{S_DIM}]问题：[/][{S_BRIGHT}]{question}[/]"
        ))
        print()

        # Cards
        cards = reading.get("cards", [])
        for c in cards:
            self.tui.print_centered(_format_card_line(
                c.get('position', ''), c.get('name_cn', c.get('name', '?')),
                c.get('reversed', False)))

        print()
        self.tui.print_rule(S_BORDER)
        print()

        # Reading text - 整段显示 + 关键词高亮
        reading_text = reading.get("reading", "")
        self._print_reading_with_highlight(reading_text)

        print()
        print()
        self.tui.print_rule(S_BORDER)
        print()
        self.tui.pause("按 Enter 返回列表...")

    def _print_reading_with_highlight(self, text: str):
        """带关键词高亮的解读文本显示。"""
        # 定义要高亮的关键词
        keywords = [
            "正位", "逆位", "愚者", "魔术师", "女祭司", "女皇", "皇帝", "教皇",
            "恋人", "战车", "力量", "隐士", "命运之轮", "正义", "倒吊人", "死神",
            "节制", "恶魔", "高塔", "星星", "月亮", "太阳", "审判", "世界",
            "权杖", "圣杯", "宝剑", "星币",
            "过去", "现在", "未来", "挑战", "根源", "结局",
        ]

        text_w = min(60, term_width() - 4)
        pad = max(0, (term_width() - text_w) // 2)

        for line in text.split('\n'):
            if not line.strip():
                print()
                continue

            # 高亮关键词
            display_line = line
            for kw in keywords:
                if kw in display_line:
                    display_line = display_line.replace(
                        kw, f"{C.s(C.ACCENT)}{kw}{RESET}"
                    )

            sys.stdout.write(" " * pad + display_line + "\n")
            sys.stdout.flush()
