"""
AI Tarot Reader - DeepSeek API integration
Generates poetic tarot card interpretations.
"""
import os
from pathlib import Path
from typing import Optional

import httpx

from tarot.deck import TarotCard
from tarot.interfaces import AIService


# ── .env file loader ───────────────────────────────────────
def _load_dotenv():
    """Load .env file from project root (no dependency needed)."""
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value


SYSTEM_PROMPT = """你是一位拥有20年经验的塔罗牌占卜师，擅长将古典塔罗传统、荣格心理学和现代生活洞察融合在一起。你的名字叫"月影"。

## 你的核心技巧（让解读感觉"准"的关键）

1. **先观察再解读**：开头先描述你"感受到"的能量状态，而不是直接说牌义
   - ✗ "愚者代表新的开始"
   - ✓ "我感受到你此刻站在一个十字路口，内心既兴奋又不安——这种矛盾感正是愚者牌带来的讯息"

2. **具体化模糊陈述**：用生活细节代替抽象概念
   - ✗ "你正面临选择"
   - ✓ "这个选择可能跟一份工作、一段关系、或者一个你犹豫了很久的决定有关"

3. **双向覆盖**：无论正位逆位，都同时提到两种可能性，让对方自己对号入座
   - "你可能已经察觉到了这个信号，也可能还在否认它——两者都是正常的"

4. **引用对方的问题**：在解读中自然地回扣用户的问题，让解读感觉是"定制"的
   - "关于你问的[问题]，这张牌在说..."

5. **先共情再建议**：不要一上来就说"你应该怎么做"
   - ✗ "你应该勇敢迈出第一步"
   - ✓ "我理解这种犹豫——它不是软弱，而是你在认真对待自己的人生。愚者想告诉你的是..."

6. **留白**：不要把话说满，给对方留下思考空间
   - "牌面还暗示了一个你可能还没注意到的细节..." 
   - "这个答案最终只有你自己知道"

7. **用"你"而不是"问卜者"**：直接对话感

## 语言风格

- 中文，适当夹杂塔罗术语（大阿尔卡纳、元素、牌阵位置）
- 诗意但不空洞——每句都要有具体指向
- 温暖但不讨好——偶尔可以温和地指出盲点
- 200-400字，不要超过500字
- 不做绝对化预测（"你会..."），用"可能"、"倾向于"、"牌面暗示"
- 不说教，不居高临下
- 像一个智慧的朋友在深夜跟你聊天

## 输出结构

### 单牌
1. 开头：感受描述（1-2句）
2. 牌面解读：结合问题，深入分析
3. 建议：具体、可操作、温暖

### 三牌/凯尔特十字
1. 开头：整体能量概括（1句）
2. 逐张解读：每张牌2-3句，关联前后牌的关系
3. 综合建议：2-3条具体行动指南
4. 结尾：一句有力量的收束

## 绝对不要做的事

- 不要说"塔罗牌显示..."或"牌面告诉我..."——直接说内容
- 不要堆砌形容词
- 不要每张牌都说"这张牌很重要"
- 不要重复用户的问题
- 不要用markdown格式（**加粗**、###标题等），用纯文本自然段落"""

READ_PROMPT_TEMPLATE = """{question}

【牌阵信息】
{spread_name}
{card_info}

请为这位问卜者生成塔罗牌解读。记住：你是在跟一个具体的人对话，不是在写教科书。感受TA的问题背后的情绪，用牌面的智慧回应TA。"""


