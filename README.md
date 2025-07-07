# First Python RPG

A sophisticated 2D Role-Playing Game built with Pygame, featuring turn-based combat, magic spells, equipment upgrades, boss battles, and multiple difficulty levels. This is a fully-featured RPG with procedural map generation, achievement system, and rich sprite-based graphics.

## Game Features

### Core Gameplay
- **2D Movement**: Full directional movement with arrow keys across procedurally generated maps
- **Turn-Based Combat**: Strategic combat system with various enemy types and abilities
- **Magic System**: Cast spells including Heal, Shield, Stun, Poison, and Mana Regeneration
- **Equipment Upgrades**: Upgrade swords, shields, and boots through the shop system
- **Boss Battles**: Epic encounters with unique boss enemies featuring ASCII art
- **Achievement System**: Unlock achievements like "First Blood", "Boss Slayer", and "Untouchable"

### RPG Systems
- **Experience & Leveling**: Gain experience points and level up your character
- **Gold & Shop**: Earn gold to purchase equipment upgrades and healing potions
- **Inventory Management**: Collect and manage various items and weapons
- **Difficulty Levels**: Choose between Easy and Hard modes with different penalties
- **Random Events**: Encounter treasure, traps, and wandering merchants

### Technical Features
- **Rich Graphics**: Animated character sprites with idle, running, jumping, and combat animations
- **Audio System**: Background music and sound effects
- **Procedural Generation**: Optional procedural map generation for varied gameplay
- **Asset Management**: Comprehensive sprite and audio asset system

## Installation & Setup

### Requirements
- Python 3.12 or higher
- Pygame library
- Audio system (for background music)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jbcom/first-python-rpg.git
   cd first-python-rpg
   ```

2. **Install dependencies**:
   ```bash
   pip install pygame
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## Controls & Gameplay

### Movement
- **Arrow Keys**: Move character in four directions (Up, Down, Left, Right)
- **Wrapping**: Character wraps around map edges (configurable)

### Combat
- **A**: Attack enemy
- **S**: Cast spell
- **Number Keys**: Select specific spells or items
- **Q**: Quit/Return to previous menu

### Menu Navigation
- **Number Keys**: Select menu options
- **Enter**: Confirm selection
- **ESC/Q**: Exit menus

### Shop System
- **1-4**: Purchase items (Sword, Shield, Boots, Potions)
- **0**: Exit shop

## Game Mechanics

### Combat System
- **Health Points**: Start with 10 HP (varies by difficulty)
- **Mana Points**: Used for casting spells
- **Damage Calculation**: Based on weapon level and enemy strength
- **Status Effects**: Poison, stun, confusion, and blocking

### Spell System
- **Heal**: Restore 4 HP (2 mana)
- **Shield Up**: Block next attack (3 mana)
- **Stun**: Disable enemy for 1 turn (3 mana)
- **Poison**: Deal damage over time (2 mana)
- **Mana Regen**: Restore mana once per encounter

### Difficulty Levels
- **Easy**: 10 HP, no overheal penalty, reduced enemy stats
- **Hard**: 10 HP, overheal confusion penalty, increased enemy stats

### Enemy Types
- **Goblin**: Basic enemy with standard stats
- **Orc**: Higher health and damage with rage ability
- **Slime**: Lower stats but splits when defeated
- **Wraith**: Applies curse effects

## File Structure

```
first-python-rpg/
├── main.py              # Game entry point
├── game.py              # Core game logic and Pygame management
├── player.py            # Player class with stats, spells, equipment
├── enemy.py             # Enemy classes and combat logic
├── boss.py              # Boss battle mechanics
├── shop.py              # Shop system implementation
├── map.py               # Map generation and management
├── map_data.py          # Game constants, difficulty levels, achievements
├── assets_map.py        # Asset loading and management
├── procedural_enemies.py # Procedural enemy generation
├── utils.py             # Utility functions
├── images/              # Sprite assets
│   ├── character/       # Player animations
│   ├── weapons/         # Weapon sprites
│   ├── objects/         # Item and object sprites
│   └── enemies.png      # Enemy spritesheet
├── music/               # Audio files
│   └── bgm.mp3         # Background music
└── test_*.py           # Test files
```

## Development & Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest

# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_game_logic.py -v
```

### Asset Management
The game uses a comprehensive asset system that automatically loads and scales sprites based on the defined scale factor. All assets are managed through `assets_map.py`.

## Features Overview

| Feature | Description |
|---------|-------------|
| **Graphics** | Sprite-based 2D graphics with animations |
| **Audio** | Background music and sound effects |
| **Combat** | Turn-based combat with various enemy types |
| **Magic** | 5 different spells with mana system |
| **Equipment** | Upgradeable weapons, shields, and boots |
| **Shop** | Gold-based economy with item purchases |
| **Bosses** | Special boss encounters with unique mechanics |
| **Achievements** | 5 different achievements to unlock |
| **Difficulty** | Easy and Hard modes with different penalties |
| **Procedural** | Optional procedural map generation |

## Contributing

This project demonstrates advanced Python game development concepts including:
- Object-oriented game design
- Pygame graphics and audio integration
- Turn-based combat systems
- Asset management and loading
- Game state management
- Event-driven programming

Enjoy exploring this comprehensive RPG implementation!
