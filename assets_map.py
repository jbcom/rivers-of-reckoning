# assets_map.py
# This file maps logical asset names to their file paths for use in pygame.
# It is auto-generated from the images directory structure.

import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), 'images')

ASSETS = {
    # Character animations
    'character': {
        'idle': [os.path.join(ASSET_DIR, 'character', f'idle_{i}.png') for i in range(4)],
        'run': [os.path.join(ASSET_DIR, 'character', f'run_{i}.png') for i in range(6)],
        'jump': [os.path.join(ASSET_DIR, 'character', f'jump_{i}.png') for i in range(4)],
        'swim': [os.path.join(ASSET_DIR, 'character', f'swim_{i}.png') for i in range(6)],
        'attack': [os.path.join(ASSET_DIR, 'character', f'attack_{i}.png') for i in range(4)],
        'x': [os.path.join(ASSET_DIR, 'character', f'x_{i}.png') for i in range(4)],
    },
    # Objects
    'objects': {
        'advance_lens': os.path.join(ASSET_DIR, 'objects', 'advance lens.png'),
        'drill': os.path.join(ASSET_DIR, 'objects', 'drill.png'),
        'fast_sailing': os.path.join(ASSET_DIR, 'objects', 'fast sailing.png'),
        'gift_box': os.path.join(ASSET_DIR, 'objects', 'gift box.png'),
        'mount_reins': os.path.join(ASSET_DIR, 'objects', 'Mount reins.png'),
        'oil_tank': os.path.join(ASSET_DIR, 'objects', 'oil tank.png'),
        'protection_crystal': os.path.join(ASSET_DIR, 'objects', 'protection crystal.png'),
        'quality_grain': os.path.join(ASSET_DIR, 'objects', 'quality grain.png'),
        'research_journal': os.path.join(ASSET_DIR, 'objects', 'Research Journal.png'),
        'ship_structure': os.path.join(ASSET_DIR, 'objects', 'Ship structure.png'),
        'super_charge_drum': os.path.join(ASSET_DIR, 'objects', 'super charge drum.png'),
        'super_pet_food': os.path.join(ASSET_DIR, 'objects', 'Super pet food.png'),
        'treasure_map': os.path.join(ASSET_DIR, 'objects', 'Treasure map.png'),
        'weapon_box': os.path.join(ASSET_DIR, 'objects', 'weapon box.png'),
        'wrist_equipment_box': os.path.join(ASSET_DIR, 'objects', 'Wrist equipment box.png'),
    },
    # Weapons
    'weapons': {
        '2hsword': os.path.join(ASSET_DIR, 'weapons', 'w_2hsword.png'),
        'axe_unknow': os.path.join(ASSET_DIR, 'weapons', 'w_axe_unknow.png'),
        'axe_winged': os.path.join(ASSET_DIR, 'weapons', 'w_axe_winged.png'),
        'dagger02': os.path.join(ASSET_DIR, 'weapons', 'w_dagger02.png'),
        'halberd': os.path.join(ASSET_DIR, 'weapons', 'w_halberd.png'),
        'katana': os.path.join(ASSET_DIR, 'weapons', 'w_katana.png'),
        'katana_diamond': os.path.join(ASSET_DIR, 'weapons', 'w_katana_diamond.png'),
        'katana_fire': os.path.join(ASSET_DIR, 'weapons', 'w_katana_fire.png'),
        'katana_holly': os.path.join(ASSET_DIR, 'weapons', 'w_katana_holly.png'),
        'katana_wooden': os.path.join(ASSET_DIR, 'weapons', 'w_katana_wooden.png'),
        'longsword02': os.path.join(ASSET_DIR, 'weapons', 'w_longsword02.png'),
        'mace': os.path.join(ASSET_DIR, 'weapons', 'w_mace.png'),
        'mace_copper': os.path.join(ASSET_DIR, 'weapons', 'w_mace_copper.png'),
        'mace_dark': os.path.join(ASSET_DIR, 'weapons', 'w_mace_dark.png'),
        'mace_diamond': os.path.join(ASSET_DIR, 'weapons', 'w_mace_diamond.png'),
        'mace_fire': os.path.join(ASSET_DIR, 'weapons', 'w_mace_fire.png'),
        'mace_holly': os.path.join(ASSET_DIR, 'weapons', 'w_mace_holly.png'),
        'mace_ice': os.path.join(ASSET_DIR, 'weapons', 'w_mace_ice.png'),
        'sabre': os.path.join(ASSET_DIR, 'weapons', 'w_sabre.png'),
        'shortsword02': os.path.join(ASSET_DIR, 'weapons', 'w_shortsword02.png'),
        'spear': os.path.join(ASSET_DIR, 'weapons', 'w_spear.png'),
        'sword_roman_ruby': os.path.join(ASSET_DIR, 'weapons', 'w_sword_roman ruby.png'),
        'sword_roman': os.path.join(ASSET_DIR, 'weapons', 'w_sword_roman.png'),
        'sword_roman_blood': os.path.join(ASSET_DIR, 'weapons', 'w_sword_roman_blood.png'),
        'sword_roman_dark': os.path.join(ASSET_DIR, 'weapons', 'w_sword_roman_dark.png'),
        'sword_roman_diamond': os.path.join(ASSET_DIR, 'weapons', 'w_sword_roman_diamond.png'),
        'sword_roman_holly': os.path.join(ASSET_DIR, 'weapons', 'w_sword_roman_holly.png'),
        'sword_roman_lightning': os.path.join(ASSET_DIR, 'weapons', 'w_sword_roman_lightning.png'),
        'trident': os.path.join(ASSET_DIR, 'weapons', 'w_trident.png'),
    },
    # Map
    'map': os.path.join(ASSET_DIR, 'map.png'),
}
