import sys
import os

def main():
    """Main entry point - supports pygame, pyxel, and enhanced pyxel versions"""
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--pyxel':
            # Run basic Pyxel version
            try:
                from game_pyxel import GamePyxel
                import pyxel
                print("Starting Pyxel version...")
                game = GamePyxel()
                pyxel.run(game.update, game.draw)
                return
            except ImportError as e:
                print(f"Error loading Pyxel: {e}")
                print("Falling back to Pygame version...")
        elif sys.argv[1] == '--enhanced':
            # Run enhanced Pyxel version
            try:
                from game_pyxel_enhanced import GamePyxelEnhanced
                import pyxel
                print("Starting Enhanced Pyxel version...")
                game = GamePyxelEnhanced()
                pyxel.run(game.update, game.draw)
                return
            except ImportError as e:
                print(f"Error loading Enhanced Pyxel: {e}")
                print("Falling back to basic Pyxel version...")
                try:
                    from game_pyxel import GamePyxel
                    import pyxel
                    print("Starting basic Pyxel version...")
                    game = GamePyxel()
                    pyxel.run(game.update, game.draw)
                    return
                except ImportError as e2:
                    print(f"Error loading basic Pyxel: {e2}")
                    print("Falling back to Pygame version...")
        elif sys.argv[1] == '--pygame':
            # Force Pygame version
            pass
        else:
            print("Usage: python main.py [--pygame|--pyxel|--enhanced]")
            print("  --pygame:   Run the original Pygame version")
            print("  --pyxel:    Run the basic Pyxel version")
            print("  --enhanced: Run the enhanced Pyxel version with advanced features")
            return
    
    # Default to Pygame version for backward compatibility
    try:
        import pygame
        from game import Game
        print("Starting Pygame version...")
        pygame.init()
        game = Game()
        game.run()
        pygame.quit()
    except ImportError as e:
        print(f"Error loading Pygame: {e}")
        print("Try installing with: pip install pygame")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
