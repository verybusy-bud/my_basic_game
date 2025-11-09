#!/usr/bin/env python3
"""
Super Mario & Sonic: Operation Red Shell - Full Text Adventure Game
A Zork-style, menu-driven text adventure game with Cold War parody and crossover humor.
"""

import random
import sys
import time
import os
import json
from datetime import datetime

# --- Utility functions ---
def slowprint(text, delay=0.03):
    """Print text with typewriter effect."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def divider():
    print("\n" + "=" * 70 + "\n")

def choose(options, allow_special=True):
    """Display numbered options and force a valid choice."""
    while True:
        for i, opt in enumerate(options, 1):
            print(f"{i}) {opt}")
        if allow_special:
            print("Type 's' for status, 'l' for location, 'h' for help")
        try:
            choice = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGame interrupted.")
            return None
        
        if allow_special and choice == 's':
            show_status()
            continue
        elif allow_special and choice == 'l':
            show_location()
            continue
        elif allow_special and choice == 'h':
            show_help()
            continue
        elif choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print("Please enter the number of your choice.")

def roll_dice(sides):
    return random.randint(1, sides)

def save_game(slot=None):
    """Save current game state to file slot."""
    if slot is None:
        # Show save slot selection
        return save_to_slot()
    
    save_data = {
        'state': state,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0',
        'slot': slot,
        'summary': {
            'score': state['score'],
            'zones_liberated': state['zones_liberated'],
            'location': state['location'],
            'act': state['act'],
            'mario_hp': state['mario_hp'],
            'sonic_hp': state['sonic_hp']
        }
    }
    
    filename = f'operation_red_shell_save_{slot}.json'
    try:
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        slowprint(f"Game saved to slot {slot} successfully!")
        return True
    except Exception as e:
        slowprint(f"Failed to save game to slot {slot}: {e}")
        return False

def save_to_slot():
    """Show save slot selection and save to chosen slot."""
    slowprint("=== SAVE GAME ===")
    
    # Show existing saves
    for slot in range(1, 4):
        save_info = get_save_info(slot)
        if save_info:
            timestamp = save_info['timestamp'][:19].replace('T', ' ')
            slowprint(f"Slot {slot}: {save_info['summary']['zones_liberated']} zones, {save_info['summary']['score']} points - {timestamp}")
        else:
            slowprint(f"Slot {slot}: Empty")
    
    slowprint("\nSelect a slot to save to:")
    options = ["Slot 1", "Slot 2", "Slot 3", "Cancel"]
    choice = choose(options, allow_special=False)
    
    if choice <= 3:
        slot = choice
        # Check if slot has existing save
        if get_save_info(slot):
            slowprint(f"Slot {slot} already contains a save. Overwrite?")
            confirm_options = ["Yes, overwrite", "No, cancel"]
            confirm = choose(confirm_options, allow_special=False)
            if confirm != 1:
                return False
        
        return save_game(slot)
    
    return False

def get_save_info(slot):
    """Get save information without loading full state."""
    filename = f'operation_red_shell_save_{slot}.json'
    try:
        with open(filename, 'r') as f:
            save_data = json.load(f)
        return save_data
    except FileNotFoundError:
        return None
    except Exception:
        return None

def list_save_slots():
    """Show all available save slots."""
    slowprint("=== LOAD GAME ===")
    available_saves = []
    
    for slot in range(1, 4):
        save_info = get_save_info(slot)
        if save_info:
            timestamp = save_info['timestamp'][:19].replace('T', ' ')
            summary = save_info['summary']
            slowprint(f"Slot {slot}: Act {summary['act']}, {summary['zones_liberated']} zones, {summary['score']} points")
            slowprint(f"         Location: {summary['location']}, HP: {summary['mario_hp']}/{summary['mario_max_hp']}")
            slowprint(f"         Saved: {timestamp}")
            available_saves.append(slot)
        else:
            slowprint(f"Slot {slot}: Empty")
    
    return available_saves

def load_game():
    """Load game state from file slot."""
    available_saves = list_save_slots()
    
    if not available_saves:
        slowprint("No save files found.")
        return False
    
    slowprint("\nSelect a slot to load from:")
    options = []
    for slot in available_saves:
        options.append(f"Slot {slot}")
    options.append("Cancel")
    
    choice = choose(options, allow_special=False)
    
    if choice <= len(available_saves):
        slot = available_saves[choice - 1]
        filename = f'operation_red_shell_save_{slot}.json'
        
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            global state
            state = save_data['state']
            slowprint(f"Game loaded from slot {slot} successfully!")
            return True
        except Exception as e:
            slowprint(f"Failed to load game from slot {slot}: {e}")
            return False
    
    return False

# --- ASCII Art ---
TITLE = r"""
██████╗ ██╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝
██╔══██╗██║   ██║██╔══██╗██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██║  ██║███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
     OPERATION RED SHELL – A TEXT ADVENTURE
      SUPER MARIO & SONIC: COLD WAR CHAOS
