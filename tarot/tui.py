"""
TUI Engine v2.2 - Fixed CJK/emoji alignment
"""
import sys
import time
import threading
from typing import Optional, Callable

from tarot import __version__

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory

from tarot.style import (
    C, RESET, display_width, strip_ansi, term_width, center_line,
    S_GOLD, S_ACCENT, S_DIM, S_BRIGHT, S_BORDER,
)
from tarot.interfaces import TUIEngine


# ═══════════════════════════════════════════════════════════════
#  Blinking Cursor
# ═══════════════════════════════════════════════════════════════

_blink_running = False

def blink_cursor(prompt: str = "▸ ", duration: float = 2.0):
    global _blink_running
    _blink_running = True

    def _blink():
        global _blink_running
        visible = True
        end_time = time.time() + duration
        while time.time() < end_time and _blink_running:
            ch = "▌" if visible else " "
            sys.stdout.write(f"\r{C.s(C.ACCENT)}{prompt}{RESET}{ch}")
            sys.stdout.flush()
            visible = not visible
            time.sleep(0.4)
        sys.stdout.write(f"\r{C.s(C.ACCENT)}{prompt}{RESET}")
        sys.stdout.flush()
        _blink_running = False

    t = threading.Thread(target=_blink, daemon=True)
    t.start()
    return t

def stop_blink():
    global _blink_running
    _blink_running = False


# ═══════════════════════════════════════════════════════════════
#  8-bit Boot Screen (fixed alignment)
# ═══════════════════════════════════════════════════════════════

# ANSI helpers — 引用 style.C 统一色源
_G = C.s(C.GOLD)        # gold
_D = C.s(C.TEXT_DIM)    # dim
_B = C.s(C.TEXT_BRIGHT) # bright
_A = C.s(C.ACCENT)      # accent
_W = C.s(C.GLOW)        # glow
_R = RESET              # reset



def _pad_right(text: str, width: int) -> str:
    """Pad text with spaces to fill width (accounting for display width)."""
    dw = display_width(text)
    return text + ' ' * max(0, width - dw)


