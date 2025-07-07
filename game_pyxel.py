import pyxel
import random
from player import Player
from enemy import Enemy
from map_data import MAP_SIZE, DIFFICULTY_LEVELS, EVENT_TYPES
from map_pyxel import MapPyxel

class GamePyxel:
    def __init__(self):
        # Pyxel app configuration
        self.WINDOW_WIDTH = 256
        self.WINDOW_HEIGHT = 256
        
        # Initialize Pyxel
        pyxel.init(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, title="First Python RPG")
        
        # Game state
        self.running = True
        self.state = 'feature_select'  # 'feature_select', 'playing', 'paused', 'gameover'
        
        # Features
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
        
        # Game objects
        self.player = None
        self.enemies = []
        self.map = None
        self.event_message = None
        self.event_timer = 0
        
        # Colors (using Pyxel's 16-color palette)
        self.colors = {
            'bg': 0,       # Black
            'text': 7,     # White
            'player': 8,   # Red
            'enemy': 10,   # Green
            'ui': 6,       # Light Blue
            'highlight': 11, # Light Green
        }
        
        # Load initial assets
        self.load_pyxel_assets()
    
    def load_pyxel_assets(self):
        """Load assets for Pyxel - simplified compared to Pygame version"""
        # For now, we'll use simple colored rectangles for sprites
        # Later we can load actual sprite sheets
        pass
    
    def update(self):
        """Main update loop called by Pyxel"""
        if not self.running:
            pyxel.quit()
            return
            
        if self.state == 'feature_select':
            self.update_feature_select()
        elif self.state == 'playing':
            self.update_playing()
        elif self.state == 'paused':
            self.update_paused()
        elif self.state == 'gameover':
            self.update_gameover()
    
    def draw(self):
        """Main draw loop called by Pyxel"""
        pyxel.cls(self.colors['bg'])
        
        if self.state == 'feature_select':
            self.draw_feature_select()
        elif self.state == 'playing':
            self.draw_playing()
        elif self.state == 'paused':
            self.draw_paused()
        elif self.state == 'gameover':
            self.draw_gameover()
    
    def update_feature_select(self):
        """Handle feature selection state"""
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_feature = (self.selected_feature - 1) % len(self.feature_names)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_feature = (self.selected_feature + 1) % len(self.feature_names)
        elif pyxel.btnp(pyxel.KEY_SPACE):
            # Toggle selected feature
            feature_name = self.feature_names[self.selected_feature][1]
            self.features[feature_name] = not self.features[feature_name]
        elif pyxel.btnp(pyxel.KEY_RETURN):
            # Start game
            self.start_game()
            self.state = 'playing'
        elif pyxel.btnp(pyxel.KEY_ESCAPE):
            self.running = False
    
    def draw_feature_select(self):
        """Draw feature selection screen"""
        pyxel.text(self.WINDOW_WIDTH//2 - 30, 20, "FEATURE SELECT", self.colors['text'])
        
        for i, (display_name, feature_name) in enumerate(self.feature_names):
            y = 60 + i * 20
            color = self.colors['highlight'] if i == self.selected_feature else self.colors['text']
            status = "ON" if self.features[feature_name] else "OFF"
            text = f"{display_name}: {status}"
            
            pyxel.text(20, y, text, color)
        
        pyxel.text(20, 160, "UP/DOWN: Select", self.colors['ui'])
        pyxel.text(20, 170, "SPACE: Toggle", self.colors['ui'])
        pyxel.text(20, 180, "ENTER: Start Game", self.colors['ui'])
        pyxel.text(20, 190, "ESC: Quit", self.colors['ui'])
    
    def start_game(self):
        """Initialize game objects"""
        difficulty = 'Easy'  # Default difficulty
        if self.features['difficulty_levels']:
            difficulty = 'Hard'
        
        self.player = Player(difficulty)
        self.map = MapPyxel()
        self.enemies = []
        self.event_message = None
    
    def update_playing(self):
        """Handle playing state"""
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.state = 'paused'
            return
        
        # Handle movement
        dx, dy = 0, 0
        if pyxel.btnp(pyxel.KEY_UP):
            dy = -1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            dy = 1
        elif pyxel.btnp(pyxel.KEY_LEFT):
            dx = -1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            dx = 1
        
        if dx != 0 or dy != 0:
            self.move_player(dx, dy)
        
        # Clear event message after some time
        if self.event_message and self.event_timer > 0:
            self.event_timer -= 1
            if self.event_timer <= 0:
                self.event_message = None
    
    def move_player(self, dx, dy):
        """Move player and handle events"""
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        if self.map.is_walkable(new_x, new_y):
            self.player.move(dx, dy, wrap=True)
            
            # Trigger random event if enabled
            if self.features['random_events'] and random.random() < 0.2:
                event = random.choice(EVENT_TYPES)
                self.event_message = event['desc']
                self.event_timer = 180  # 3 seconds at 60 FPS
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
                self.event_timer = 180
                if self.player.health <= 0:
                    self.state = 'gameover'
    
    def draw_playing(self):
        """Draw playing state"""
        # Draw map
        self.map.draw()
        
        # Draw player
        player_x = self.player.x * (self.WINDOW_WIDTH // MAP_SIZE)
        player_y = self.player.y * (self.WINDOW_HEIGHT // MAP_SIZE)
        pyxel.rect(player_x, player_y, 8, 8, self.colors['player'])
        
        # Draw HUD
        self.draw_hud()
        
        # Draw event message if active
        if self.event_message:
            self.draw_event_message()
    
    def draw_hud(self):
        """Draw heads-up display"""
        # Background bar
        pyxel.rect(0, 0, self.WINDOW_WIDTH, 20, self.colors['ui'])
        
        # Health
        pyxel.text(5, 5, f"HP: {self.player.health}", self.colors['text'])
        
        # Gold
        pyxel.text(80, 5, f"Gold: {self.player.gold}", self.colors['text'])
        
        # Mana
        pyxel.text(150, 5, f"Mana: {self.player.mana}", self.colors['text'])
    
    def draw_event_message(self):
        """Draw event message dialog"""
        # Simple centered text box
        msg_width = len(self.event_message) * 4 + 10
        msg_x = (self.WINDOW_WIDTH - msg_width) // 2
        msg_y = self.WINDOW_HEIGHT // 2 - 20
        
        pyxel.rect(msg_x, msg_y, msg_width, 40, self.colors['ui'])
        pyxel.rectb(msg_x, msg_y, msg_width, 40, self.colors['text'])
        
        # Center the text
        text_x = msg_x + 5
        text_y = msg_y + 15
        pyxel.text(text_x, text_y, self.event_message, self.colors['text'])
    
    def update_paused(self):
        """Handle paused state"""
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.state = 'playing'
        elif pyxel.btnp(pyxel.KEY_Q):
            self.state = 'feature_select'
    
    def draw_paused(self):
        """Draw paused state"""
        # Draw the game state first (dimmed)
        self.draw_playing()
        
        # Draw pause overlay
        pyxel.rect(60, 100, 136, 60, self.colors['ui'])
        pyxel.rectb(60, 100, 136, 60, self.colors['text'])
        
        pyxel.text(100, 110, "PAUSED", self.colors['text'])
        pyxel.text(70, 130, "ESC: Resume", self.colors['text'])
        pyxel.text(70, 140, "Q: Quit to Menu", self.colors['text'])
    
    def update_gameover(self):
        """Handle game over state"""
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = 'feature_select'
        elif pyxel.btnp(pyxel.KEY_ESCAPE):
            self.running = False
    
    def draw_gameover(self):
        """Draw game over state"""
        pyxel.text(self.WINDOW_WIDTH//2 - 30, self.WINDOW_HEIGHT//2 - 20, "GAME OVER", self.colors['text'])
        pyxel.text(self.WINDOW_WIDTH//2 - 40, self.WINDOW_HEIGHT//2, "SPACE: Menu", self.colors['ui'])
        pyxel.text(self.WINDOW_WIDTH//2 - 30, self.WINDOW_HEIGHT//2 + 10, "ESC: Quit", self.colors['ui'])