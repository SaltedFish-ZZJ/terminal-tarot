#!/usr/bin/env python3
"""
Terminal Tarot - 终端像素塔罗牌占卜

Usage:
    python main.py              # Interactive TUI mode
    python main.py --test       # Quick test: render The Fool card
    python main.py --skip-boot  # Skip boot animation
    python main.py --version
"""
import sys
import os
import argparse

# Windows GBK 兼容：强制 stdout 用 UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(
        description="Terminal Tarot - 终端像素塔罗牌占卜",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py              # 交互模式
  python main.py --test       # 测试渲染愚者卡
  python main.py --skip-boot  # 跳过开机动画
        """
    )
    parser.add_argument('--version', '-v', action='version',
                       version='Terminal Tarot v0.7.5')
    parser.add_argument('--test', '-t', action='store_true',
                       help='测试模式：渲染愚者卡')
    parser.add_argument('--skip-boot', '-s', action='store_true',
                       help='跳过开机动画')

    args = parser.parse_args()

    if args.test:
        run_test()
        return

    from tarot.app import TarotApp
    app = TarotApp()
    app.run(skip_boot=args.skip_boot)


def run_test():
    """Quick test: render The Fool card and show it."""
    import sys
    from tarot.style import C, RESET
    from tarot.renderer import render_ascii_art, render_card, print_centered, print_line, clear_screen
    from tarot.cards import CARD_ART
    from tarot.deck import CARD_BY_ID

    clear_screen()
    print()

    print_centered(C.s(C.GOLD) + "✦ Terminal Tarot · Test Mode ✦" + RESET)
    print()
    print_line(C.GOLD_DIM)
    print()

    fool_data = CARD_ART.get(0)
    fool_card = CARD_BY_ID.get(0)

    if fool_data and fool_card:
        print_centered(C.s(C.ACCENT) + "Rendering The Fool with true-color half-blocks..." + RESET)
        print()

        card_str = render_card(
            fool_data["ascii"], fool_data["color_map"],
            fool_card.name, fool_card.name_cn, fool_card.number,
            is_reversed=False, scale=2,
        )
        for line in card_str.split('\n'):
            print_centered(line)
        print()

        print_line(C.GOLD_DIM)
        print()
        print_centered(C.s(C.TEXT_DIM) + "Test complete. Run 'python main.py' for interactive mode." + RESET)
        print()
    else:
        print("ERROR: Could not load card data!")


if __name__ == "__main__":
    main()
