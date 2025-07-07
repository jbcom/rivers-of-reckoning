#!/usr/bin/env python3
"""Test script to verify Pyxel game logic without GUI"""

import sys

def test_game_pyxel_import():
    """Test that we can import the Pyxel game modules"""
    try:
        from first_python_rpg.map import MapPyxel
        print("✓ MapPyxel imported successfully")
        
        # Test map generation
        map_obj = MapPyxel()
        print(f"✓ Map generated with size {map_obj.size}x{map_obj.size}")
        
        # Test walkability
        walkable_count = 0
        for y in range(map_obj.size):
            for x in range(map_obj.size):
                if map_obj.is_walkable(x, y):
                    walkable_count += 1
        print(f"✓ Map has {walkable_count} walkable tiles")
        
        return True
    except Exception as e:
        print(f"✗ Error importing MapPyxel: {e}")
        return False

def test_game_logic():
    """Test game logic without GUI"""
    try:
        from first_python_rpg.player import Player
        from first_python_rpg.enemy import Enemy
        from first_python_rpg.map_data import MAP_SIZE, DIFFICULTY_LEVELS
        
        # Test player creation
        player = Player()
        print(f"✓ Player created with health {player.health}")
        
        # Test enemy creation  
        enemy = Enemy()
        print(f"✓ Enemy created: {enemy.name}")
        
        # Test map constants
        print(f"✓ Map size: {MAP_SIZE}")
        print(f"✓ Difficulty levels: {list(DIFFICULTY_LEVELS.keys())}")
        
        return True
    except Exception as e:
        print(f"✗ Error in game logic test: {e}")
        return False

def main():
    print("Testing Pyxel game components...")
    
    success = True
    success &= test_game_pyxel_import()
    success &= test_game_logic()
    
    if success:
        print("\n✓ All tests passed! Pyxel migration is working correctly.")
    else:
        print("\n✗ Some tests failed.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)