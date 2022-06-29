##
# irene_indiana.py
# Created on: 9/06/2022
# Samuel Smith
# The computer game "Where in onslow college is Irene Indiana?"

import os

#Funtions

def main_menu():
    global game_loop, game_state
    print("""
   - Irene Indiana -   
======================

1) New Game
2) Continue Game
3) Credits
4) Help & Tutorials
5) Quit""")
    user_input = input("> ").strip().lower() 
    if user_input == '1':
        new_game()
    elif user_input == '2':
        if not os.path.exists("/game_data/current_game.txt"):
            print("No current game")
        else:
            load_game()
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
    # Figure out how and where I want to store the game data (do last)
    game_state = True

def load_game():
    with open("/game_data/current_game.txt", 'r'):
        pass

def action_menu():
    print("""""")

# Constants
CREDITS = "Made by me"
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
          'Gym','Bottom field']]

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

POSSIBLE_ACTIONS = [[],
    [],
    [],
    [],
    []]

# Variables
pos = [4,0]


game_state = False
game_loop = True

while game_loop:
    if not game_state:
        main_menu()
    else:
        action_menu()


print("\nThanks for playing 'Where in Onslow College is Irene Indiana?'")