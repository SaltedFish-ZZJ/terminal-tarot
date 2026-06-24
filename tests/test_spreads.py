"""spreads.py 测试 — 牌阵定义"""
from tarot.spreads import SPREADS, CELTIC_CROSS, SINGLE, THREE_CARD


def test_spreads_exist():
    assert "single" in SPREADS
    assert "three_card" in SPREADS
    assert "celtic_cross" in SPREADS


def test_single_spread():
    assert SINGLE["name_cn"] == "单牌指引"
    assert len(SINGLE["positions"]) == 1


def test_three_spread():
    assert len(THREE_CARD["positions"]) == 3


def test_celtic_cross_spread():
    assert len(CELTIC_CROSS["positions"]) == 10
    assert SPREADS["celtic_cross"] is CELTIC_CROSS


def test_position_has_fields():
    for spread in SPREADS.values():
        for pos in spread["positions"]:
            assert hasattr(pos, "name")
            assert hasattr(pos, "name_cn")
