import sys
import random

def main():
    print("You are standing in an open field west of a white house, with a boarded front door.")
    print("There is a small mailbox here.")
    location = "field"
    mailbox_opened = False
    leaflet_read = False
    inventory = []

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
                print("You approach the white house, but the door is boarded shut.")
        elif command == "go west":
            if location == "field":
                location = "forest"
                print("You venture into the dense forest.")
            else:
                print("You can't go that way.")
        elif command == "inventory":
            if inventory:
                print("You have: " + ", ".join(inventory))
            else:
                print("Your inventory is empty.")
        elif command == "quit" or command == "exit":
            print("Thanks for playing!")
            sys.exit()
        else:
            print(random.choice(insults))

if __name__ == "__main__":
    main()