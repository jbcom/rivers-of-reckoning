import curses

MAP_SIZE = 11

ENEMY_TYPES = [
    {'name': 'Goblin', 'hp_mod': 0, 'dmg_mod': 0, 'effect': None},
    {'name': 'Orc', 'hp_mod': 2, 'dmg_mod': 1, 'effect': 'rage'},
    {'name': 'Slime', 'hp_mod': -2, 'dmg_mod': -1, 'effect': 'split'},
    {'name': 'Wraith', 'hp_mod': 0, 'dmg_mod': 0, 'effect': 'curse'},
]

EVENT_TYPES = [
    {'name': 'Treasure', 'desc': 'You found a hidden stash! +5 gold.', 'effect': lambda p: setattr(p, 'gold', p.gold+5)},
    {'name': 'Trap', 'desc': 'A trap! Lose 3 HP.', 'effect': lambda p: p.take_damage(3)},
    {'name': 'Wandering Merchant', 'desc': 'A merchant offers a random item.', 'effect': None},
]

ACHIEVEMENTS = [
    {'name': 'First Blood', 'desc': 'Defeat your first enemy.'},
    {'name': 'Boss Slayer', 'desc': 'Defeat both bosses.'},
    {'name': 'Potion Master', 'desc': 'Use 5 potions.'},
    {'name': 'Explorer', 'desc': 'Reveal the entire map.'},
    {'name': 'Untouchable', 'desc': 'Win without dying once.'},
]

DIRECTIONS = {
    curses.KEY_UP: (0, -1, 'North'),
    curses.KEY_DOWN: (0, 1, 'South'),
    curses.KEY_LEFT: (-1, 0, 'West'),
    curses.KEY_RIGHT: (1, 0, 'East'),
}

SPRITES = {
    'player': '@',
    'enemy': 'E',
    'empty': '.',
    'tree': 'T',
    'rock': 'O',
    'potion': 'P',
    'fog': ' ',
    'treasure': '$',
    'trap': '^',
    'merchant': 'M',
}

PROP_LOCATIONS = set()
POTION_LOCATIONS = set()
for i in range(3, MAP_SIZE, 3):
    PROP_LOCATIONS.add((i, i))
    PROP_LOCATIONS.add((i, (MAP_SIZE - i) % MAP_SIZE))
for i in range(2, MAP_SIZE, 4):
    if (i, MAP_SIZE - i - 1) not in PROP_LOCATIONS and (i, MAP_SIZE - i - 1) != (0, 0):
        POTION_LOCATIONS.add((i, MAP_SIZE - i - 1))

DIFFICULTY_LEVELS = {
    'Easy': {
        'max_health': 10,
        'overheal_penalty': False,
        'enemy_health_scale': 0.7,
        'enemy_damage_scale': 0.7,
        'confusion': False,
    },
    'Hard': {
        'max_health': 10,
        'overheal_penalty': True,
        'enemy_health_scale': 1.5,
        'enemy_damage_scale': 1.5,
        'confusion': True,
    },
}

SHOP_ITEMS = [
    {'name': 'Sword', 'cost': 3, 'desc': '+1 attack damage (upgrades stack)', 'effect': 'sword'},
    {'name': 'Shield', 'cost': 3, 'desc': '-1 enemy damage (upgrades stack)', 'effect': 'shield'},
    {'name': 'Boots', 'cost': 2, 'desc': 'Negate confusion effect (upgrades: +1 gold per enemy)', 'effect': 'boots'},
    {'name': 'Potion', 'cost': 1, 'desc': 'Heal 3 HP instantly', 'effect': 'potion'},
]

BOSS_SPRITES = [
    [
        "   /\\/\\   ",
        "  ( o  o )  ",
        "  (  --  )  ",
        "  /|    |\\ ",
        "   | || |   "
    ],
    [
        "   /\_/\   ",
        "  ( >_< )  ",
        "  (  ==  ) ",
        "  /|    |\ ",
        "   | || |  "
    ],
    [
        "   /\_/\   ",
        "  ( o_o )  ",
        "  (  vv  ) ",
        "  /|    |\ ",
        "   | || |  "
    ]
]

BOSS_NAMES = ["Dread Hydra", "Shadow Golem", "Chaos Drake"]
