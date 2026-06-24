"""
Terminal Tarot - Main Application (TUI v2)
Uses Rich + prompt_toolkit for flicker-free, keyboard-driven experience.
"""
import os
import sys
import random
import time
from typing import Optional

from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box

from tarot.deck import TarotCard, ALL_CARDS, CARD_BY_ID, ELEMENT_INFO
from tarot.style import (
    C, RESET, display_width, term_width, center_line, strip_ansi, vpad,
    S_GOLD, S_ACCENT, S_DIM, S_BRIGHT, S_BORDER, S_UPRIGHT, S_REVERSED,
)
from tarot.renderer import (
    render_ascii_art, render_card,
    render_three_cards_horizontal, render_celtic_cross,
    print_centered, clear_screen, self_center_text,
)
from tarot.tui import TUI, EscapePressed
from tarot.animations import (
    shuffle_animation, reveal_card, card_back_raw, question_raw, text_card_raw,
)
from tarot.ai_reader import AIReader
from tarot.log import save_reading, get_recent_readings, get_reading_count
from tarot.spreads import CELTIC_CROSS
from tarot.spreads_ui import SpreadUI
from tarot.history_ui import HistoryUI

REVERSED_PROBABILITY = 0.35  # 逆位概率


# ── ASCII Logo (plain text for Rich) ──
LOGO_LINES = [
    "★ · · · · ★ · · · · ★ · · · · ★",
    "████████╗ █████╗ ███████╗██╗  ██╗",
    "╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝",
    "   ██║   ███████║███████╗█████╔╝",
    "   ██║   ██╔══██║╚════██║██╔═██╗",
    "   ██║   ██║  ██║███████║██║  ██╗",
    "   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
    "  ████████╗███████╗██████╗ ███╗   ███╗",
    "  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║",
    "     ██║   █████╗  ██████╔╝██╔████╔██║",
    "     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║",
    "     ██║   ███████╗██║  ██║██║ ╚═╝ ██║",
    "     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝",
    "★ · · · · ★ · · · · ★ · · · · ★",
    "        ✦ 终 端 塔 罗 牌 ✦",
]