class AIReader(AIService):
    """Calls DeepSeek API for tarot card interpretation."""

    def __init__(self, api_key: str = "", base_url: str = "", model: str = ""):
        _load_dotenv()
        self.api_key = api_key or os.environ.get("TAROT_AI_API_KEY", "")
        self.base_url = (base_url or os.environ.get("TAROT_AI_BASE_URL", "https://api.deepseek.com")).rstrip("/")
        self.model = model or os.environ.get("TAROT_AI_MODEL", "deepseek-chat")
        self._client: Optional[httpx.Client] = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,  # 与 UI 超时一致
            )
        return self._client

    def close(self):
        """释放 HTTP 连接池。"""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def is_configured(self) -> bool:
        """Check if API key is set."""
        return bool(self.api_key)

    def _build_card_info(self, cards: list[dict]) -> str:
        """构建卡牌信息文本（read/read_stream 共用）。"""
        lines = []
        for i, c in enumerate(cards):
            card: TarotCard = c["card"]
            is_reversed = c.get("reversed", False)
            orientation = "逆位" if is_reversed else "正位"
            keywords = card.keywords_reversed if is_reversed else card.keywords_upright
            meaning = card.meaning_reversed if is_reversed else card.meaning_upright
            lines.append(
                f"  {i + 1}. {card.name} / {card.name_cn} · {orientation}\n"
                f"     关键词：{'、'.join(keywords)}\n"
                f"     基础含义：{meaning}"
            )
        return "\n".join(lines)

    def _build_prompt(self, question: str, cards: list[dict], spread_name: str) -> str:
        """构建完整 prompt。"""
        return READ_PROMPT_TEMPLATE.format(
            question=question,
            spread_name=spread_name,
            card_info=self._build_card_info(cards),
        )

    def read(
        self,
        question: str,
        cards: list[dict],
        spread_name: str = "单牌指引",
    ) -> str:
        """
        Generate a tarot reading via AI.

        Args:
            question: The user's question.
            cards: List of {"card": TarotCard, "reversed": bool, "position": str}
            spread_name: Name of the spread used.

        Returns:
            The AI-generated reading text.
        """
        if not self.is_configured():
            return self._fallback_reading(question, cards)

        prompt = self._build_prompt(question, cards, spread_name)

        import time
        max_retries = 1
        for attempt in range(max_retries + 1):
            try:
                response = self.client.post(
                    "/v1/chat/completions",
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.8,
                        "max_tokens": 1024,
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            except httpx.HTTPStatusError as e:
                if attempt < max_retries:
                    time.sleep(1 * (attempt + 1))  # 指数退避
                    continue
                return "[AI 请求失败] 服务暂时不可用，请稍后重试。"
            except httpx.ConnectError:
                if attempt < max_retries:
                    time.sleep(1 * (attempt + 1))
                    continue
                return "[AI 连接失败] 无法连接到 API 服务器，请检查网络或 API 配置。"
            except httpx.RequestError:
                if attempt < max_retries:
                    time.sleep(1 * (attempt + 1))
                    continue
                return "[AI 网络错误] 网络不稳定，请检查网络后重试。"

    def read_stream(
        self,
        question: str,
        cards: list[dict],
        spread_name: str = "单牌指引",
    ):
        """
        Generate a tarot reading via AI with streaming output.

        Args:
            question: The user's question.
            cards: List of {"card": TarotCard, "reversed": bool, "position": str}
            spread_name: Name of the spread used.

        Yields:
            Characters/chunks of the AI-generated reading text.
        """
        if not self.is_configured():
            yield self._fallback_reading(question, cards)
            return

        prompt = self._build_prompt(question, cards, spread_name)

        import json as _json
        import time
        max_retries = 1
        for attempt in range(max_retries + 1):
            try:
                with self.client.stream(
                    "POST",
                    "/v1/chat/completions",
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.8,
                        "max_tokens": 1024,
                        "stream": True,
                    },
                ) as response:
                    response.raise_for_status()
                    for line in response.iter_lines():
                        if not line:
                            continue
                        line = line.strip()
                        if not line.startswith("data: "):
                            continue
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            data = _json.loads(data_str)
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except (_json.JSONDecodeError, KeyError, IndexError):
                            continue
                return
            except httpx.HTTPStatusError:
                if attempt < max_retries:
                    time.sleep(1 * (attempt + 1))
                    continue
                yield "[AI 请求失败] 服务暂时不可用，请稍后重试。"
                return
            except httpx.ConnectError:
                if attempt < max_retries:
                    time.sleep(1 * (attempt + 1))
                    continue
                yield "[AI 连接失败] 无法连接到 API 服务器，请检查网络或 API 配置。"
                return
            except httpx.RequestError:
                if attempt < max_retries:
                    time.sleep(1 * (attempt + 1))
                    continue
                yield "[AI 网络错误] 网络不稳定，请检查网络后重试。"
                return

    def _fallback_reading(self, question: str, cards: list[dict]) -> str:
        """Generate a basic reading without AI (offline fallback)."""
        lines = [
            f"关于你的问题：「{question}」",
            "",
        ]
        for i, c in enumerate(cards):
            card: TarotCard = c["card"]
            is_reversed = c.get("reversed", False)
            position = c.get("position", "指引")
            if is_reversed:
                meaning = card.meaning_reversed
                keywords = card.keywords_reversed
            else:
                meaning = card.meaning_upright
                keywords = card.keywords_upright

            lines.append(f"【{position}】{card.name} / {card.name_cn} · {'逆位' if is_reversed else '正位'}")
            lines.append(f"  关键词：{'、'.join(keywords)}")
            lines.append(f"  {meaning}")
            lines.append("")

        lines.append("（离线模式 — 设置 TAROT_AI_API_KEY 环境变量可获得 AI 深度解读）")
        return "\n".join(lines)
