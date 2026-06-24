"""
Session Log - Simple JSON-based reading history.
Saves each reading to a local log file.
"""
import json
import os
from datetime import datetime
from pathlib import Path

# Store in project's data/ directory (D: drive) instead of C:\Users\~\.tarot-cli
LOG_DIR = str(Path(__file__).resolve().parent.parent / "data")
LOG_FILE = os.path.join(LOG_DIR, "readings.jsonl")
MAX_READINGS = 200  # 最多保留条数，超出自动清理旧记录

# ── 条目缓存（mtime + entries） ──
_cache_mtime: float = 0
_cache_entries: list[dict] = []


def ensure_log_dir():
    """Create log directory if it doesn't exist."""
    os.makedirs(LOG_DIR, exist_ok=True)


def _read_all_entries() -> list[dict]:
    """读取全部条目（带 mtime 缓存）。"""
    global _cache_mtime, _cache_entries

    if not os.path.exists(LOG_FILE):
        return []

    mtime = os.path.getmtime(LOG_FILE)
    if mtime == _cache_mtime and _cache_entries:
        return _cache_entries

    entries: list[dict] = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    _cache_mtime = mtime
    _cache_entries = entries
    return entries


def save_reading(
    question: str,
    cards: list[dict],
    spread_name: str,
    reading_text: str,
) -> str:
    """
    Save a reading to the log file.

    Args:
        question: The user's question.
        cards: List of card data used.
        spread_name: Name of the spread.
        reading_text: The AI-generated reading.

    Returns:
        The timestamp ID of this reading.
    """
    ensure_log_dir()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "timestamp": timestamp,
        "question": question,
        "spread": spread_name,
        "cards": [
            {
                "name": c["card"].name,
                "name_cn": c["card"].name_cn,
                "reversed": c.get("reversed", False),
                "position": c.get("position", ""),
            }
            for c in cards
        ],
        "reading": reading_text,
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 使缓存失效
    global _cache_mtime, _cache_entries
    _cache_mtime = 0
    _cache_entries = []

    _prune_old_readings()

    return timestamp


def _prune_old_readings():
    """保留最近 MAX_READINGS 条，清理多余旧记录。单次遍历完成。"""
    if not os.path.exists(LOG_FILE):
        return

    # 用 deque 单次遍历，只保留最后 MAX_READINGS 行
    from collections import deque
    kept: deque[str] = deque(maxlen=MAX_READINGS)
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                kept.append(line)

    if len(kept) < MAX_READINGS:
        return  # 未超限，无需写回

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(kept)

    # 使缓存失效
    global _cache_mtime, _cache_entries
    _cache_mtime = 0
    _cache_entries = []


def get_recent_readings(limit: int = 10) -> list[dict]:
    """Get the most recent readings from the log."""
    ensure_log_dir()
    entries = _read_all_entries()
    return entries[-limit:][::-1]


def get_reading_count() -> int:
    """Get total number of readings in the log."""
    ensure_log_dir()
    return len(_read_all_entries())
