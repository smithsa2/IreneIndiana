##
# irene_indiana.py
# Created on: 9/06/2022
# Samuel Smith
# The computer game "Where in onslow college is Irene Indiana?"

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
        print("Error: feature not added yet")
    elif user_input == '2':
        print("No current game")
    elif user_input == '3':
        print("Made by me")
    elif user_input == '4':
        print(credits)
    elif user_input == '5':
        game_loop = False
    else:
        print("That wasn't an option")


def new_game():
    # Figure out how and where I want to store the game data
    pass


game_state = main_menu
game_loop = True

while game_loop:
    game_state()

print("\nThanks for playing Irene Indiana!")