import random
import time
import winsound
from .map_data import BOSS_SPRITES, BOSS_NAMES

def boss_screen(stdscr, player, boss_num, boss_strength, boss_health):
    boss_idx = boss_num - 1
    boss_art = BOSS_SPRITES[boss_idx]
    boss_name = BOSS_NAMES[boss_idx]
    max_y, max_x = stdscr.getmaxyx()
    boss_cur_health = boss_health
    message = f"Boss Fight: {boss_name}!"
    boss_ability_cd = 3
    boss_ability = None
    while boss_cur_health > 0 and player.health > 0:
        stdscr.clear()
        for i, line in enumerate(boss_art):
            stdscr.addstr(max_y//2 - 4 + i, max_x//2 - len(line)//2, line)
        stdscr.addstr(max_y//2 + 2, max_x//2 - 10, f"Boss HP: {boss_cur_health}")
        stdscr.addstr(max_y//2 + 3, max_x//2 - 10, f"Your HP: {player.health}  Mana: {player.mana}")
        stdscr.addstr(max_y//2 + 5, max_x//2 - 10, message)
        stdscr.addstr(max_y//2 + 7, max_x//2 - 10, "[A]ttack  [S]pell  [Q]uit")
        stdscr.refresh()
        key = stdscr.getch()
        if key in (ord('a'), ord('A')):
            dmg = random.randint(2, 4) + player.sword_level
            boss_cur_health -= dmg
            message = f"You attack for {dmg}!"
        elif key in (ord('s'), ord('S')):
            stdscr.addstr(max_y//2 + 9, max_x//2 - 10, "Select Spell:")
            spell_choices = [i for i in player.spell_unlocks]
            for i in spell_choices:
                spell = player.spells[i]
                stdscr.addstr(max_y//2 + 10 + i, max_x//2 - 10, f"{i+1}. {spell['name']} ({spell['cost']} MP): {spell['desc']}")
            stdscr.refresh()
            skey = stdscr.getch()
            if skey in [ord(str(i+1)) for i in spell_choices]:
                idx = int(chr(skey)) - 1
                message = player.use_spell(idx, type('Boss', (), {'health': boss_cur_health}))
                if 'Fireball' in message:
                    boss_cur_health -= int(message.split()[-2])
        elif key in (ord('q'), ord('Q')):
            break
        boss_ability_cd -= 1
        if boss_ability_cd <= 0:
            if boss_idx == 0:
                bdmg = random.randint(2, 4) + boss_strength
                player.take_damage(bdmg)
                player.take_damage(bdmg//2)
                message += f" Hydra lashes twice! {bdmg} and {bdmg//2} damage!"
            elif boss_idx == 1:
                boss_ability = 'shielded'
                message += " Golem shields itself (half damage next turn)!"
            elif boss_idx == 2:
                bdmg = random.randint(4, 8) + boss_strength
                player.take_damage(bdmg)
                message += f" Drake breathes fire! {bdmg} damage!"
            boss_ability_cd = 3
        if boss_cur_health > 0:
            if player.block_next:
                message += " You blocked the boss's attack!"
                player.block_next = False
            else:
                bdmg = random.randint(3, 6) + boss_strength
                if boss_ability == 'shielded':
                    bdmg //= 2
                    boss_ability = None
                player.take_damage(bdmg)
                message += f" Boss hits you for {bdmg}!"
        player.mana = min(player.max_mana, player.mana + 1)
        winsound.Beep(600, 100)
        time.sleep(0.5)
    if boss_cur_health <= 0:
        player.bosses_defeated += 1
    return boss_cur_health <= 0
