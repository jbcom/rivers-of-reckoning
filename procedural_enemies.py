import pygame
import os
import random

def load_enemy_spritesheet(path, sprite_size):
    sheet = pygame.image.load(path).convert()
    bg_color = sheet.get_at((0, 0))  # Assume top-left is background
    sheet.set_colorkey(bg_color)
    sheet_w, sheet_h = sheet.get_size()
    sprites = []
    for y in range(0, sheet_h, sprite_size[1]):
        for x in range(0, sheet_w, sprite_size[0]):
            rect = pygame.Rect(x, y, sprite_size[0], sprite_size[1])
            sprite = pygame.Surface(sprite_size, pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), rect)
            sprites.append(sprite)
    return sprites

def tint_surface(surface, tint_color):
    surf = surface.copy().convert_alpha()
    arr = pygame.surfarray.pixels3d(surf)
    r, g, b = tint_color
    arr[..., 0] = (arr[..., 0] * r // 255).astype('uint8')
    arr[..., 1] = (arr[..., 1] * g // 255).astype('uint8')
    arr[..., 2] = (arr[..., 2] * b // 255).astype('uint8')
    del arr
    return surf

def generate_procedural_enemy_sprite(base_surface, color_tint=None, overlay=None, overlay_alpha=128):
    surf = base_surface.copy().convert_alpha()
    if color_tint:
        surf = tint_surface(surf, color_tint)
    if overlay:
        overlay_img = overlay.copy().convert_alpha()
        overlay_img.set_alpha(overlay_alpha)
        surf.blit(overlay_img, (0, 0))
    return surf

def generate_enemy_sprite(enemy_sprites, overlays, variant):
    base = random.choice(enemy_sprites)
    color_tint = None
    overlay_alpha = 128
    overlay_img = None
    if variant == 'red':
        color_tint = (255, 80, 80)
    elif variant == 'blue':
        color_tint = (80, 80, 255)
    elif variant == 'green':
        color_tint = (80, 255, 80)
    elif variant == 'gold':
        color_tint = (255, 220, 80)
    if variant in ['red', 'blue', 'green', 'gold'] and overlays:
        overlay_img = random.choice(overlays)
    surf = base
    if color_tint or overlay_img:
        surf = generate_procedural_enemy_sprite(base, color_tint, overlay_img, overlay_alpha)
    return surf
