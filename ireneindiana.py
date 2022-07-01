##
# irene_indiana.py
# Created on: 9/06/2022
# Samuel Smith
# The computer game "Where in onslow college is Irene Indiana?"

import os

# Funtions


def main_menu():
    global game_loop, game_state
    print("""
   - Irene Indiana -
======================

1) New Game
2) Stats
3) Credits
4) Help & Tutorials
5) Quit""")
    user_input = input("> ").strip().lower()
    if user_input == '1':
        new_game()
    elif user_input == '2':
        if not os.path.exists("game_data/current_game.txt"):
            print("No stats")
        else:
            print_stats()
    elif user_input == '3':
        print(CREDITS)
    elif user_input == '4':
        print(HELP)
    elif user_input == '5':
        game_loop = False
    else:
        print("That wasn't an option")


def new_game():
    global game_state
    game_state = True



def print_stats():
    pass


def action_menu():
    print("""""")


def pick_up(key):
    pass


def check_irene(key):
    pass


def talk(key):
    pass

# Constants
CREDITS = """

===========================
    Made by Samuel Smith
===========================

"""
HELP = "Google it"
MAP = [['Top field', 'Chemistry classrooms', 'Science hallway',
        'Maths corridor', 'Student carpark'],
       ['Old Skatebowl', 'Physics classrooms', 'Garden',
        'Digital Tech classes', 'Art department'],
       ['English block', 'Library', 'Social Sciences',
        'Accounting & Business', 'Hall'],
       ['Rear driveway', 'Student Centre', 'Quad', 'Main Driveway',
        'Design Tech'],
       ['Dairy', 'Table mountain: (main)', 'Table mountain (far)',
        'Gym', 'Bottom field']]

DESCRIPTIONS = []

if not os.path.exists("game_data/descriptions.txt"):
    print("Descriptions file is missing. Cannot Run")
    quit()
else:
    with open("game_data/descriptions.txt", 'r') as file:
        x = file.readlines()
        for i in range(5):
            DESCRIPTIONS.append([])
            for j in range(5):
                DESCRIPTIONS[i].append(x[i*5+j])

# Format ['Action name', 'name of speaker', [dialogue1, dialouge2, etc.]]
POSSIBLE_SPEAK = [[
    [["Yell to Runners", "Runner: ", ["I ... heard ... {} ... was ... near ... {} ...", ""]]],
    [],
    [],
    [],
    []],
    [[],
     [],
     [],
     [],
     []],
    [[],
     [],
     [],
     [],
     []],
    [[],
     [],
     [],
     [],
     []],
    [[],
     [],
     [],
     [],
     []]]

POSSIBLE_NON_CLUE = [
    [[],
     [],
     [],
     [],
     []],
    [[],
     [],
     [],
     [],
     []],
    [[],
     [],
     [],
     [],
     []],
    [[],
     [],
     [],
     [],
     []],
    [[],
     [],
     [],
     [],
     []]]

# [['container desc', 'open attempt', 'open', [locx, locy], reward_funct],
# ['key desc', 'pick up key', [locx, locy]]]
POSSIBLE_CONTAINER = [
    [["Open Shipping Container", "Cannot open, the old rusty lock wont budge",
      "The acid dissolved the rusty latch and the door swings open", [0, 0], check_irene],
     ["Acid (could be used to dissolve metal or remove rust)", "Picked up acid (don't spill it)", [1, 0]]],
    [["Talk to hooded kid", "He ignores you, entirely obsessed with the comforting glow of his smartphone",
      "The smell of the lollies, tantalisingly sweet and delicous, fills the air. The hooded kid notices and glances up, \
      entranced by the aroma. You see longing in his eyes, to break free, to escape the emotionally manipulating programs.\
      He starts towards you, but shudders and gives in. He returns to the glowing rectangle, encompassed in its friendly\
      warmth.", [0,1], pick_up], ["A dollar bag of lollies (could be used to bribe children)", "You paid for the dollar bag and put it in your pocket", [0,4]]],
    [["A battered silver car, parked on a horrific angle, sits at the edge of the carpark. Could it contain a secret?", "You try the boot, but it's locked.",
      "You open the boot and find a note", pick_up],["The car keys have the same logo as the one in the carpark", 
      "You picked up the car keys and quietly slid them into your pocket", [4,1]]]]

POSSIBLE_CIPHER = []


# Variables
pos = [4, 0]

game_state = False
game_loop = True

while game_loop:
    if not game_state:
        main_menu()
    else:
        action_menu()


print("\nThanks for playing 'Where in Onslow College is Irene Indiana?'")
