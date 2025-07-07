import random
from map_data import MAP_SIZE

TILE_TYPES = [
    ('.', (194, 178, 128)),  # dirt
    ('~', (210, 180, 140)),  # sand
    ('#', (120, 120, 120)),  # stone
    ('^', (34, 139, 34)),    # grass
    ('o', (70, 130, 180)),   # water
    ('T', (34, 80, 34)),     # tree (dark green)
    ('R', (160, 160, 160)),  # rock (light gray)
]

SYMBOLS = {
    'T': '🌳',  # tree
    'R': '🪨',  # rock
    'o': '🌊',  # water
    '#': '⬛',  # stone
    '~': '░',  # sand
    '^': '▒',  # grass
    '.': ' ',  # dirt
}

class Map:
    def __init__(self):
        self.size = MAP_SIZE
        self.grid, self.colors, self.symbols = self.generate_map()

    def generate_map(self):
        grid = []
        colors = []
        symbols = []
        for y in range(self.size):
            row = []
            color_row = []
            symbol_row = []
            for x in range(self.size):
                if x == 0 or y == 0 or x == self.size-1 or y == self.size-1:
                    tile, color = ('R', (160, 160, 160))  # border is always rock
                else:
                    tile, color = random.choices(
                        TILE_TYPES,
                        weights=[30, 10, 10, 20, 10, 10, 10],
                        k=1
                    )[0]
                row.append(tile)
                color_row.append(color)
                symbol_row.append(SYMBOLS.get(tile, ' '))
            grid.append(row)
            colors.append(color_row)
            symbols.append(symbol_row)
        return grid, colors, symbols

    def is_walkable(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x] not in ('o', '#', 'T', 'R')
        return False

    def move_player(self, player, dx, dy):
        if player.confused > 0 and random.random() < 0.5:
            dx, dy = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        new_x = (player.x + dx) % self.size
        new_y = (player.y + dy) % self.size
        if self.is_walkable(new_x, new_y):
            player.x = new_x
            player.y = new_y
        if player.confused > 0:
            player.confused -= 1