"""

RESCUE_ASCII = r"""
     __|__
  --o-----o--  LUIGI & GREEN BERETS
    \   /
     \_/
    /   \
   |     |  HELICOPTER RESCUE
   |_____|
"""

BOWSEROVICH_ASCII = r"""
    /\_/\  BOWSEROVICH
   ( o.o ) SOVIET GENERAL
    > ^ <
   /|   |\
  / |   | \
"""

KREMLIN_CASTLE = r"""
╔══════════════════════════╗
║   ██████╗ ███████╗██████╗  ║
║   ██╔══██╗██╔════╝██╔══██╗ ║
║   ██║  ██║█████╗  ██████╔╝ ║
║   ██║  ██║██╔══╝  ██╔══██╗ ║
║   ██████╔╝███████╗██║  ██║ ║
║   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ║
╚══════════════════════════╝
         KREMLIN CASTLE
"""

GARDEN_ICON = r"""
   _/\_
  (o  o)
   /__\   ~ Mario's Garden ~
"""

SOVIET_OUTPOST = r"""
  /~~~~\   SNOWY OUTPOST
 | RED  |  ╔═════════════╗
 | STAR |  ║ SOVIET     ║
 | PROP  |  ║ OUTPOST    ║
  \~~~~/   ╚═════════════╝
