##
# game_menu_test.py
# 23/06/2022
# SamuelSmith
# Test of main menu for IreneIndiana

import time

game_menu = True

while game_menu:
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
        pass
    elif user_input == '2':
        pass
    elif user_input == '3':
        pass
    elif user_input == '4':
        pass
    elif user_input == '5':
        game_menu = False
    else:
        print("That wasn't an option")
    time.sleep(0.1)
    
print("\nThanks for playing Irene Indiana!")
time.sleep(0.1)
