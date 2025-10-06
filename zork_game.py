import sys
import random

def print_mario_level(position):
    levels = [
        "Mario @ ~~~~~ [pit] ~~~~~ [pipe]",
        "Mario ~~~~~ @ ~~~~~ [pit] ~~~~~ [pipe]",
        "Mario ~~~~~ [pit] ~~~~~ @ ~~~~~ [pipe]",
        "Mario ~~~~~ [pit] ~~~~~ [pipe] ~~~~~ @"
    ]
    print(levels[position])

def main():
    print("You are standing in an open field west of a white house, with a boarded front door.")
    print("There is a small mailbox here.")
    location = "field"
    mailbox_opened = False
    leaflet_read = False
    inventory = []
    door_locked = True
    has_key = False
    riddle_solved = False
    in_mario = False
    mario_position = 0
    mario_level = ["ground", "pit", "ground", "pipe"]
    verbose = False
    troll_defeated = False

    insults = [
        "Nice try, but that's not a command!",
        "Even a troll would do better than that.",
        "Are you typing with your elbows?",
        "That's not how adventures work, adventurer.",
        "Perhaps you should consult a wizard for help.",
        "I think you meant to say something else.",
        "That's... creative, but wrong.",
        "The dungeon master is not amused."
    ]

    while True:
        command = input("> ").lower().strip()
        if command == "look":
            if location == "field":
                print("You are in an open field. To the east is a white house with a boarded front door.")
                print("There is a small mailbox here.")
            elif location == "forest":
                print("You are in a dense forest. Trees surround you. To the east is the open field.")
                if not riddle_solved:
                    print("There seems to be something hidden among the trees.")
            elif location == "house":
                print("You are inside the white house. It's dusty and old. There might be treasures here.")
                print("There's a green pipe in the corner, reminiscent of a classic video game.")
        elif command == "open mailbox":
            if location == "field":
                if not mailbox_opened:
                    print("You open the mailbox and find a leaflet inside.")
                    mailbox_opened = True
                else:
                    print("The mailbox is already open.")
            else:
                print("There's no mailbox here.")
        elif command == "read leaflet":
            if "leaflet" in inventory:
                if not leaflet_read:
                    print("The leaflet reads: 'Welcome to Zork! This is a basic text adventure game.'")
                    leaflet_read = True
                else:
                    print("You've already read the leaflet.")
            else:
                print("You don't have the leaflet.")
        elif command == "take leaflet":
            if location == "field" and mailbox_opened and "leaflet" not in inventory:
                print("You take the leaflet.")
                inventory.append("leaflet")
            elif "leaflet" in inventory:
                print("You already have the leaflet.")
            else:
                print("There's no leaflet to take.")
        elif command == "go east":
            if location == "forest":
                location = "field"
                print("You return to the open field west of the white house.")
            else:
                if door_locked:
                    if has_key:
                        print("You unlock the door with the key and enter the house.")
                        location = "house"
                        door_locked = False
                    else:
                        print("The door is locked. You need a key to enter.")
                else:
                    print("You enter the house.")
                    location = "house"
        elif command == "go up":
            if location == "cellar":
                location = "house"
                print("You climb up to the house.")
            else:
                print("You can't go that way.")
        elif command == "go down":
            if location == "house":
                location = "cellar"
                print("You open the trapdoor and go down to the cellar.")
            else:
                print("You can't go that way.")
        elif command == "fight" or command == "fight troll":
            if location == "cellar" and not troll_defeated:
                if "sword" in inventory:
                    print("You fight the troll with the sword and defeat it!")
                    troll_defeated = True
                else:
                    print("You need a weapon to fight the troll.")
            else:
                print("There's no one to fight here.")
        elif command == "go west" or command == "go left":
            if location == "field":
                location = "forest"
                print("You venture into the dense forest.")
            else:
                print("You can't go that way.")
        elif command == "go east" or command == "go right":
            if location == "forest":
                location = "field"
                print("You return to the open field west of the white house.")
            elif location == "cellar" and troll_defeated:
                location = "maze"
                print("You go east into a maze of twisty little passages.")
            elif location == "cellar":
                print("You can't go that way.")
            else:
                if door_locked:
                    if has_key:
                        print("You unlock the door with the key and enter the house.")
                        location = "house"
                        door_locked = False
                    else:
                        print("The door is locked. You need a key to enter.")
                else:
                    print("You enter the house.")
                    location = "house"
        elif command == "inventory":
            if inventory:
                print("You have: " + ", ".join(inventory))
            else:
                print("Your inventory is empty.")
        elif command == "unlock door":
            if location == "field" and door_locked:
                if has_key:
                    print("You unlock the door and enter the house.")
                    location = "house"
                    door_locked = False
                else:
                    print("You don't have the key.")
            else:
                print("There's no door to unlock here.")
        elif command == "solve riddle":
            if location == "forest" and not riddle_solved:
                print("A voice echoes: 'I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?'")
                print("Type your answer:")
                answer = input("> ").lower().strip()
                if answer == "echo":
                    print("Correct! You find a key hidden in the trees.")
                    has_key = True
                    riddle_solved = True
                else:
                    print("Wrong answer. Try again.")
            elif riddle_solved:
                print("You've already solved the riddle.")
            else:
                print("There's no riddle here.")
        elif command == "enter pipe":
            if location == "house" and not in_mario:
                print("You enter the green pipe and are transported to the Mushroom Kingdom!")
                print("You see a straight path with a pit in the middle and a pipe at the end.")
                in_mario = True
                mario_position = 0
                print_mario_level(mario_position)
                print("Commands: move, jump, enter pipe")
            elif in_mario and mario_position == 3:
                print("You enter the pipe and solve the puzzle! You are transported back to the house with a sword.")
                in_mario = False
                inventory.append("sword")
                location = "house"
            else:
                print("There's no pipe here.")
        elif in_mario:
            if command == "move":
                if mario_position < 3:
                    mario_position += 1
                    if mario_level[mario_position] == "pit":
                        print("You step forward but fall into the pit! Game over. Back to house.")
                        in_mario = False
                        location = "house"
                    else:
                        print(f"You move forward to position {mario_position}.")
                        print_mario_level(mario_position)
                else:
                    print("You're at the end, facing the pipe.")
            elif command == "jump":
                if mario_position == 0 and mario_level[1] == "pit":
                    print("You jump over the pit!")
                    mario_position = 2
                    print_mario_level(mario_position)
                else:
                    print("Nothing to jump over.")
            elif command == "quit mario":
                print("You exit the mini-game.")
                in_mario = False
                location = "house"
            else:
                print("Mario commands: move, jump, enter pipe, quit mario, hint")
        elif command == "i":
            if inventory:
                print("You have: " + ", ".join(inventory))
            else:
                print("Your inventory is empty.")
        elif command == "l":
            if location == "field":
                print("You are in an open field. To the east is a white house with a boarded front door.")
                print("There is a small mailbox here.")
                if verbose:
                    print("The grass sways gently in the breeze, and birds chirp in the distance.")
            elif location == "forest":
                print("You are in a dense forest. Trees surround you. To the east is the open field.")
                if not riddle_solved:
                    print("There seems to be something hidden among the trees.")
                if verbose:
                    print("The ancient trees tower above, their leaves rustling mysteriously.")
            elif location == "house":
                print("You are inside the white house. It's dusty and old. There might be treasures here.")
                print("There's a green pipe in the corner, reminiscent of a classic video game.")
                print("There's a trapdoor in the floor.")
                if verbose:
                    print("Dust motes dance in the sunlight filtering through cracked windows.")
            elif location == "cellar":
                print("You are in a dark cellar.")
                if not troll_defeated:
                    print("A troll blocks your way, growling menacingly.")
                else:
                    print("The troll is defeated. You can see a passage to the east.")
                if verbose:
                    print("The air is damp and musty, with cobwebs everywhere.")
            elif location == "maze":
                print("You are in a maze of twisty little passages, all alike.")
                if verbose:
                    print("It's confusing and dark, with no clear path.")
        elif command == "verbose":
            verbose = not verbose
            print("Verbose mode " + ("on" if verbose else "off"))
        elif command == "dev":
            has_key = True
            riddle_solved = True
            print("Dev shortcut: key obtained, riddle solved.")
        elif command == "hint":
            if location == "forest" and not riddle_solved:
                print("Hint: The answer is 'echo'.")
            elif location == "field" and door_locked and not has_key:
                print("Hint: You need to find a key. Try the forest.")
            elif in_mario:
                print("Hint: Jump over the pit from position 0.")
            else:
                print("No hints available here.")
        elif command == "quit" or command == "exit":
            print("Thanks for playing!")
            sys.exit()
        else:
            print(random.choice(insults))

if __name__ == "__main__":
    main()