"""Card pixel art registry - all 78 cards."""
from tarot.cards.fool import FOOL_ART, FOOL_COLOR_MAP
from tarot.cards.major_arcana_part1 import MAJOR_ARCANA_ART
from tarot.cards.major_arcana_part2 import MAJOR_ARCANA_ART_12_21
from tarot.cards.minor_arcana import MINOR_ARCANA_ART

# Merge all card art into one registry
# Format: card_id -> {"ascii": [...], "color_map": {...}}
CARD_ART = {}

# Fool (card 0) - has its own dedicated file
CARD_ART[0] = {"ascii": FOOL_ART, "color_map": FOOL_COLOR_MAP}

# Major Arcana 1-11
for card_id, (ascii_art, palette) in MAJOR_ARCANA_ART.items():
    CARD_ART[card_id] = {"ascii": ascii_art, "color_map": palette}

# Major Arcana 12-21
for card_id, (ascii_art, palette) in MAJOR_ARCANA_ART_12_21.items():
    CARD_ART[card_id] = {"ascii": ascii_art, "color_map": palette}

# Minor Arcana 22-77 (all 56 cards)
for card_id, (ascii_art, palette) in MINOR_ARCANA_ART.items():
    CARD_ART[card_id] = {"ascii": ascii_art, "color_map": palette}
