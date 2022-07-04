##
# irene_indiana.py
# Created on: 9/06/2022
# Samuel Smith
# The computer game "Where in onslow college is Irene Indiana?"

import time
import os
import random

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
    global game_state, GAME
    # Speakers, No-clues, Containers, Keys, (add ciphers/puzzles)
    GAME = [[[[] for i in range(5)] for j in range(5)] for k in range(5)]
    # Speakers
    for speaker in POSSIBLE_SPEAK:
        if random.randint(0, 100) > -1:  # Make constant for different difficult
            GAME[0][speaker[3][0]][speaker[3][1]].append(speaker[0:3])
    # Non-Clues
    for non_clue in POSSIBLE_NON_CLUE:
        if random.randint(0, 100) > -1:  # again make constant
            GAME[1][non_clue[2][0]][non_clue[2][1]].append(non_clue[0:2])
    # Containers and their keys
    for container, key in POSSIBLE_CONTAINER:
        if random.randint(0, 100) > -1:  # again make constant
            GAME[2][container[4][0]][container[4][1]].append(container[0:4])
            GAME[3][key[2][0]][key[2][1]].append(key[0:2])
    for cipher in POSSIBLE_CIPHER:
        if random.randint(0, 100) > -1:  # again make constant
            GAME[4][random.randint(0,4)][random.randint(0,4)].append(cipher)
    game_state = True


def print_stats():
    pass


def action_menu():
    global pos, GAME
    print()
    print(f"    ========== {ROOM_NAMES[pos[1]][pos[0]]} ==========")
    print(DESCRIPTIONS[pos[1]][pos[0]])
    print("    =========================")
    print()
    print("Actions: ")
    print("(wasd) to move rooms")
    actions = []
    for i in range(5):
        for j in GAME[i][pos[0]][pos[1]]:
            actions.append([i, j])
    for i in range(len(actions)):
        print(f"{i+1})  - {actions[i][1][0]}")
    ans = input("\n> ")
    x = True
    if ans == 'w' and pos[1] < 4:
        index, change, direction = 1, 1, 'north'
    elif ans == 's' and pos[1] > 0:
        index, change, direction = 1, -1, 'south'
    elif ans == 'a' and pos[0] > 0:
        index, change, direction = 0, -1, 'east'
    elif ans == 'd' and pos[0] < 4:
        index, change, direction = 0, 1, 'west'
    else:
        x = False
        try:
            if int(ans) > 0 and int(ans) <= len(actions):
                print(f"Selected - {actions[int(ans)-1][1][0]}")
                if type(actions[int(ans)-1][1][1]) == list:
                    print(f"{random.choice(actions[int(ans)-1][1][1])}")
                else:
                    print(f"{actions[int(ans)-1][1][1]}")
            else:
                raise Exception("Out of action range")
        except:
            print("Not a valid input!")
    if x:
        pos[index] += change
        print(f"Moved {direction} to {ROOM_NAMES[pos[1]][pos[0]]}")
    input("    Enter to Continue")
    # Remove over previous line
    print("\033[1A\r                     ")


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

POSSIBLE_SPEAK = [
    ["Yell to Runners", "Runner: ", ["I ... heard ... {} ... was ... near ... {} ...", ""], [0, 0]],
    ["Talk to Maths Teacher", "Maths Teacher: ", ["I thought {} was at {}", ], [3, 0]],
    ["Talk to Physics Teacher", "Physics Teacher: ", [], [1, 1]],
    ["Talk to Enlglish Teacher", "English Teacher: ", [], [0, 2]],
    ["Talk to Basketballers", "Basketballer: ", [], [2, 3]],
]

POSSIBLE_NON_CLUE = [
    ["Leave school", ["You decided to stay; you need to find Irene", "You aren't allowed to leave"], [4, 0]],
    ["Talk to student at microwave", ["..."], [1, 3]]
]

# [['container desc', 'open attempt', 'open', [locx, locy], reward_funct],
# ['key desc', 'pick up key', [locx, locy]]]
POSSIBLE_CONTAINER = [
    [["Open Shipping Container", "Cannot open, the old rusty lock wont budge",
      "The acid dissolved the rusty latch and the door swings open", check_irene, [0, 0]],
     ["Acid (could be used to dissolve metal or remove rust)", "Picked up acid (don't spill it)", [1, 0]]],
    [["Talk to hooded kid", "He ignores you, entirely obsessed with the comforting glow of his smartphone",
      "The smell of the lollies, tantalisingly sweet and delicous, fills the air. The hooded kid notices and glances up, \
      entranced by the aroma. You see longing in his eyes, to break free, to escape the emotionally manipulating programs.\
      He starts towards you, but shudders and gives in. He returns to the glowing rectangle, encompassed in its friendly\
      warmth.", pick_up, [0, 1]], ["A dollar bag of lollies (could be used to bribe children)", "You pay for the dollar bag and put it in your pocket", [0, 4]]],
    [["A battered silver car, parked on a horrific angle, sits at the edge of the carpark. Could it contain a secret?", "You try the boot, but it's locked.",
      "You open the boot and find a note", pick_up, [4, 0]], ["Car keys with the same logo as the one in the carpark",
      "You picked up the car keys and quietly slid them into your pocket", [4, 1]]]
]

POSSIBLE_CIPHER = [
    ["Note0", "Read Note, are now bored"],
    ["Note1", "Read Note"],
    ["Note2", "Read Note"],
    ["Note3", "Read Note"],
    ["Note4", "Read Note"],
    ["Note5", "Read Note"],
    ["Note6", "Read Note"],
    ["Note7", "Read Note"],
    ["Note8", "Read Note"],
    ["Note9", "Read Note"],
]  # Not here yet

ROOM_NAMES = [
    ["Top Field", "Chemistry", "Science Corridor", "Maths Corridor", "Student Carpark"],
    ["Old Skatebowl", "Physics", "Garden", "Digital Tech", "Art Department"],
    ["English Block", "Library", "Social Sciences", "Accounting", "Hall"],
    ["Rear exit", "Student Centre", "Quad", "Driveway", "Design Tech"],
    ["Dairy", "Table Mountain", "Far Table Mountain", "Gym", "Bottom Field"]
]


# Variables
pos = [4, 0]
# Format - [speakers, non-clues, containers, keys, (to be ciphers)]
GAME = []

game_state = False
game_loop = True

while game_loop:
    if not game_state:
        main_menu()
    else:
        action_menu()


print("\nThanks for playing 'Where in Onslow College is Irene Indiana?'")