def _center(text: str, width: int) -> str:
    """居中并右填充到固定宽度（用于 box 内部）。"""
    centered = center_line(text, width)
    dw = display_width(strip_ansi(text))
    right = width - dw - max(0, (width - dw) // 2)
    return centered + ' ' * max(0, right)


def render_boot_frame(stats: dict) -> str:
    """Render the complete boot screen with pixel-art frame style."""
    W = 44  # inner content width
    pad = max(0, (term_width() - W - 4) // 2)
    P = " " * pad  # left padding for centering

    card_count = stats.get("cards", 78)
    history_count = stats.get("history", 0)
    ai_ready = stats.get("ai", False)
    ai_text = "月影 AI · 就绪" if ai_ready else "月影 AI · 离线"

    # 颜色
    dim = _D   # TEXT_DIM
    gold = _G  # GOLD
    white = _W # WHITE
    accent = _A # ACCENT

    lines = []

    # 内框 top (░░░)
    lines.append(f"{P}{gold}{'░' * (W + 2)}{_R}")

    # 星轨
    stars = "★ · · · · ★ · · · · ★ · · · · ★"
    lines.append(f"{P}{gold}░{' ' * W}░{_R}")
    lines.append(f"{P}{gold}░{_R}{white}{_center(stars, W)}{_R}{gold}░{_R}")
    lines.append(f"{P}{gold}░{' ' * W}░{_R}")

    # Logo ASCII art — TAROT/TERM 统一宽度 37，首字母 T 对齐
    logo_lines = [
        "████████╗ █████╗ ███████╗██╗  ██╗    ",
        "╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝    ",
        "   ██║   ███████║███████╗█████╔╝     ",
        "   ██║   ██╔══██║╚════██║██╔═██╗     ",
        "   ██║   ██║  ██║███████║██║  ██╗    ",
        "   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ",
        "████████╗███████╗██████╗ ███╗   ███╗ ",
        "╚══██╔══╝██╔════╝██╔══██╗████╗ ████║ ",
        "   ██║   █████╗  ██████╔╝██╔████╔██║ ",
        "   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║ ",
        "   ██║   ███████╗██║  ██║██║ ╚═╝ ██║ ",
        "   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ",
    ]
    for logo_line in logo_lines:
        lines.append(f"{P}{gold}░{_R}{white}{_center(logo_line, W)}{_R}{gold}░{_R}")

    # 中文标题
    lines.append(f"{P}{gold}░{' ' * W}░{_R}")
    lines.append(f"{P}{gold}░{_R}{accent}{_center('✦ 终 端 塔 罗 牌 ✦', W)}{_R}{gold}░{_R}")
    lines.append(f"{P}{gold}░{' ' * W}░{_R}")

    # 分隔线
    divider = "─────── ◆ ───────"
    lines.append(f"{P}{gold}░{_R}{dim}{_center(divider, W)}{_R}{gold}░{_R}")
    lines.append(f"{P}{gold}░{' ' * W}░{_R}")

    # 信息行
    s1 = f"▪ {card_count} 张牌    ▪ {history_count} 条记录"
    s2 = f"▪ 3 种牌阵   ▪ {ai_text}"
    lines.append(f"{P}{gold}░{_R}{dim}{_center(s1, W)}{_R}{gold}░{_R}")
    lines.append(f"{P}{gold}░{_R}{dim}{_center(s2, W)}{_R}{gold}░{_R}")
    lines.append(f"{P}{gold}░{' ' * W}░{_R}")

    # 按 Enter 提示
    press = "▸ 按 ENTER 揭示命运 ◂"
    lines.append(f"{P}{gold}░{_R}{accent}{_center(press, W)}{_R}{gold}░{_R}")
    lines.append(f"{P}{gold}░{' ' * W}░{_R}")

    # 内框 bottom
    lines.append(f"{P}{gold}{'░' * (W + 2)}{_R}")

    return "\n".join(lines)


def boot_animation(console: Console, stats: dict, skip: bool = False):
    """Show boot screen with pixel-art animation."""
    frame = render_boot_frame(stats)
    lines = frame.split("\n")

    if skip:
        sys.stdout.write("\033[2J\033[H")
        from tarot.style import vpad
        sys.stdout.write(vpad(len(lines)))
        sys.stdout.write(frame + "\n")
        sys.stdout.flush()
        input()
        return

    # 清屏 + 垂直居中
    sys.stdout.write("\033[2J\033[H")
    from tarot.style import vpad
    sys.stdout.write(vpad(len(lines)))
    sys.stdout.flush()

    # 逐行动画输出
    for i, line in enumerate(lines):
        sys.stdout.write(line + "\n")
        sys.stdout.flush()

        # 外框行（▓▓▓）— 快速
        if "▓" in line and "░" not in line:
            time.sleep(0.03)
        # 内框行（░░░）— 中速
        elif "░" in line and "★" not in line and "█" not in line:
            time.sleep(0.05)
        # 星轨 — 慢
        elif "★" in line:
            time.sleep(0.1)
        # Logo — 逐行出现
        elif "█" in line:
            time.sleep(0.06)
        # 中文标题 — 慢
        elif "终" in line:
            time.sleep(0.15)
        # 分隔线 — 中速
        elif "◆" in line:
            time.sleep(0.1)
        # 信息行 — 中速
        elif "▪" in line:
            time.sleep(0.08)
        # 提示 — 慢
        elif "ENTER" in line:
            time.sleep(0.12)
        else:
            time.sleep(0.02)

    # 等待用户按 Enter
    time.sleep(0.3)
    input()


# ═══════════════════════════════════════════════════════════════
#  TUI Engine
# ═══════════════════════════════════════════════════════════════

class TUI(TUIEngine):
    def __init__(self):
        self.console = Console()
        self._back_requested = False
        self._bindings = KeyBindings()
        self._setup_bindings()

    def _setup_bindings(self):
        @self._bindings.add('escape')
        def _(event):
            self._back_requested = True
            event.app.exit(exception=EscapePressed())

        @self._bindings.add('c-c')
        def _(event):
            self._back_requested = True
            event.app.exit(exception=EscapePressed())

    def _get_output(self):
        try:
            from prompt_toolkit.output import Win32Output
            return Win32Output(sys.stdout)
        except Exception:
            return None

    def clear(self):
        self.console.clear()

    def print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)

    def print_centered(self, text, style=None):
        if isinstance(text, (Panel, Table, Text)):
            self.console.print(text, justify="center", highlight=False)
        else:
            w = term_width()
            plain = str(text)
            clean = strip_ansi(plain)
            padding = max(0, (w - display_width(clean)) // 2)
            if style:
                self.console.print(" " * padding + str(text), style=style)
            else:
                self.console.print(" " * padding + str(text), highlight=False)

    def print_rule(self, color=S_BORDER):
        from rich.rule import Rule
        self.console.print(Rule(style=color))

    def build_menu_panel(self, options, stats="", ai_status=""):
        # 选项图标映射
        icons = {"1": "🔮", "2": "✦", "3": "❀", "h": "📜", "q": "🚪"}

        table = Table(show_header=False, box=None, padding=(0, 1), expand=True)
        table.add_column("icon", width=3)
        table.add_column("key", width=5)
        table.add_column("title", style=S_BRIGHT, ratio=1)
        table.add_column("desc", style=S_DIM, ratio=1, no_wrap=True)

        for key, title, desc in options:
            icon = icons.get(key, "▸")
            key_text = Text(f"[{key}]", style=f"{S_GOLD} bold")
            table.add_row(icon, key_text, title, f"— {desc}" if desc else "")

        # 装饰分隔线
        divider = Text("─── ◇ ───", style=S_DIM)

        footer_parts = []
        if stats:
            footer_parts.append(stats)
        if ai_status:
            footer_parts.append(ai_status)
        footer = "  ·  ".join(footer_parts)

        content = Table(show_header=False, box=None, expand=True)
        content.add_column(justify="center")
        content.add_row(table)
        content.add_row(Text(""))
        content.add_row(divider)
        if footer:
            content.add_row(Text(f"\n  {footer}", style=S_DIM))

        return Panel(
            content,
            title=f"[{S_GOLD}]✦ 终端塔罗牌占卜 ✦[/]",
            subtitle=f"[{S_DIM}]v{__version__} · 云舒 × Hermes[/]",
            border_style=S_GOLD,
            box=box.DOUBLE,
            expand=True,
            width=min(term_width() - 4, 72),
        )

    def build_history_panel(self, readings):
        if not readings:
            content = Text("暂无占卜记录。", style=S_DIM)
            return Panel(content, title=f"[{S_GOLD}]✦ 占卜历史 ✦[/]",
                        border_style=S_GOLD, box=box.ROUNDED)

        table = Table(show_header=True, box=box.SIMPLE_HEAVY, expand=True,
                      header_style=S_GOLD)
        table.add_column("#", width=3)
        table.add_column("时间", width=20)
        table.add_column("问题", ratio=3)
        table.add_column("牌面", ratio=2)

        for i, r in enumerate(readings, 1):
            cards_str = " → ".join(
                f"{c['name_cn']}({'逆' if c['reversed'] else '正'})"
                for c in r.get("cards", [])
            )
            table.add_row(
                str(i),
                r.get("timestamp", "?")[-8:],
                r.get("question", "?")[:25],
                cards_str[:30],
            )

        footer = Text("\n[数字] 查看详情  [Enter] 返回", style=S_DIM)

        content = Table(show_header=False, box=None, expand=True)
        content.add_column()
        content.add_row(table)
        content.add_row(footer)

        return Panel(
            content,
            title=f"[{S_GOLD}]✦ 占卜历史 ✦[/]",
            border_style=S_GOLD,
            box=box.ROUNDED,
            expand=True,
        )

    def get_input(self, prompt: str = "▸ ") -> Optional[str]:
        self._back_requested = False
        try:
            session = PromptSession(
                history=InMemoryHistory(),
                key_bindings=self._bindings,
                complete_while_typing=False,
                output=self._get_output(),
            )
            result = session.prompt(
                HTML(f'<rgb(232,196,124)>{prompt}</rgb(232,196,124)>'),
            )
            if self._back_requested:
                return None
            return result.strip()
        except (EscapePressed, KeyboardInterrupt):
            self._back_requested = True
            return None
        except Exception:
            try:
                result = input(f"{C.s(C.ACCENT)}{prompt}{RESET}")
                return result.strip()
            except (EOFError, KeyboardInterrupt):
                return None

    def get_centered_input(self, prompt: str = "▸ ") -> Optional[str]:
        """动态居中输入 — 提示符和输入内容都保持居中。"""
        self._back_requested = False
        try:
            from prompt_toolkit import Application
            from prompt_toolkit.buffer import Buffer
            from prompt_toolkit.layout import Layout, Window
            from prompt_toolkit.layout.controls import BufferControl

            # 创建 buffer
            buf = Buffer(multiline=False)

            # 动态计算居中前缀的函数
            def get_prefix(cli, lineno):
                if lineno > 0:
                    return []
                tw = term_width()
                text_w = display_width(buf.text)
                prompt_w = display_width(prompt)
                # 总宽度 = 提示符 + 输入内容
                total_w = prompt_w + text_w
                # 居中偏移
                spaces = max(0, (tw - total_w) // 2)
                return [('class:prompt', ' ' * spaces + prompt)]

            # 创建 buffer control
            control = BufferControl(buffer=buf)

            # 创建窗口
            win = Window(control, get_line_prefix=get_prefix, wrap_lines=False)

            # 创建布局
            layout = Layout(win)

            # 创建应用
            app = Application(
                layout=layout,
                key_bindings=self._bindings,
                output=self._get_output(),
                erase_when_done=True,
                full_screen=False,
            )

            # 设置 accept handler — app.exit(result=...) 会将 result 作为 run() 的返回值
            buf.accept_handler = lambda _: app.exit(result=buf.text)

            # 运行应用，返回值是 accept_handler 中 app.exit(result=...) 设置的值
            result = app.run()

            if self._back_requested:
                return None
            # 使用 run() 的返回值，而不是 buf.text（因为 buf 可能已被清理）
            return result.strip() if result else None
        except (EscapePressed, KeyboardInterrupt):
            self._back_requested = True
            return None
        except Exception:
            try:
                result = input(f"{C.s(C.ACCENT)}{prompt}{RESET}")
                return result.strip()
            except (EOFError, KeyboardInterrupt):
                return None

    def get_choice(self, prompt: str = "▸ ", valid: list[str] = None) -> Optional[str]:
        """获取用户选择。无效输入时提示并重新等待，返回值保证在 valid 中或 None(ESC)。"""
        self._back_requested = False
        while True:
            try:
                session = PromptSession(
                    key_bindings=self._bindings,
                    complete_while_typing=False,
                    output=self._get_output(),
                )
                result = session.prompt(
                    HTML(f'<rgb(232,196,124)>{prompt}</rgb(232,196,124)>'),
                )
                if self._back_requested:
                    return None
                choice = result.strip().lower()
                if valid and choice not in valid:
                    sys.stdout.write(f"{C.s(C.REVERSED)}  ⚠ 无效选项{RESET}\n")
                    sys.stdout.flush()
                    continue
                return choice
            except (EscapePressed, KeyboardInterrupt):
                self._back_requested = True
                return None
            except Exception:
                try:
                    result = input(f"{C.s(C.ACCENT)}{prompt}{RESET}")
                    choice = result.strip().lower()
                    if valid and choice not in valid:
                        sys.stdout.write(f"{C.s(C.REVERSED)}  ⚠ 无效选项{RESET}\n")
                        sys.stdout.flush()
                        continue
                    return choice
                except (EOFError, KeyboardInterrupt):
                    return None

    def pause(self, msg: str = "按 Enter 继续...", skip_key: str = "") -> bool:
        """暂停等待用户输入。返回 True 如果用户按了跳过键。"""
        if skip_key:
            result = self.get_choice(f"{msg} [S]跳过: ", valid=["", skip_key.lower()])
            return result == skip_key.lower()
        else:
            self.get_choice(f"{msg} ")
            return False


class EscapePressed(Exception):
    pass
