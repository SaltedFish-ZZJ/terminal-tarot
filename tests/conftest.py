"""
测试配置 — 共享的 Mock 对象和 fixtures
"""
from unittest.mock import MagicMock

import pytest

from tarot.interfaces import AIService, TUIEngine


# ═══════════════════════════════════════════════════════════════
#  Mock 对象
# ═══════════════════════════════════════════════════════════════

class MockAI(AIService):
    """Mock AI 服务"""

    def __init__(self):
        self.read_called = False
        self.last_question = None
        self.last_cards = None

    def is_configured(self) -> bool:
        return True

    def read(self, question: str, cards: list[dict], spread_name: str = "单牌指引") -> str:
        self.read_called = True
        self.last_question = question
        self.last_cards = cards
        return f"AI 解读: {question}"

    def read_stream(self, question: str, cards: list[dict], spread_name: str = "单牌指引"):
        """Mock streaming read - yields the same result as read()."""
        self.read_called = True
        self.last_question = question
        self.last_cards = cards
        yield f"AI 解读: {question}"

    def close(self) -> None:
        pass


class MockTUI(TUIEngine):
    """Mock TUI 引擎"""

    def __init__(self):
        self.clear_called = False
        self.printed_texts = []
        self.console = MagicMock()

    def clear(self) -> None:
        self.clear_called = True

    def print(self, *args, **kwargs) -> None:
        self.printed_texts.append(args)

    def print_centered(self, text, style=None) -> None:
        self.printed_texts.append((text, style))

    def print_rule(self, color=None) -> None:
        self.printed_texts.append(("rule", color))

    def get_input(self, prompt: str = "▸ ") -> str:
        return "测试输入"

    def get_centered_input(self, prompt: str = "▸ ") -> str:
        return "测试输入"

    def get_choice(self, prompt: str = "▸ ", valid: list[str] = None) -> str:
        return ""

    def pause(self, msg: str = "按 Enter 继续...", skip_key: str = "") -> bool:
        return False


# ═══════════════════════════════════════════════════════════════
#  Fixtures
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def mock_ai():
    """Mock AI 服务实例"""
    return MockAI()


@pytest.fixture
def mock_tui():
    """Mock TUI 引擎实例"""
    return MockTUI()
