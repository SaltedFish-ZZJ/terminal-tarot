"""
Terminal Tarot - Spreads UI Module
Handles all spread-related UI: single/three/celtic readings, panoramas, and AI reading display.
"""
import sys
import random
import time
from typing import Optional

from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
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

REVERSED_PROBABILITY = 0.35  # 逆位概率


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


class SpreadUI:
    """牌阵 UI 管理器 - 处理所有牌阵相关的界面。"""

    def __init__(self, tui: TUI, ai: AIReader):
        self.tui = tui
        self.ai = ai
        self._last_question = ""  # 记住上次问题，用于重新占卜

    def do_single_reading(self, question: str) -> str:
        """单牌占卜流程。"""
        self._last_question = question
        shuffle_animation(self.tui.console)

        card = random.choice(ALL_CARDS)
        is_reversed = random.random() < REVERSED_PROBABILITY

        reveal_card(card, is_reversed)
        self.tui.pause("按 Enter 查看解读...")

        return self._show_reading(
            question=question,
            cards=[{"card": card, "reversed": is_reversed, "position": "指引"}],
            spread_name="单牌指引",
        )

    def do_three_card_reading(self, question: str) -> str:
        """三牌占卜流程。"""
        self._last_question = question
        shuffle_animation(self.tui.console)

        positions = ["过去", "现在", "未来"]
        drawn = random.sample(ALL_CARDS, 3)
        reversed_flags = [random.random() < REVERSED_PROBABILITY for _ in range(3)]

        for i, (card, rev) in enumerate(zip(drawn, reversed_flags)):
            reveal_card(card, rev, position=positions[i])
            if self.tui.pause("按 Enter 查看下一张...", skip_key="S" if i < 2 else ""):
                # 跳过剩余动画
                for j in range(i + 1, 3):
                    self.tui.print(_format_card_line(
                        positions[j], drawn[j].name_cn, reversed_flags[j],
                        drawn[j].keywords_reversed if reversed_flags[j] else drawn[j].keywords_upright
                    ))
                break

        # Show all three side by side
        self._show_three_panorama(drawn, reversed_flags, positions)

        cards_data = [
            {"card": drawn[i], "reversed": reversed_flags[i], "position": positions[i]}
            for i in range(3)
        ]

        return self._show_reading(
            question=question,
            cards=cards_data,
            spread_name="三牌占卜 · 过去-现在-未来",
        )

    def do_celtic_cross_reading(self, question: str) -> str:
        """凯尔特十字流程。"""
        self._last_question = question
        shuffle_animation(self.tui.console)

        drawn = random.sample(ALL_CARDS, 10)
        reversed_flags = [random.random() < REVERSED_PROBABILITY for _ in range(10)]

        pos_names = [
            "现状", "挑战", "根源", "过去", "可能",
            "近未来", "自我", "环境", "希望", "结局",
        ]

        skip = False
        for i in range(10):
            if skip:
                self.tui.print(_format_card_line(
                    pos_names[i], drawn[i].name_cn, reversed_flags[i],
                    drawn[i].keywords_reversed if reversed_flags[i] else drawn[i].keywords_upright
                ))
            else:
                reveal_card(drawn[i], reversed_flags[i], position=pos_names[i])
                if self.tui.pause("按 Enter 查看下一张...", skip_key="S"):
                    skip = True
                    self.tui.clear()
                    self.tui.print_centered(Text("✦ 跳过动画 ✦", style=S_GOLD))
                    print()

        # Show Celtic Cross layout
        self._show_celtic_cross_panorama(drawn, reversed_flags, pos_names)

        cards_data = [
            {"card": drawn[i], "reversed": reversed_flags[i], "position": pos_names[i]}
            for i in range(10)
        ]

        return self._show_reading(
            question=question,
            cards=cards_data,
            spread_name="凯尔特十字 · 深度解读",
        )

    def rerun_spread(self, spread_name: str) -> str:
        """重新占卜 — 根据牌阵名重新执行，复用上次问题。"""
        question = self._last_question
        if not question:
            return "menu"
        if "单牌" in spread_name:
            return self.do_single_reading(question)
        elif "三牌" in spread_name:
            return self.do_three_card_reading(question)
        elif "凯尔特" in spread_name:
            return self.do_celtic_cross_reading(question)
        return "menu"

    def _show_three_panorama(self, drawn, reversed_flags, positions):
        """Show three cards side by side."""
        self.tui.clear()
        sys.stdout.write(vpad(30))
        sys.stdout.flush()
        self.tui.print_centered(Text("✦ 三牌全景 ✦", style=S_GOLD))
        print()

        from tarot.cards import CARD_ART
        tw = term_width()

        if tw >= 120:
            render_data = []
            for i, (card, rev) in enumerate(zip(drawn, reversed_flags)):
                art_info = CARD_ART.get(card.id)
                if art_info:
                    render_data.append({
                        "ascii": art_info["ascii"],
                        "color_map": art_info["color_map"],
                        "name_en": card.name,
                        "name_cn": card.name_cn,
                        "number": card.number,
                        "reversed": rev,
                    })
            if render_data:
                try:
                    horizontal = render_three_cards_horizontal(render_data, scale=1)
                    for line in horizontal.split('\n'):
                        sys.stdout.write(center_line(line, tw) + "\n")
                    sys.stdout.flush()
                except (KeyError, ValueError, IndexError):
                    self._show_three_list(drawn, reversed_flags, positions)
            else:
                self._show_three_list(drawn, reversed_flags, positions)
        else:
            self._show_three_list(drawn, reversed_flags, positions)

        print()
        self.tui.pause("按 Enter 继续...")

    def _show_three_list(self, drawn, reversed_flags, positions):
        for i, (card, rev) in enumerate(zip(drawn, reversed_flags)):
            kw = card.keywords_reversed if rev else card.keywords_upright
            self.tui.print(_format_card_line(positions[i], card.name_cn, rev, kw))

    def _show_celtic_cross_panorama(self, drawn, reversed_flags, pos_names):
        """Show Celtic Cross layout."""
        self.tui.clear()
        sys.stdout.write(vpad(40))
        sys.stdout.flush()
        self.tui.print_centered(Text("✦ 凯尔特十字全景 ✦", style=S_GOLD))
        print()

        from tarot.cards import CARD_ART
        render_data = []
        for i in range(10):
            card = drawn[i]
            art_info = CARD_ART.get(card.id)
            if art_info:
                render_data.append({
                    "ascii": art_info["ascii"],
                    "color_map": art_info["color_map"],
                    "name_en": card.name,
                    "name_cn": card.name_cn,
                    "number": card.number,
                    "reversed": reversed_flags[i],
                })
            else:
                render_data.append({
                    "ascii": ["." * 32] * 40,
                    "color_map": {".": "#0a111d"},
                    "name_en": card.name,
                    "name_cn": card.name_cn,
                    "number": card.number,
                    "reversed": reversed_flags[i],
                })

        try:
            layout = render_celtic_cross(
                render_data,
                [{"row": p.row, "col": p.col} for p in CELTIC_CROSS["positions"]],
                scale=1,
            )
            if layout is not None:
                # 网格渲染成功
                tw = term_width()
                for line in layout.split('\n'):
                    sys.stdout.write(center_line(line, tw) + "\n")
                sys.stdout.flush()
            else:
                # 终端太小，降级为文字列表
                self.tui.print_centered(Text("(终端较小，使用列表模式)", style=S_DIM))
                print()
                for i in range(10):
                    self.tui.print(_format_card_line(
                        pos_names[i], drawn[i].name_cn, reversed_flags[i],
                        drawn[i].keywords_reversed if reversed_flags[i] else drawn[i].keywords_upright
                    ))
        except (KeyError, ValueError, IndexError):
            for i in range(10):
                self.tui.print(_format_card_line(
                    pos_names[i], drawn[i].name_cn, reversed_flags[i]))

        print()
        self.tui.pause("按 Enter 继续...")

    def _show_reading(self, question: str, cards: list[dict], spread_name: str) -> str:
        """Show AI reading with premium UI."""
        self.tui.clear()
        sys.stdout.write(vpad(35))
        sys.stdout.flush()

        # ── Grand header ──
        stars = "★ · · · · ★ · · · · ★ · · · · ★"
        self.tui.print_centered(Text(stars, style=S_GOLD))
        self.tui.print_centered(Text("✦ 占卜解读 ✦", style=S_ACCENT))
        self.tui.print_centered(Text(stars, style=S_GOLD))
        print()

        # ── Question + Spread in Panel ──
        q_text = Text()
        q_text.append("  问  题  ", style=S_DIM)
        q_text.append(question, style=S_BRIGHT)
        q_text.append(f"\n  牌  阵  ", style=S_DIM)
        q_text.append(spread_name, style=S_GOLD)
        self.tui.print_centered(Panel(q_text, box=box.ROUNDED, border_style=S_BORDER,
                             title=f"[{S_DIM}]提问信息[/]"))
        print()

        # ── Card summary in Table ──
        table = Table(show_header=True, box=None, expand=True, padding=(0, 1))
        table.add_column("牌位", style=S_ACCENT, width=8)
        table.add_column("卡牌", style=S_BRIGHT)
        table.add_column("朝向", width=6)
        table.add_column("关键词", style=S_DIM)

        for c in cards:
            card = c["card"]
            rev = c.get("reversed", False)
            pos = c.get("position", "")
            orient = "逆位" if rev else "正位"
            orient_c = S_REVERSED if rev else S_UPRIGHT
            kw = "  ".join(card.keywords_reversed if rev else card.keywords_upright)
            table.add_row(
                f"【{pos}】",
                card.name_cn,
                f"[{orient_c}]{orient}[/]",
                kw[:30],
            )

        self.tui.print_centered(Panel(table, box=box.ROUNDED, border_style=S_GOLD,
                             title=f"[{S_GOLD}]牌面信息[/]"))
        print()

        # ── AI reading with streaming output ──
        reading_text = Text()
        full_reading = ""

        with Live(
            Panel(reading_text, box=box.ROUNDED, border_style=S_BORDER,
                  title=f"[{S_ACCENT}]✦ 月影解读 ✦[/]"),
            console=self.tui.console,
            refresh_per_second=20,
            transient=False,
        ) as live:
            for chunk in self.ai.read_stream(question, cards, spread_name):
                full_reading += chunk
                # Rebuild reading text for display
                reading_text = Text()
                read_lines = full_reading.split('\n')
                for rl in read_lines:
                    if rl.strip() == '':
                        reading_text.append('\n')
                    else:
                        reading_text.append('  ' + rl + '\n')
                live.update(
                    Panel(reading_text, box=box.ROUNDED, border_style=S_BORDER,
                          title=f"[{S_ACCENT}]✦ 月影解读 ✦[/]")
                )
            reading = full_reading
        print()

        # ── Save + Action bar ──
        timestamp = save_reading(question, cards, spread_name, reading)

        action_text = Text()
        action_text.append("  ✓ 已记录  ", style=S_DIM)
        action_text.append(timestamp, style=S_DIM)
        action_text.append("\n")
        action_text.append("  [R] 重新占卜   [H] 历史记录   [Enter] 返回菜单", style=S_DIM)
        self.tui.print_centered(Panel(action_text, box=box.ROUNDED, border_style=S_BORDER))
        print()

        sys.stdout.flush()

        choice = self.tui.get_choice("▸ ", valid=["r", "h", "", "q"])

        if choice == "h":
            return "history"
        if choice == "r":
            return self.rerun_spread(spread_name)
        if choice == "q":
            return "quit"
        return "menu"