class TarotApp:
    """Main application with TUI v2 engine."""

    def __init__(self):
        self.tui = TUI()
        self.ai = AIReader()
        self.running = True
        self.current_spread = "single"
        # UI 模块
        self.spread_ui = SpreadUI(self.tui, self.ai)
        self.history_ui = HistoryUI(self.tui)

    def run(self, skip_boot: bool = False):
        """Main loop."""
        try:
            self._show_boot(skip=skip_boot)
            while self.running:
                result = self._show_menu()
                if result == "quit":
                    self.running = False
        except KeyboardInterrupt:
            pass
        except Exception as e:
            # 捕获未处理的异常，显示错误信息而不是直接退出
            self.tui.clear()
            self.tui.print_centered(Text("✦ 发生错误 ✦", style=S_REVERSED))
            self.tui.print_centered(Text(str(e), style=S_DIM))
            print()
            import traceback
            traceback.print_exc()
            self.tui.pause("按 Enter 继续...")
        finally:
            self.ai.close()
            self._show_exit()

    # ═══════════════════════════════════════════════════════════
    #  Boot
    # ═══════════════════════════════════════════════════════════

    def _show_boot(self, skip: bool = False):
        from tarot.tui import boot_animation
        stats = {
            "cards": len(ALL_CARDS),
            "history": get_reading_count(),
            "ai": self.ai.is_configured(),
        }
        boot_animation(self.tui.console, stats, skip=skip)

    # ═══════════════════════════════════════════════════════════
    #  Menu
    # ═══════════════════════════════════════════════════════════

    def _show_menu(self) -> str:
        """显示菜单，返回 'quit' / 'h' / 'menu' / 或 reading 结果。"""
        self.tui.clear()
        # 垂直居中：装饰标题 5 行 + 空行 + panel ~10 行 + 空行 + prompt
        sys.stdout.write(vpad(16))
        sys.stdout.flush()

        # 装饰标题：菱形角标 + 英文大字
        deco = [
            "◆─ · ─ · ─ · ─ · ─ · ─ · ─ · ─ · ─ · ─·◆",
            "",
            "   R  E  V  E  A  L   D  E  S  T  I  N  Y",
            "",
            "◆─ · ─ · ─ · ─ · ─ · ─ · ─ · ─ · ─ · ─·◆",
        ]
        for line in deco:
            self.tui.print_centered(Text(line, style=S_GOLD))
        print()

        count = get_reading_count()
        ai_status = "AI ✓" if self.ai.is_configured() else "离线"

        options = [
            ("1", "单牌指引", "快速抽一张牌"),
            ("2", "三牌占卜", "过去 · 现在 · 未来"),
            ("3", "凯尔特十字", "深度解读（10张牌）"),
            ("h", "历史记录", f"共 {count} 条"),
            ("q", "退出", ""),
        ]

        panel = self.tui.build_menu_panel(
            options,
            stats=f"{len(ALL_CARDS)}牌",
            ai_status=ai_status,
        )
        self.tui.print_centered(panel)
        print()
        sys.stdout.flush()

        choice = self.tui.get_choice("▸ [1/2/3/h/q/?]: ",
                                     valid=["1", "2", "3", "h", "q", "", "?", "？"])

        if choice is None:  # ESC pressed
            return "menu"

        if not choice:  # Empty input, loop back
            return "menu"

        if choice in ("1", "2", "3"):
            # 选牌阵后进入输入问题循环
            spread_titles = {"1": "✦ 单牌指引 ✦", "2": "✦ 三牌占卜 ✦", "3": "✦ 凯尔特十字 ✦"}
            while True:
                question = self._ask_question(spread_titles[choice])
                if question is None:  # ESC → 回到菜单
                    return "menu"
                # 有问题 → 执行占卜
                if choice == "1":
                    return self.spread_ui.do_single_reading(question)
                elif choice == "2":
                    return self.spread_ui.do_three_card_reading(question)
                else:
                    return self.spread_ui.do_celtic_cross_reading(question)

        if choice == "h":
            return self.history_ui.show_history()
        elif choice == "q":
            return "quit"
        elif choice in ("?", "？"):
            self._show_help()
            return "menu"

        return "menu"

    # ═══════════════════════════════════════════════════════════
    #  Question Input (装饰版)
    # ═══════════════════════════════════════════════════════════

    def _ask_question(self, title: str) -> str | None:
        """显示装饰版问题输入页，返回问题文本或 None（取消）。"""
        while True:
            self.tui.clear()
            sys.stdout.write(vpad(12))
            sys.stdout.flush()

            # 极简标题
            self.tui.print_centered(Text(title, style=S_ACCENT))
            print()
            print()

            # 输入提示（居中）
            self.tui.print_centered(Text("✦ 请在心中默念你的问题 ✦", style=S_GOLD))
            print()

            question = self.tui.get_centered_input("▸ ")
            # ESC 返回 None → 回到菜单
            if question is None:
                return None
            # 用户输入了问题 → 返回问题文本
            if question:
                return question
            # 用户直接按 Enter（空输入）→ 居中提示并重新等待
            print()
            self.tui.print_centered(Text("⚠ 请输入你的问题", style=S_REVERSED))
            time.sleep(1.5)

    # ═══════════════════════════════════════════════════════════
    #  Help
    # ═══════════════════════════════════════════════════════════

    def _show_help(self):
        """显示帮助信息 — 快捷键参考。"""
        self.tui.clear()
        sys.stdout.write(vpad(14))
        sys.stdout.flush()

        # 标题
        self.tui.print_centered(Text("✦ 快捷键参考 ✦", style=S_GOLD))
        print()

        # 用 Rich Table 做整齐的快捷键列表
        table = Table(
            box=None,
            show_header=True,
            show_edge=False,
            pad_edge=False,
            padding=(0, 2),
        )
        table.add_column("按键", style=S_GOLD, justify="right", no_wrap=True, width=12)
        table.add_column("说明", style=S_DIM, min_width=36)

        # 分组快捷键
        groups = [
            ("导航", [
                ("ESC", "返回上一级"),
                ("Enter", "确认 / 下一步"),
                ("?", "显示此帮助"),
            ]),
            ("占卜", [
                ("S", "跳过翻牌动画"),
                ("R", "重新占卜"),
                ("H", "查看历史记录"),
            ]),
            ("系统", [
                ("Ctrl+C", "退出程序"),
            ]),
        ]

        for g_idx, (group_name, items) in enumerate(groups):
            if g_idx > 0:
                table.add_section()  # 组间分隔线
            # 组标题行
            table.add_row(Text(group_name, style=S_ACCENT), Text(""), end_section=False)
            for key, desc in items:
                table.add_row(f" {key}", f"  {desc}")

        # 将 table 渲染为居中
        from io import StringIO
        from rich.console import Console as _Console
        buf = StringIO()
        tmp = _Console(file=buf, width=term_width(), force_terminal=True, no_color=True)
        tmp.print(table)
        raw = buf.getvalue().rstrip("\n")
        for line in raw.splitlines():
            self.tui.print_centered(Text(line))
        print()
        self.tui.print_centered(Text("─── ◇ ───", style=S_DIM))
        print()
        self.tui.pause("按 Enter 返回菜单...")

    # ═══════════════════════════════════════════════════════════
    #  Exit
    # ═══════════════════════════════════════════════════════════

    def _show_exit(self):
        """退出画面 — 星轨渐隐动画。"""
        self.tui.clear()

        # 星轨渐隐动画
        exit_lines = [
            "★ · · · · ★ · · · · ★ · · · · ★",
            "",
            "✦ 感谢使用终端塔罗 ✦",
            "",
            "愿星光指引你的道路",
            "",
            "★ · · · · ★ · · · · ★ · · · · ★",
        ]

        # 垂直居中
        sys.stdout.write(vpad(len(exit_lines) + 4))
        sys.stdout.flush()

        # 渐显
        for line in exit_lines:
            if line:
                self.tui.print_centered(Text(line, style=S_GOLD))
            else:
                print()
            sys.stdout.flush()
            time.sleep(0.08)

        time.sleep(0.5)

        # 渐隐 - 逐行消失
        for i in range(len(exit_lines) - 1, -1, -1):
            # 移动光标到该行并清除
            sys.stdout.write(f"\033[{len(exit_lines) - i + 4}A")  # 向上移动
            sys.stdout.write("\033[2K")  # 清除该行
            sys.stdout.flush()
            time.sleep(0.05)

        # 最后清除剩余内容
        self.tui.clear()
