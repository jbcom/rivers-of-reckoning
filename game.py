import pygame
import os
import random
from procedural_enemies import load_enemy_spritesheet, generate_enemy_sprite, generate_procedural_enemy_sprite
from assets_map import ASSETS
from player import Player
from enemy import Enemy
from map_data import MAP_SIZE, DIFFICULTY_LEVELS, EVENT_TYPES
from map import Map

class Game:
    def __init__(self, test_mode=False):
        self.SCALE = 1.5
        self.WINDOW_WIDTH = 960
        self.WINDOW_HEIGHT = 960
        self.screen = None
        self.clock = None
        self.FONT = None
        self.running = True
        self.features = {
            'random_events': False,
            'difficulty_levels': False,
            'enemy_encounters': False,
        }
        self.selected_feature = 0
        self.feature_names = [
            ('Random Events', 'random_events'),
            ('Difficulty Levels', 'difficulty_levels'),
            ('Enemy Encounters', 'enemy_encounters'),
        ]
        self.PRELOADED = None
        self.ENEMY_SPRITES = None
        self.overlays = None
        self.player = None
        self.enemies = []
        self.map = None
        self.event_message = None
        self.event_timer = 0
        self.test_mode = test_mode
        # Always set state to 'playing' in test_mode, and skip all pygame init
        if self.test_mode:
            self.state = 'playing'
        else:
            self.state = 'feature_select'
            self.init_pygame()
            self.load_assets()

    def init_pygame(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont("consolas", int(28 * self.SCALE))

    def load_assets(self):
        # Load and scale all assets
        def load_scaled(img, size):
            surf = pygame.image.load(img)
            if surf.get_alpha() is not None or surf.get_masks()[3] != 0:
                surf = surf.convert_alpha()
            else:
                surf = surf.convert()
            return pygame.transform.smoothscale(surf, size)
        PLAYER_SIZE = (int(60 * self.SCALE), int(60 * self.SCALE))
        ENEMY_SIZE = (int(56 * self.SCALE), int(56 * self.SCALE))
        MAP_TILE_SIZE = (int(64 * self.SCALE), int(64 * self.SCALE))
        INVENTORY_ICON_SIZE = (int(40 * self.SCALE), int(40 * self.SCALE))
        WEAPON_ICON_SIZE = (int(32 * self.SCALE), int(32 * self.SCALE))
        self.PRELOADED = {
            'character': {k: [load_scaled(f, PLAYER_SIZE) for f in v] for k, v in ASSETS['character'].items()},
            'character_enemy': {k: [load_scaled(f, ENEMY_SIZE) for f in v] for k, v in ASSETS['character'].items()},
            'objects': {k: load_scaled(v, MAP_TILE_SIZE) for k, v in ASSETS['objects'].items()},
            'objects_inv': {k: load_scaled(v, INVENTORY_ICON_SIZE) for k, v in ASSETS['objects'].items()},
            'weapons': {k: load_scaled(v, WEAPON_ICON_SIZE) for k, v in ASSETS['weapons'].items()},
            'map': pygame.transform.smoothscale(pygame.image.load(ASSETS['map']).convert(), (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)),
        }
        self.ENEMY_SPRITES = load_enemy_spritesheet(os.path.join('images', 'enemies.png'), ENEMY_SIZE)
        self.overlays = list(self.PRELOADED['objects'].values()) + list(self.PRELOADED['weapons'].values())

    def run(self):
        if self.test_mode:
            return  # Do nothing in test mode
        while self.running:
            if self.state == 'feature_select':
                self.feature_select()
            elif self.state == 'playing':
                self.start_game()
                self.playing()
            elif self.state == 'paused':
                self.paused()
            elif self.state == 'gameover':
                self.gameover()

    def feature_select(self):
        dialog_font = pygame.font.SysFont("consolas", 20)
        dialog_width, dialog_height = 640, 480
        self.screen = pygame.display.set_mode((dialog_width, dialog_height), pygame.FULLSCREEN)
        option_height = dialog_font.get_height() + 16
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.VIDEORESIZE:
                    dialog_width, dialog_height = event.w, event.h
                    self.screen = pygame.display.set_mode((dialog_width, dialog_height), pygame.FULLSCREEN)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_feature = (self.selected_feature + 1) % len(self.feature_names)
                    elif event.key == pygame.K_UP:
                        self.selected_feature = (self.selected_feature - 1) % len(self.feature_names)
                    elif event.key == pygame.K_SPACE:
                        label, key = self.feature_names[self.selected_feature]
                        self.features[key] = not self.features[key]
                    elif event.key == pygame.K_RETURN:
                        selecting = False
                        self.state = 'playing'
            self.screen.fill((30, 30, 60))
            title = dialog_font.render("Select Features to Enable (SPACE to toggle, ENTER to start):", True, (255,255,0))
            title_rect = title.get_rect(center=(dialog_width//2, 40))
            self.screen.blit(title, title_rect)
            y_start = 80
            for idx, (label, key) in enumerate(self.feature_names):
                status = "ON" if self.features[key] else "OFF"
                color = (0,255,0) if self.features[key] else (255,0,0)
                txt = dialog_font.render(f"[{status}] {label}", True, color)
                txt_rect = txt.get_rect(center=(dialog_width//2, y_start + idx * option_height))
                self.screen.blit(txt, txt_rect)
                if idx == self.selected_feature:
                    pygame.draw.rect(self.screen, (255,255,255), (txt_rect.left-8, txt_rect.top-4, txt_rect.width+16, txt_rect.height+8), 2)
            instruct = dialog_font.render("Use UP/DOWN to select, SPACE to toggle, ENTER to start", True, (200,200,200))
            instruct_rect = instruct.get_rect(center=(dialog_width//2, y_start + len(self.feature_names) * option_height + 30))
            self.screen.blit(instruct, instruct_rect)
            pygame.display.flip()

    def start_game(self):
        # Initialize player and map for a new game
        difficulty = 'Easy'
        if self.features['difficulty_levels']:
            difficulty = 'Hard'  # For demo, just toggle between Easy/Hard
        self.player = Player(difficulty)
        self.map = Map()
        self.enemies = []  # No enemies on map at start

    def playing(self):
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.FULLSCREEN)
        tile_size = int(64 * self.SCALE)
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.load('music/bgm.mp3')
                pygame.mixer.music.play(-1)
            except Exception:
                pass
        while self.state == 'playing' and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if self.event_message:
                        self.event_message = None
                        continue
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'paused'
                    elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        dx, dy = 0, 0
                        if event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                        elif event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        # Use map.move_player for all movement logic
                        self.map.move_player(self.player, dx, dy)
                        # Trigger random event if enabled
                        if self.features['random_events'] and random.random() < 0.2:
                            event = random.choice(EVENT_TYPES)
                            self.event_message = event['desc']
                            if event['effect']:
                                event['effect'](self.player)
                            if self.player.health <= 0:
                                self.state = 'gameover'
                        # Trigger enemy encounter if enabled
                        elif self.features['enemy_encounters'] and random.random() < 0.2:
                            enemy = Enemy(strength=random.randint(1, 3))
                            dmg = random.randint(1, enemy.strength)
                            self.player.take_damage(dmg)
                            self.event_message = f"Enemy Encounter! Took {dmg} damage from a {enemy.name}."
                            if self.player.health <= 0:
                                self.state = 'gameover'
            self.screen.fill((0, 0, 0))
            # Draw procedurally generated map tiles
            for y in range(self.map.size):
                for x in range(self.map.size):
                    rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
                    color = self.map.colors[y][x]
                    pygame.draw.rect(self.screen, color, rect)
                    # Draw symbol overlay for trees, rocks, water
                    symbol = self.map.symbols[y][x]
                    if symbol not in (' ', '\u2591', '\u2592'):
                        font = pygame.font.SysFont("segoeuiemoji,symbola,consolas", int(tile_size*0.8))
                        txt = font.render(symbol, True, (0,0,0))
                        txt_rect = txt.get_rect(center=rect.center)
                        self.screen.blit(txt, txt_rect)
            # Draw player
            px, py = self.player.x, self.player.y
            player_img = self.PRELOADED['character']['idle'][0]
            self.screen.blit(player_img, (px*tile_size, py*tile_size))
            # Draw HUD as a fixed always-on-top bar
            hud_height = 40
            hud_surf = pygame.Surface((self.WINDOW_WIDTH, hud_height))
            hud_surf.fill((30, 30, 60))
            pygame.draw.rect(hud_surf, (255,255,0), hud_surf.get_rect(), 2)
            hud_font = pygame.font.SysFont("consolas", 24)
            health_txt = hud_font.render(f"HP: {self.player.health}", True, (255,0,0))
            gold_txt = hud_font.render(f"Gold: {self.player.gold}", True, (255, 215, 0))
            mana_txt = hud_font.render(f"Mana: {self.player.mana}", True, (0, 200, 255))
            hud_surf.blit(health_txt, (10, 8))
            hud_surf.blit(gold_txt, (150, 8))
            hud_surf.blit(mana_txt, (300, 8))
            self.screen.blit(hud_surf, (0, 0))
            # Draw event dialog if needed
            if self.event_message:
                dialog_font = pygame.font.SysFont("consolas", 28)
                dialog_surf = pygame.Surface((self.WINDOW_WIDTH//2, 100))
                dialog_surf.fill((30,30,60))
                pygame.draw.rect(dialog_surf, (255,255,0), dialog_surf.get_rect(), 3)
                msg = dialog_font.render(self.event_message, True, (255,255,255))
                msg_rect = msg.get_rect(center=(dialog_surf.get_width()//2, dialog_surf.get_height()//2))
                dialog_surf.blit(msg, msg_rect)
                self.screen.blit(dialog_surf, (self.WINDOW_WIDTH//4, self.WINDOW_HEIGHT//2-50))
            pygame.display.flip()
            self.clock.tick(60)

    def paused(self):
        paused_font = pygame.font.SysFont("consolas", 40)
        menu_font = pygame.font.SysFont("consolas", 28)
        menu_options = ["Resume", "Feature Select", "Quit Game"]
        selected = 0
        paused = True
        while paused and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'playing'
                        paused = False
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:  # Resume
                            self.state = 'playing'
                            paused = False
                        elif selected == 1:  # Feature Select
                            self.state = 'feature_select'
                            paused = False
                        elif selected == 2:  # Quit Game
                            self.running = False
                            return
            self.screen.fill((20, 20, 40))
            txt = paused_font.render("PAUSED", True, (255,255,0))
            txt_rect = txt.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 - 80))
            self.screen.blit(txt, txt_rect)
            for i, option in enumerate(menu_options):
                color = (255,255,255) if i == selected else (180,180,180)
                opt_txt = menu_font.render(option, True, color)
                opt_rect = opt_txt.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 + i*50))
                self.screen.blit(opt_txt, opt_rect)
                if i == selected:
                    pygame.draw.rect(self.screen, (255,255,0), opt_rect.inflate(20,10), 2)
            instruct = menu_font.render("Use UP/DOWN, ENTER to select, ESC to resume", True, (200,200,200))
            instruct_rect = instruct.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 + 180))
            self.screen.blit(instruct, instruct_rect)
            pygame.display.flip()
            self.clock.tick(30)

    def gameover(self):
        over_font = pygame.font.SysFont("consolas", 40)
        over = True
        while over and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = 'feature_select'
                        over = False
            self.screen.fill((60, 20, 20))
            txt = over_font.render("GAME OVER", True, (255,0,0))
            txt_rect = txt.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2))
            self.screen.blit(txt, txt_rect)
            instruct = over_font.render("Press ENTER to restart", True, (255,255,255))
            instruct_rect = instruct.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2+60))
            self.screen.blit(instruct, instruct_rect)
            pygame.display.flip()
            self.clock.tick(30)

    def move_player(self, dx, dy):
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        if self.map.is_walkable(new_x, new_y):
            self.player.move(dx, dy, wrap=self.features['procedural_map'])
            # Trigger random event if enabled
            if self.features['random_events'] and random.random() < 0.2:
                from map_data import EVENT_TYPES
                event = random.choice(EVENT_TYPES)
                self.event_message = event['desc']
                if event['effect']:
                    event['effect'](self.player)
                if self.player.health <= 0:
                    self.state = 'gameover'
            # Trigger enemy encounter if enabled
            elif self.features['enemy_encounters'] and random.random() < 0.2:
                from enemy import Enemy
                enemy = Enemy(strength=random.randint(1, 3))
                dmg = random.randint(1, enemy.strength)
                self.player.take_damage(dmg)
                self.event_message = f"Enemy Encounter! Took {dmg} damage from a {enemy.name}."
                if self.player.health <= 0:
                    self.state = 'gameover'

game = Game()
game.run()
pygame.quit()
