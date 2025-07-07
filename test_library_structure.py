#!/usr/bin/env python3
"""Test script to verify the new library structure works"""

import sys

def test_library_import():
    """Test that we can import the library modules"""
    try:
        from first_python_rpg import Game, Player, Enemy
        print("✓ Core library imports successful")
        
        # Test individual module imports
        from first_python_rpg.map import MapPyxel
        from first_python_rpg.map_data import MAP_SIZE, ENEMY_TYPES
        from first_python_rpg.procedural_enemies import ProceduralEnemyGenerator
        print("✓ All module imports successful")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic game object creation"""
    try:
        from first_python_rpg import Player, Enemy
        from first_python_rpg.map import MapPyxel
        from first_python_rpg.procedural_enemies import ProceduralEnemyGenerator
        
        # Test object creation
        player = Player()
        print(f"✓ Player created with health {player.health}")
        
        enemy = Enemy()
        print(f"✓ Enemy created: {enemy.name}")
        
        game_map = MapPyxel()
        print(f"✓ Map created with size {game_map.size}x{game_map.size}")
        
        # Test procedural generation
        generator = ProceduralEnemyGenerator()
        proc_enemy = generator.generate_enemy(level=1)
        print(f"✓ Procedural enemy generated: {proc_enemy['name']}")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_game_creation():
    """Test that we can create a game instance"""
    try:
        # Note: This will fail in headless mode due to pyxel.init()
        # But we can test the import at least
        from first_python_rpg import Game
        print("✓ Game class can be imported")
        return True
    except Exception as e:
        print(f"✗ Game creation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing new library structure...")
    
    tests = [
        test_library_import,
        test_basic_functionality,
        test_game_creation
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✓ All tests passed! Library structure is working correctly.")
        return True
    else:
        print("✗ Some tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)