"""

# --- Game state ---
state = {
    "player": "Mario",
    "ally": "Sonic",
    "mario_hp": 15,
    "mario_max_hp": 15,
    "sonic_hp": 10,
    "sonic_max_hp": 10,
    "inventory": [],
    "upgrades": {
        "fireball_level": 1, 
        "spin_booster": False, 
        "jetpack_schematic": False,
        "super_jump": False,
        "chaos_emerald": False
    },
    "score": 0,
    "zones_liberated": 0,
    "location": "garden",
    "act": 1,
    "flags": {
        "met_sonic": False,
        "defeated_first_koopa": False,
        "found_warp_ring": False,
        "defeated_brokov": False,
        "rescue_triggered": False,
        "cliffhanger": False
    }
}

# --- Status and Help Functions ---
def show_status():
    divider()
    print("=== TEAM STATUS ===")
    print(f"Mario: HP {state['mario_hp']}/{state['mario_max_hp']}")
    print(f"Sonic: HP {state['sonic_hp']}/{state['sonic_max_hp']}")
    print(f"Score: {state['score']}")
    print(f"Zones Liberated: {state['zones_liberated']}")
    print(f"Current Act: {state['act']}")
    
    if state['inventory']:
        print(f"Inventory: {', '.join(state['inventory'])}")
    else:
        print("Inventory: Empty")
    
    upgrades = [k.replace('_', ' ').title() for k, v in state['upgrades'].items() if v]
    if upgrades:
        print(f"Upgrades: {', '.join(upgrades)}")
    divider()

def show_location():
    divider()
    print("=== CURRENT LOCATION ===")
    locations = {
        "garden": "Mario's Garden - A peaceful garden under Soviet attack",
        "soviet_outpost": "Soviet Outpost - Snowy military camp with Mushroom decor",
        "red_square": "Red Square - Hybrid Soviet-Mushroom propaganda zone",
        "kremlin_approach": "Kremlin Castle Approach - Final fortress approach",
        "kremlin_throne": "Kremlin Throne Room - Bowserovich's domain"
    }
    print(locations.get(state['location'], "Unknown location"))
    divider()

def show_help():
    divider()
    print("=== GAME HELP ===")
    print("Navigate through numbered choices in menus.")
    print("Special commands:")
    print("  's' - Show team status")
    print("  'l' - Show current location")
    print("  'h' - Show this help")
    print("\nCombat Tips:")
    print("  - Fireballs are effective against armored enemies")
    print("  - Spin Dash requires booster for maximum damage")
    print("  - Team combos can turn the tide of battle")
    print("\nSave your progress anytime during choice prompts!")
    divider()

# --- Combat System ---
def damage_text(dmg):
    return f"({dmg} dmg)" if dmg > 0 else "(miss)"

def attack_enemy(name, hp, attacker, move):
    """Return (new_hp, message, damage_done)"""
    if move == "jump":
        if attacker == "Mario":
            base = 3 if state['upgrades']['super_jump'] else 2
            dmg = roll_dice(6) + base
        else:
            dmg = roll_dice(5) + 1
    elif move == "fireball":
        base = 2 + state['upgrades']['fireball_level']
        dmg = roll_dice(8) + base
    elif move == "spin_dash":
        dmg = roll_dice(7)
        if not state['upgrades']['spin_booster']:
            dmg = max(1, dmg - 3)
    elif move == "bazooka":
        dmg = roll_dice(12) + 8
    elif move == "team_combo":
        dmg = roll_dice(10) + roll_dice(8)
    elif move == "chaos_attack":
        dmg = roll_dice(15) + 10 if state['upgrades']['chaos_emerald'] else roll_dice(8)
    else:
        dmg = 0
    
    hp -= dmg
    msg = f"{attacker} uses {move.replace('_',' ').title()} and hits {name} {damage_text(dmg)}."
    return hp, msg, dmg

def use_item_menu():
    if not state['inventory']:
        slowprint("You have no items to use.")
        return
    
    slowprint("Select an item to use:")
    options = state['inventory'] + ["Cancel"]
    choice = choose(options, allow_special=False)
    
    if choice <= len(state['inventory']):
        item = state['inventory'][choice-1]
        slowprint(f"You use the {item}.")
        
        if item == "Mushroom":
            heal = roll_dice(6) + 4
            state['mario_hp'] = min(state['mario_max_hp'], state['mario_hp'] + heal)
            slowprint(f"Mario recovers {heal} HP!")
            state['inventory'].remove(item)
        elif item == "Ring":
            heal = roll_dice(4) + 3
            state['sonic_hp'] = min(state['sonic_max_hp'], state['sonic_hp'] + heal)
            slowprint(f"Sonic recovers {heal} HP!")
            state['inventory'].remove(item)
        elif item == "Spin Dash Booster":
            state['upgrades']['spin_booster'] = True
            slowprint("Sonic's spin dash is now supercharged!")
            state['inventory'].remove(item)
        elif item == "Fire Flower":
            state['upgrades']['fireball_level'] = min(3, state['upgrades']['fireball_level'] + 1)
            slowprint(f"Fireball upgraded to level {state['upgrades']['fireball_level']}!")
            state['inventory'].remove(item)
        elif item == "Soviet Bazooka Shell":
            slowprint("You save the bazooka shell for a critical moment.")
        elif item == "Red Star Key":
            slowprint("The key glows with Soviet power. Might be useful later.")
        elif item == "Chaos Emerald":
            state['upgrades']['chaos_emerald'] = True
            slowprint("The Chaos Emerald radiates with incredible power!")
            state['inventory'].remove(item)
        else:
            slowprint(f"The {item} doesn't seem to do anything right now.")

# --- Act I: The Invasion Begins ---
def scene_title():
    # Clear screen first
    print("\033[2J\033[H", end="")
    print(TITLE)
    slowprint("Bowser has allied with the Soviets to create the Union of Koopa Socialist Republics!")
    slowprint("Only Mario and Sonic can stop this absurd alliance.")
    slowprint("\nPress Enter to begin your mission...")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        print("\nStarting game automatically...")
        return

def scene_garden():
    state['location'] = "garden"
    slowprint(GARDEN_ICON, 0.002)
    slowprint("Narrator: You're watering suspiciously normal mushrooms when the sky tears open.")
    slowprint("A column of gray smoke, propaganda leaflets, and Koopa paratroopers descend.")
    slowprint('"You never thought you\'d fight Soviet-influenced Koopas in your backyard, but here we are."')
    
    if not state['flags']['met_sonic']:
        slowprint("\nA blue blur streaks past you. It's Sonic!")
        slowprint("Sonic: 'Whoa, this is not what I expected when I took that warp ring!'")
        state['flags']['met_sonic'] = True
    
    options = [
        "Grab Fire Flower and prepare for battle",
        "Hide behind the green pipe",
        "Coordinate with Sonic for a team attack"
    ]
    
    choice = choose(options)
    if choice == 1:
        slowprint("You snatch the Fire Flower — flames dance around your hands.")
        state['inventory'].append("Fire Flower")
        battle_koopa_commando(tutorial=True)
    elif choice == 2:
        slowprint("You hide behind the pipe. Sonic handles the first wave!")
        sonic_vs_koopa_wave()
    else:
        slowprint("You and Sonic exchange a knowing nod. Time for teamwork!")
        battle_koopa_commando(tutorial=True, team_attack=True)

def battle_koopa_commando(tutorial=False, team_attack=False):
    enemy_hp = 8 if tutorial else 10
    enemy_name = "Koopa Commando"
    slowprint(f"\nA {enemy_name} with a red star helmet approaches!")
    
    while enemy_hp > 0 and state['mario_hp'] > 0:
        slowprint(f"\nMario HP: {state['mario_hp']}  Sonic HP: {state['sonic_hp']}  Enemy HP: {enemy_hp}")
        options = [
            "Mario: Jump Attack",
            "Mario: Fireball",
            "Sonic: Spin Dash",
            "Team Combo Attack",
            "Use Item",
            "Inspect Enemy",
            "Run"
        ]
        choice = choose(options)
        
        if choice == 1:
            enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Mario", "jump")
            slowprint(msg)
        elif choice == 2:
            enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Mario", "fireball")
            slowprint(msg)
        elif choice == 3:
            enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Sonic", "spin_dash")
            slowprint(msg)
        elif choice == 4:
            if team_attack or random.random() < 0.6:
                enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Team", "team_combo")
                slowprint(msg)
            else:
                slowprint("The combo fails! Bad timing!")
                state['mario_hp'] -= 2
        elif choice == 5:
            use_item_menu()
            continue
        elif choice == 6:
            slowprint("You inspect the Koopa: wearing Soviet uniform underneath the shell, weak to fire.")
            continue
        else:
            if random.random() < 0.4:
                slowprint("You successfully retreat!")
                return
            else:
                slowprint("You can't escape this fight!")
                state['mario_hp'] -= 1
        
        if enemy_hp > 0:
            dmg = roll_dice(4) + 1
            state['mario_hp'] -= dmg
            slowprint(f"The Koopa Commando counters with Soviet precision! Mario takes {dmg} damage.")
    
    if enemy_hp <= 0:
        slowprint("Koopa Commando defeated! It drops a Red Star Key and Soviet propaganda.")
        state['inventory'].append("Red Star Key")
        state['score'] += 15
        state['flags']['defeated_first_koopa'] = True
        
        if tutorial:
            state['upgrades']['fireball_level'] = 2
            slowprint("Tutorial complete! Fireball upgraded to level 2!")
        
        state['zones_liberated'] += 1
        slowprint("Zone liberated: Mario's Garden (+1 to zones liberated)")
        slowprint("\nWould you like to save your progress?")
        options = ["Save Game", "Continue Without Saving"]
        save_choice = choose(options, allow_special=False)
        if save_choice == 1:
            save_game()
    else:
        if state['mario_hp'] <= 0 and state['sonic_hp'] > 0:
            slowprint("Mario has fallen! Sonic must continue the mission alone!")
            state['player'] = "Sonic"
            state['flags']['mario_down'] = True
            slowprint("Sonic: 'Mario! No! I'll finish this for you!'")
            return
        else:
            slowprint("Both heroes have fallen. The UKSR wins...")
            game_over()

def sonic_vs_koopa_wave():
    slowprint("Sonic springs into action with incredible speed!")
    enemy_hp = 6
    
    while enemy_hp > 0 and state['sonic_hp'] > 0:
        dmg = roll_dice(5) + 2
        enemy_hp -= dmg
        slowprint(f"Sonic spin dashes for {dmg} damage!")
        
        if enemy_hp <= 0:
            break
        
        dmg = roll_dice(3) + 1
        state['sonic_hp'] -= dmg
        slowprint(f"The Koopa hits Sonic for {dmg} damage!")
    
    if enemy_hp <= 0:
        slowprint("Sonic defeats the Koopa wave but you missed the Fire Flower upgrade.")
        state['score'] += 10
    else:
        slowprint("Sonic was defeated! You must continue alone...")
        state['flags']['sonic_defeated'] = True

def scene_warp_discovery():
    slowprint("\nAfter the battle, you discover something strange in the garden...")
    slowprint("A glowing Warp Ring hums with Soviet energy.")
    slowprint('A propaganda poster reads: "1-UP FOR THE MOTHERLAND - JOIN THE UKSR"')
    slowprint('Below it in Koopa-Russian hybrid: "Rurer means VICTORY! Der means THE!"')
    
    options = [
        "Enter the Warp Ring with Sonic",
        "Search the garden for more supplies",
        "Use Red Star Key on the mysterious green pipe"
    ]
    
    choice = choose(options)
    
    if choice == 1:
        state['flags']['found_warp_ring'] = True
        slowprint("You and Sonic jump into the Warp Ring...")
        slowprint("The world warps around you in a blur of red stars and mushrooms!")
        state['act'] = 2
        scene_soviet_outpost()
    elif choice == 2:
        slowprint("You search the garden and find a Mushroom and Ring!")
        state['inventory'].extend(["Mushroom", "Ring"])
        state['score'] += 5
        scene_warp_discovery()
    else:
        if "Red Star Key" in state['inventory']:
            slowprint("You use the Red Star Key on the pipe. It opens revealing a Super Jump feather!")
            state['inventory'].append("Super Jump Feather")
            state['upgrades']['super_jump'] = True
            state['inventory'].remove("Red Star Key")
            state['score'] += 10
        else:
            slowprint("You don't have the Red Star Key yet.")
        scene_warp_discovery()

# --- Act II: Operation Red Shell ---
def scene_soviet_outpost():
    state['location'] = "soviet_outpost"
    slowprint(SOVIET_OUTPOST, 0.002)
    slowprint("\nYou materialize in a snow-swept military encampment.")
    slowprint("Soviet flags adorned with Mushroom symbols flap in the wind.")
    slowprint("A nearby sign reads: 'Rurer = Comrade + Koopa Brother'")
    slowprint("You hear a distorted Soviet march mixed with Mario theme music.")
    
    options = [
        "Sneak through the outpost quietly",
        "Fight your way through the main gate",
        "Search the supply tents first",
        "Try to sabotage the propaganda speakers"
    ]
    
    choice = choose(options)
    
    if choice == 1:
        if random.random() < 0.7:
            slowprint("You successfully sneak past several patrols!")
            state['score'] += 10
            scene_outpost_interior()
        else:
            slowprint("A patrol spots you! Battle begins!")
            battle_soviet_patrol()
    elif choice == 2:
        slowprint("You charge the main gate with Sonic!")
        battle_gate_guards()
    elif choice == 3:
        slowprint("You search the tents and find valuable supplies!")
        state['inventory'].extend(["Spin Dash Booster", "Soviet Rations"])
        state['upgrades']['spin_booster'] = True
        state['score'] += 15
        scene_outpost_interior()
    else:
        slowprint("You blast Soviet-Mario propaganda through the speakers!")
        slowprint("The resulting confusion allows you to slip past!")
        state['score'] += 20
        scene_outpost_interior()

def battle_soviet_patrol():
    enemies = [("Soviet Goomba", 5), ("Red Koopa", 7)]
    
    for name, hp in enemies:
        slowprint(f"\nA {name} attacks!")
        while hp > 0 and state['mario_hp'] > 0:
            slowprint(f"Mario HP: {state['mario_hp']}  Sonic HP: {state['sonic_hp']}  Enemy HP: {hp}")
            options = ["Attack", "Use Item", "Team Attack", "Run"]
            choice = choose(options)
            
            if choice == 1:
                hp, msg, dmg = attack_enemy(name, hp, "Mario", "fireball")
                slowprint(msg)
            elif choice == 2:
                use_item_menu()
                continue
            elif choice == 3:
                hp, msg, dmg = attack_enemy(name, hp, "Team", "team_combo")
                slowprint(msg)
            else:
                slowprint("You retreat from this enemy!")
                break
            
            if hp > 0:
                dmg = roll_dice(4)
                state['mario_hp'] -= dmg
                slowprint(f"The {name} attacks with renewed fury! Mario takes {dmg} damage.")
        
        if state['mario_hp'] <= 0:
            game_over()
    
    slowprint("Patrol defeated! You find a Jetpack Schematic!")
    state['inventory'].append("Jetpack Schematic")
    state['upgrades']['jetpack_schematic'] = True
    state['score'] += 20

def battle_gate_guards():
    slowprint("Two heavily armed Soviet Koopas guard the gate!")
    enemy_hp = 12
    
    while enemy_hp > 0 and state['mario_hp'] > 0:
        slowprint(f"Mario HP: {state['mario_hp']}  Enemy HP: {enemy_hp}")
        options = ["Mario Attack", "Sonic Attack", "Combined Assault", "Use Item"]
        choice = choose(options)
        
        if choice == 1:
            enemy_hp, msg, dmg = attack_enemy("Gate Guards", enemy_hp, "Mario", "fireball")
            slowprint(msg)
        elif choice == 2:
            enemy_hp, msg, dmg = attack_enemy("Gate Guards", enemy_hp, "Sonic", "spin_dash")
            slowprint(msg)
        elif choice == 3:
            enemy_hp, msg, dmg = attack_enemy("Gate Guards", enemy_hp, "Team", "team_combo")
            slowprint(msg)
        else:
            use_item_menu()
            continue
        
        if enemy_hp > 0:
            dmg = roll_dice(5)
            state['mario_hp'] -= dmg
            slowprint(f"The gate guards counterattack with military precision! Mario takes {dmg} damage.")
    
    slowprint("Gate guards defeated! The path is clear!")
    state['score'] += 25

def scene_outpost_interior():
    slowprint("\nYou reach the interior of the Soviet outpost.")
    slowprint("General Hammer Brokov awaits you with his elite guard!")
    
    if not state['flags']['defeated_brokov']:
        battle_general_brokov()
    else:
        slowprint("The outpost is already under your control!")
        scene_red_square()

def battle_general_brokov():
    slowprint("\nGeneral Hammer Brokov: 'You capitalist pigs will never stop the UKSR!'")
    slowprint("General Hammer Brokov: 'We fight for Rurer - der Koopa-Russian dream!'")
    slowprint("He's a massive Hammer Bro in a Soviet general's uniform!")
    
    enemy_hp = 25
    enemy_name = "General Hammer Brokov"
    special_cooldown = 0
    
    while enemy_hp > 0 and state['mario_hp'] > 0:
        slowprint(f"\nMario HP: {state['mario_hp']}  Sonic HP: {state['sonic_hp']}  {enemy_name} HP: {enemy_hp}")
        options = [
            "Mario: Jump Attack",
            "Mario: Fireball",
            "Sonic: Spin Dash",
            "Team: Super Combo",
            "Use Item",
            "Inspect General"
        ]
        choice = choose(options)
        
        if choice == 1:
            enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Mario", "jump")
            slowprint(msg)
        elif choice == 2:
            enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Mario", "fireball")
            slowprint(msg)
        elif choice == 3:
            enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Sonic", "spin_dash")
            slowprint(msg)
        elif choice == 4:
            if random.random() < 0.7:
                enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Team", "team_combo")
                slowprint(msg)
            else:
                slowprint("The combo fails! General Brokov counters!")
                state['mario_hp'] -= 3
        elif choice == 5:
            use_item_menu()
            continue
        else:
            slowprint("General Brokov is winding up for his special attack!")
            continue
        
        if enemy_hp > 0:
            if special_cooldown == 0:
                slowprint("General Brokov unleashes the 'Soviet Hammer Storm'!")
                dmg = roll_dice(8) + 2
                state['mario_hp'] -= dmg
                state['sonic_hp'] -= dmg // 2
                slowprint(f"The devastating hammer storm deals {dmg} damage to Mario and {dmg//2} to Sonic!")
                special_cooldown = 3
            else:
                dmg = roll_dice(5)
                state['mario_hp'] -= dmg
                slowprint(f"The General swings his hammer with surprising force! Mario takes {dmg} damage.")
            
            special_cooldown = max(0, special_cooldown - 1)
    
    if enemy_hp <= 0:
        slowprint("General Hammer Brokov is defeated!")
        slowprint("He drops his Dog Tags, a Soviet Bazooka Shell, and a Chaos Emerald!")
        state['inventory'].extend(["General's Dog Tags", "Soviet Bazooka Shell", "Chaos Emerald"])
        state['score'] += 50
        state['flags']['defeated_brokov'] = True
        state['zones_liberated'] += 1
        slowprint("Zone liberated: Soviet Outpost (+1 to zones liberated)")
        slowprint("\nWould you like to save your progress?")
        options = ["Save Game", "Continue Without Saving"]
        save_choice = choose(options, allow_special=False)
        if save_choice == 1:
            save_game()
        
        scene_red_square()
    else:
        game_over()

def scene_red_square():
    state['location'] = "red_square"
    slowprint("\nYou arrive at Red Square - a bizarre hybrid of Soviet architecture and Mushroom Kingdom elements.")
    slowprint("Goombas march in formation carrying hammers and sickles.")
    slowprint("They chant: 'Rurer! Rurer! Rurer!' in unison.")
    slowprint("Propaganda screens show Bowserovich giving speeches.")
    
    options = [
        "Fight through the square directly",
        "Use Soviet disguise to infiltrate",
        "Cause a diversion with Sonic's speed",
        "Find the underground resistance"
    ]
    
    choice = choose(options)
    
    if choice == 1:
        slowprint("You fight your way through propaganda-filled Red Square!")
        battle_red_square_forces()
    elif choice == 2:
        if "General's Dog Tags" in state['inventory']:
            slowprint("Using General Brokov's dog tags, you bluff your way past guards!")
            state['score'] += 30
        else:
            slowprint("Without proper disguise, you're quickly spotted!")
            battle_red_square_forces()
    elif choice == 3:
        slowprint("Sonic creates a blue blur of confusion, allowing you to slip past!")
        state['score'] += 25
    else:
        slowprint("You find Toad leading an underground resistance movement!")
        slowprint("Toad: 'Mario! We've been waiting for you! Here, take this!'")
        state['inventory'].extend(["Mushroom", "Fire Flower"])
        state['score'] += 20
    
    state['act'] = 3
    scene_kremlin_approach()

def battle_red_square_forces():
    enemies = [("Propaganda Goomba", 4), ("Soviet Shy Guy", 6), ("Red Koopa Troopa", 8)]
    
    for name, hp in enemies:
        slowprint(f"\nA {name} blocks your path!")
        while hp > 0 and state['mario_hp'] > 0:
            slowprint(f"Mario HP: {state['mario_hp']}  Enemy HP: {hp}")
            options = ["Attack", "Sonic Assist", "Use Item"]
            choice = choose(options)
            
            if choice == 1:
                hp, msg, dmg = attack_enemy(name, hp, "Mario", "fireball")
                slowprint(msg)
            elif choice == 2:
                hp, msg, dmg = attack_enemy(name, hp, "Sonic", "spin_dash")
                slowprint(msg)
            else:
                use_item_menu()
                continue
            
            if hp > 0:
                dmg = roll_dice(4)
                state['mario_hp'] -= dmg
                slowprint(f"The {name} attacks with Soviet determination! Mario takes {dmg} damage.")
        
        if state['mario_hp'] <= 0:
            game_over()
    
    slowprint("Red Square forces defeated! The path to Kremlin Castle is open!")
    state['score'] += 40

# --- Act III: The Kremlin Castle ---
def scene_kremlin_approach():
    state['location'] = "kremlin_approach"
    slowprint(KREMLIN_CASTLE, 0.002)
    slowprint("\nYou approach the massive Kremlin Castle - a terrifying fusion of Soviet architecture and Bowser's fortress.")
    slowprint("Hybrid Soviet-Koopa enemies patrol the walls: Shy Guys with Kalashnikovs, Goombas in ushankas.")
    slowprint("The air crackles with dark energy from Bowserovich's Dimensional Warp Array.")
    
    if state['mario_hp'] < state['mario_max_hp'] // 2:
        slowprint("You're wounded. Sonic looks concerned.")
        options = [
            "Use healing items before proceeding",
            "Push forward despite injuries",
            "Try to find a secret entrance"
        ]
        choice = choose(options)
        
        if choice == 1:
            use_item_menu()
        elif choice == 3:
            slowprint("Sonic spots a weakened section of the castle wall!")
            state['score'] += 15
    
    slowprint("The castle gates open. Bowserovich awaits you on his throne!")
    scene_final_boss()

def scene_final_boss():
    slowprint("\n" + BOWSEROVICH_ASCII)
    slowprint("Bowserovich: 'So, the capitalist plumber and his blue pet have arrived!'")
    slowprint("Bowserovich: 'The Union of Koopa Socialist Republics will crush you!'")
    slowprint("Bowserovich: 'In our language, Rurer means unstoppable force! Der means ultimate!'")
    slowprint("Bowserovich: 'Prepare to face the power of Soviet Koopa technology!'")
    
    enemy_hp = 40
    enemy_name = "Bowserovich"
    phase = 1
    special_cooldown = 0
    
    while enemy_hp > 0 and state['mario_hp'] > 0:
        slowprint(f"\nMario HP: {state['mario_hp']}  Sonic HP: {state['sonic_hp']}  {enemy_name} HP: {enemy_hp}")
        
        if phase == 1 and enemy_hp < 25:
            slowprint("Bowserovich: 'You're stronger than I thought! Time for Phase 2!'")
            slowprint("Bowserovich activates his Soviet Jetpack!")
            phase = 2
        elif phase == 2 and enemy_hp < 10:
            slowprint("Bowserovich: 'Impossible! I'll destroy this entire castle!'")
            slowprint("The Dimensional Warp Array begins to overload!")
            phase = 3
        
        options = [
            "Mario: Ultimate Fireball",
            "Sonic: Chaos Spin Dash",
            "Team: Final Combo Attack",
            "Use Soviet Bazooka Shell",
            "Use Item",
            "Try to disable the Warp Array"
        ]
        choice = choose(options)
        
        if choice == 1:
            enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Mario", "fireball")
            slowprint(msg)
        elif choice == 2:
            enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Sonic", "chaos_attack")
            slowprint(msg)
        elif choice == 3:
            if random.random() < 0.8:
                enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Team", "team_combo")
                slowprint(msg)
            else:
                slowprint("The combo fails! Bowserovich counters fiercely!")
                state['mario_hp'] -= 5
        elif choice == 4 and "Soviet Bazooka Shell" in state['inventory']:
            enemy_hp, msg, dmg = attack_enemy(enemy_name, enemy_hp, "Mario", "bazooka")
            slowprint(msg)
            state['inventory'].remove("Soviet Bazooka Shell")
        elif choice == 5:
            use_item_menu()
            continue
        else:
            slowprint("You attempt to disable the Warp Array but Bowserovich stops you!")
            state['mario_hp'] -= 3
        
        if enemy_hp > 0:
            if phase == 1:
                dmg = roll_dice(6) + 2
                slowprint("Bowserovich unleashes devastating Soviet fire!")
            elif phase == 2:
                dmg = roll_dice(8) + 3
                slowprint("Bowserovich performs a Jetpack Hammer Strike!")
            else:
                dmg = roll_dice(10) + 5
                slowprint("Bowserovich unleashes Desperate Soviet Fury!")
            
            state['mario_hp'] -= dmg
            slowprint(f"The devastating attack deals {dmg} damage to Mario!")
            
            if phase >= 2:
                sonic_dmg = dmg // 2
                state['sonic_hp'] -= sonic_dmg
                slowprint(f"Sonic takes {sonic_dmg} splash damage from the attack!")
    
    if enemy_hp <= 0:
        scene_rescue_and_cliffhanger()
    else:
        game_over()

def scene_rescue_and_cliffhanger():
    slowprint("\n" + RESCUE_ASCII)
    slowprint("Bowserovich is defeated! But as he falls, he activates the Dimensional Warp Array!")
    slowprint("Bowserovich: 'You may have won this battle, but the UKSR will rise again!'")
    slowprint("Bowserovich: 'Rurer never dies! It only transforms!'")
    slowprint("A mysterious Soviet scientist appears: 'Comrade Bowser, this way!'")
    slowprint("They leap into a dimensional rift just as Luigi and the Green Berets arrive by helicopter!")
    
    slowprint("\nLuigi: 'Mama mia! We were too late to help with the fighting!'")
    slowprint("Green Beret Commander: 'Good work, soldiers. But this isn't over.'")
    slowprint("The rift snaps shut, but you can hear Bowser's laughter echoing from another dimension...")
    
    state['flags']['cliffhanger'] = True
    state['flags']['rescue_triggered'] = True
    state['zones_liberated'] += 1
    state['score'] += 100
    slowprint("Zone liberated: Kremlin Castle (+1 to zones liberated)")
    slowprint("\nWould you like to save your progress?")
    options = ["Save Game", "Continue Without Saving"]
    save_choice = choose(options, allow_special=False)
    if save_choice == 1:
        save_to_slot()
    
    slowprint("\n=== MISSION COMPLETE ===")
    slowprint(f"Final Score: {state['score']}")
    slowprint(f"Zones Liberated: {state['zones_liberated']}")
    slowprint(f"Final Mario HP: {state['mario_hp']}/{state['mario_max_hp']}")
    slowprint(f"Final Sonic HP: {state['sonic_hp']}/{state['sonic_max_hp']}")
    
    if state['score'] >= 300:
        slowprint("Rank: SUPER STAR - You're a true hero of the Mushroom Kingdom!")
    elif state['score'] >= 200:
        slowprint("Rank: HERO - Excellent work saving the world!")
    elif state['score'] >= 100:
        slowprint("Rank: VETERAN - Good job, but room for improvement!")
    else:
        slowprint("Rank: SURVIVOR - You made it through, but try for better results!")
    
    slowprint("\n=== TO BE CONTINUED... ===")
    slowprint("Bowser and the Soviet scientist have escaped to another dimension!")
    slowprint("What new adventures await Mario and Sonic in Operation Red Shell 2?")
    
    # Save final game state
    save_to_slot()
    slowprint("\nGame saved! Thank you for playing Operation Red Shell!")

def game_over():
    slowprint("\n=== GAME OVER ===")
    slowprint("The Union of Koopa Socialist Republics has won...")
    slowprint(f"Final Score: {state['score']}")
    slowprint("The Mushroom Kingdom falls under Soviet control.")
    slowprint("\nWould you like to:")
    options = ["Load a saved game", "Start a new game", "Quit"]
    choice = choose(options)
    
    if choice == 1:
        if load_game():
            return True
    elif choice == 2:
        reset_game()
        return True
    elif choice == 3:
        slowprint("Thanks for playing Operation Red Shell!")
        sys.exit(0)

def main_game_loop():
    if state['act'] == 1:
        if not state['flags']['defeated_first_koopa']:
            scene_garden()
            scene_warp_discovery()
        else:
            scene_warp_discovery()
    elif state['act'] == 2:
        if not state['flags']['defeated_brokov']:
            scene_soviet_outpost()
        else:
            scene_red_square()
    elif state['act'] == 3:
        scene_kremlin_approach()
    else:
        scene_rescue_and_cliffhanger()

def reset_game():
    """Reset game state to starting values."""
    global state
    state = {
        "player": "Mario",
        "ally": "Sonic",
        "mario_hp": 15,
        "mario_max_hp": 15,
        "sonic_hp": 10,
        "sonic_max_hp": 10,
        "inventory": [],
        "upgrades": {
            "fireball_level": 1, 
            "spin_booster": False, 
            "jetpack_schematic": False,
            "super_jump": False,
            "chaos_emerald": False
        },
        "score": 0,
        "zones_liberated": 0,
        "location": "garden",
        "act": 1,
        "flags": {
            "met_sonic": False,
            "defeated_first_koopa": False,
            "found_warp_ring": False,
            "defeated_brokov": False,
            "rescue_triggered": False,
            "cliffhanger": False
        }
    }

def main_menu():
    while True:
        # Clear screen first
        print("\033[2J\033[H", end="")
        print(TITLE)
        slowprint("=== MAIN MENU ===")
        options = [
            "Start New Game",
            "Load Saved Game",
            "View Instructions",
            "Quit"
        ]
        choice = choose(options, allow_special=False)
        
        if choice == 1:
            reset_game()
            return True
        elif choice == 2:
            if load_game():
                return True
        elif choice == 3:
            show_help()
            input("\nPress Enter to return to main menu...")
        else:
            slowprint("Thanks for playing Operation Red Shell!")
            sys.exit(0)

def main():
    try:
        while main_menu():
            scene_title()
            main_game_loop()
    except KeyboardInterrupt:
        print('\n\nGame interrupted. Thanks for playing!')
    except Exception as e:
        print(f'\nAn error occurred: {e}')
        print('Saving game state...')
        save_game()

if __name__ == '__main__':
    main()