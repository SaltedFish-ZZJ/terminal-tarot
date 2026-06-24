"""deck.py 测试 — 78 张牌数据完整性"""
from tarot.deck import TarotCard, ALL_CARDS, CARD_BY_ID, ELEMENT_INFO


def test_all_78_cards():
    assert len(ALL_CARDS) == 78


def test_card_by_id_complete():
    for i in range(78):
        assert i in CARD_BY_ID, f"缺少 card_id={i}"


def test_card_unique_ids():
    ids = [c.id for c in ALL_CARDS]
    assert len(ids) == len(set(ids)), "有重复 id"


def test_card_has_required_fields():
    for card in ALL_CARDS:
        assert isinstance(card, TarotCard)
        assert card.name, f"card {card.id} 缺 name"
        assert card.name_cn, f"card {card.id} 缺 name_cn"
        assert card.number, f"card {card.id} 缺 number"
        assert card.keywords_upright, f"card {card.id} 缺 keywords_upright"
        assert card.keywords_reversed, f"card {card.id} 缺 keywords_reversed"
        assert card.meaning_upright, f"card {card.id} 缺 meaning_upright"
        assert card.meaning_reversed, f"card {card.id} 缺 meaning_reversed"


def test_major_arcana_range():
    """0-21 为大阿尔卡那"""
    for i in range(22):
        card = CARD_BY_ID[i]
        assert card.arcana == "major", f"card {i} 应该是 major"


def test_minor_arcana_range():
    """22-77 为小阿尔卡那"""
    suits = {"wands", "cups", "swords", "pentacles"}
    for i in range(22, 78):
        card = CARD_BY_ID[i]
        assert card.arcana in suits, f"card {i} arcana={card.arcana}"


def test_element_info_exists():
    assert len(ELEMENT_INFO) > 0
    for key, info in ELEMENT_INFO.items():
        assert "name" in info
