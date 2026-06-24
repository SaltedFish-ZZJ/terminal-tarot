"""
Terminal Tarot - 接口定义
定义模块间依赖的抽象接口，降低耦合度。
"""
from abc import ABC, abstractmethod
from typing import Optional


class AIService(ABC):
    """AI 服务接口 — 定义 AI 读取解读的标准方法。"""

    @abstractmethod
    def is_configured(self) -> bool:
        """检查 AI 服务是否已配置。"""
        ...

    @abstractmethod
    def read(
        self,
        question: str,
        cards: list[dict],
        spread_name: str = "单牌指引",
    ) -> str:
        """
        生成塔罗牌解读。

        Args:
            question: 用户问题
            cards: 卡牌列表 [{"card": TarotCard, "reversed": bool, "position": str}]
            spread_name: 牌阵名称

        Returns:
            解读文本
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """释放资源。"""
        ...


class TUIEngine(ABC):
    """TUI 引擎接口 — 定义终端 UI 的标准方法。"""

    @abstractmethod
    def clear(self) -> None:
        """清屏。"""
        ...

    @abstractmethod
    def print(self, *args, **kwargs) -> None:
        """打印文本。"""
        ...

    @abstractmethod
    def print_centered(self, text, style=None) -> None:
        """居中打印文本。"""
        ...

    @abstractmethod
    def print_rule(self, color=None) -> None:
        """打印分隔线。"""
        ...

    @abstractmethod
    def get_input(self, prompt: str = "▸ ") -> Optional[str]:
        """获取用户输入。"""
        ...

    @abstractmethod
    def get_centered_input(self, prompt: str = "▸ ") -> Optional[str]:
        """获取居中的用户输入。"""
        ...

    @abstractmethod
    def get_choice(self, prompt: str = "▸ ", valid: list[str] = None) -> Optional[str]:
        """获取用户选择。"""
        ...

    @abstractmethod
    def pause(self, msg: str = "按 Enter 继续...", skip_key: str = "") -> bool:
        """暂停等待用户输入。"""
        ...
