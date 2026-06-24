"""log.py 测试 — 读牌记录"""
import json
import os
import tempfile
from unittest.mock import patch

from tarot.log import save_reading, get_recent_readings, get_reading_count, _prune_old_readings, MAX_READINGS


def _mock_card():
    """创建最小 mock card dict"""

    class FakeCard:
        name = "The Fool"
        name_cn = "愚者"
        id = 0

    return {"card": FakeCard(), "reversed": False, "position": "指引"}


def test_save_and_read():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        path = f.name

    try:
        with patch('tarot.log.LOG_FILE', path):
            ts = save_reading("测试问题", [_mock_card()], "单牌指引", "测试解读")
            assert ts

            readings = get_recent_readings(10)
            assert len(readings) >= 1
            assert readings[-1]["question"] == "测试问题"

            count = get_reading_count()
            assert count >= 1
    finally:
        os.unlink(path)


def test_prune_keeps_max():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        path = f.name

    try:
        # 写入超过 MAX_READINGS 条
        with open(path, 'w', encoding='utf-8') as f:
            for i in range(MAX_READINGS + 50):
                f.write(json.dumps({"i": i}, ensure_ascii=False) + "\n")

        with patch('tarot.log.LOG_FILE', path):
            _prune_old_readings()

        with open(path, 'r', encoding='utf-8') as f:
            lines = [l for l in f if l.strip()]
        assert len(lines) == MAX_READINGS

        # 验证保留的是最新的
        first = json.loads(lines[0])
        assert first["i"] == 50  # 前 50 条被裁掉
    finally:
        os.unlink(path)
