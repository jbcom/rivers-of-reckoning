import pyxel
from game_pyxel import GamePyxel

if __name__ == "__main__":
    game = GamePyxel()
    pyxel.run(game.update, game.draw)