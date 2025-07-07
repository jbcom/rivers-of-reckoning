import pyxel
from game_pyxel_enhanced import GamePyxelEnhanced

if __name__ == "__main__":
    game = GamePyxelEnhanced()
    pyxel.run(game.update, game.draw)