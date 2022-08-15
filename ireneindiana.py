##
# irene_indiana.py
# Created on: 9/06/2022
# Samuel Smith
# The computer game "Where in onslow college is Irene Indiana?"

import logging

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
        x = input("Easy (1) or Hard (2): \n> ")
        while x not in ['1','2']:
            print("Please enter '1' for easy or '2' for hard")
            x = input("Easy (1) or Hard (2): \n> ").strip().lower()
        new_game(int(x)-1)
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


def new_game(difficulty):
    global game_state, game, irene, note_text, trail, game_time, hint, score_multiplier, score
    # Speakers, No-clues, Containers, Keys, (add ciphers/puzzles)
    game = [[[None for i in range(5)] for j in range(5)] for k in range(5)]
    choices = []
    # Speakers
    for speaker in POSSIBLE_SPEAK:
        if random.randint(0, 100) > -1:  # Make constant for different difficult
            choices.append([0, speaker])
            game[speaker[3][0]][speaker[3][1]][0] = speaker[0:3]
            # Red herring
            game[speaker[3][0]][speaker[3][1]][0][2] = f"I haven't seen Irene, maybe she is at {ROOM_NAMES[random.randint(0,4)][random.randint(0,4)]}"
    # Non-Clues
    for non_clue in POSSIBLE_NON_CLUE:
        if random.randint(0, 100) > -1:  # again make constant
            game[non_clue[2][0]][non_clue[2][1]][1] = non_clue[0:2]
    # Containers and their keys
    for container in POSSIBLE_CONTAINER:
        key = container[-1]
        if random.randint(0, 100) > -1:  # again make constant
            choices.append([1, key, container[0:-1]+[key[2]]])
            game[container[4][0]][container[4][1]][2] = container[0:-2]+[key[2]]
            game[key[3][0]][key[3][1]][3] = key[0:3]
    for cipher in POSSIBLE_CIPHER:  # Make list of all rooms and shuffle them. 
        if random.randint(0, 100) > -1:  # again make constant
            pos = [random.randint(0,4), random.randint(0,4)]
            cipher.append(pos)
            choices.append([2, cipher])
            game[pos[0]][pos[1]][4] = cipher[0:]
            # Red Herring
            red_loc = ROOM_NAMES[random.randint(0,4)][random.randint(0,4)]
            possible_herrings = ["Irene Indiana is at {}",
                                 "Irene's at {}",
                                 "Ms. Miller said Irene was at {}",
                                 "I saw Irene at {}",
                                 "Irene's got to be in {}"]
            note_text[cipher[1]] = random.choice(possible_herrings).format(red_loc)
    # Place Irene
    irene = random.choice(POSSIBLE_IRENE)
    prev = irene
    # Generate clue trail
    random.shuffle(choices)
    trail = []
    # Random based on difficulty
    length = [random.randint(5, 10), random.randint(10, 17)][difficulty]
    for i in range(len(choices[:length])):
        choice = choices[i]
        key_type = choice[0]
        logging.warning(f"Prev: {prev}")
        logging.warning(f"Choice: {choice}")
        if key_type == 0:  # Speaker
            # Make dialogue/solution contain clue
            pos = choice[1][-1]
            game[pos[0]][pos[1]][key_type][2] = random.choice(choice[1][2]).format("Irene", ROOM_NAMES[prev[1]][prev[0]])
            trail.append([choice[1][0], pos])
        elif key_type == 1: # Container
            note_loc = ROOM_NAMES[prev[1]][prev[0]]
            possible_texts = ["Check near {}",
                              "Perhaps she is at {}",
                              "She might be near {}",
                              "She often hangs out around {}"]
            note_text[choice[2][3]] = random.choice(possible_texts).format(note_loc)
            logging.warning(choice)
            pos = choice[2][4]
            trail.append([choice[2][3], pos])
            pos = choice[1][3] # Direction of next hint is to key then container
            trail.append([choice[1][0], pos])
            pos = choice[2][4] # Direction of next clue is to container not to key
        elif key_type == 2: # Note/Cipher
            note_loc = ROOM_NAMES[prev[1]][prev[0]]
            possible_texts = ["Check near {}",
                              "Perhaps she is at {}",
                              "She might be near {}",
                              "My friend saw her at {}",
                              "I was at {} before and she was there",
                              "I saw her friend at {}"]
            note_text[choice[1][1]] = random.choice(possible_texts).format(note_loc)
            pos = choice[1][2]
            trail.append([choice[1][0], pos])
        else:
            raise Exception("Invalid key_type")
        prev = pos
    trail.reverse()
    hint = trail[0]
    logging.warning(f"Trail starts at {ROOM_NAMES[prev[1]][prev[0]]}")
    logging.warning(trail)
    game_time = [300, 150][difficulty] + random.randint(-30,30)
    score_multiplier = [EASY_MULTIPLY, HARD_MULTIPLY][difficulty]
    score = 0
    game_state = True


def print_stats():
    pass

def display(pos):
    print(" _ _ _ _ _")
    for y in range(5, -1, -1):
        string = "|"
        for x in range(5):
            if [x,y] == pos:
                string += "X|"
            elif [x,y] == hint:
                string += '?|'
            else:
                string += "_|" 
        if y == 0:
            string += f'     Time: {game_time//60}h {game_time%60}m left   Current Score: {score}'
        print(string)

def action_menu():
    global pos, game, inventory, game_time, game_loop, hint, trail, score, score_multiplier
    # Print Map and Time remaining
    if game_time <= 0:
        print("You have run out of game_time!")
        game_loop = False
        return
    print()
    display(pos)
    # Print Location and description
    print(f"\n    ========== {ROOM_NAMES[pos[1]][pos[0]]} ==========")
    print(DESCRIPTIONS[pos[1]][pos[0]][0:-1])
    print("    ======================" + '=' * len(ROOM_NAMES[pos[1]][pos[0]]) + "\n")
    print("Actions: ")
    print("(wasd) to move rooms")
    print("'h' to get a hint (will lower score)")
    print("'e' to open inventory")
    actions = [[i, game[pos[0]][pos[1]][i]] for i in range(5) if game[pos[0]][pos[1]][i] is not None]
    #Print Actions
    for i in range(len(actions)):
        print(f"{i+1})  - {actions[i][1][0]}")
    if pos in POSSIBLE_IRENE:
        print("I)  - Search for Irene")
    # Get input
    ans = input("\n> ").strip().lower()
    x = True
    # Check if movement input
    if ans == 'w' and pos[1] < 4:
        index, change, direction = 1, 1, 'north'
    elif ans == 's' and pos[1] > 0:
        index, change, direction = 1, -1, 'south'
    elif ans == 'a' and pos[0] > 0:
        index, change, direction = 0, -1, 'east'
    elif ans == 'd' and pos[0] < 4:
        index, change, direction = 0, 1, 'west'
    # Check if hint
    elif ans == 'h':
        x = False
        # Decrease difficulty modifier
        score_multiplier *= 0.9
        print(f"Action: {hint[0]} in {ROOM_NAMES[hint[1][1]][hint[1][0]]}")
    # Check if irene search
    elif ans == 'i' and pos in POSSIBLE_IRENE:
        x = False
        check_irene(pos)
    # Check if action option
    else:
        x = False
        try:
            y = int(ans) - 1
            if y >= 0 and y < len(actions):
                # Do action
                match (actions[y][0]):
                    case 0: # Speak
                        game_time -= int(SPEAK_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        print(f"{actions[y][1][1]} {actions[y][1][2]}") # Add formatting for clue
                    case 1: # Non-clue
                        game_time -= int(NON_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        print(f"{random.choice(actions[y][1][1])}")
                    case 2: # Container
                        game_time -= int(CONT_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        if actions[y][1][-1] in inventory:
                            print(actions[y][1][2])
                            # Do container action
                            if actions[y][1][4] == 'irene':
                                print("Checking for Irene Indiana")
                                check_irene(pos) # Call function
                            else:
                                print("You found a note (added to inventory)")
                                inventory.append(actions[y][1][4]) # Pickup item
                                print(f"It reads: |{note_text[actions[y][1][3]]}|")
                            actions.pop(y)
                        else:
                            print(actions[y][1][1])
                    case 3: # Keys
                        game_time -= int(KEY_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        print(actions[y][1][1])
                        inventory.append(actions[y][1][2])
                        print("Item added to inventory")
                        game[pos[0]][pos[1]][3].pop(0) # Remove container from room
                    case 4: # Cipher
                        game_time -= int(CIPHER_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        note_print(actions[y][1][1])
                # Check if room and action is next hint
                logging.warning(f"action {actions[y][1][0]} hint {hint[0]}")
                logging.warning(f"action room {pos} hint room {hint[1]}")
                if actions[y][1][0] == hint[0] and pos == hint[1]:
                    # Remove hint from hint list
                    trail.pop(0)
                    # Set new hint from hint list
                    if len(trail) >= 1:
                        hint = trail[0]
                    else:
                        hint = ["Check Irene", irene]
                    # Add to score
                    score += int(NEXT_STEP_SCORE * score_multiplier)
            else:
                raise Exception("Out of action range")
        except BaseException as exception_error: # For debug purposes
            logging.exception(exception_error)
            print(f"Not a valid input! Wasted {int(ERR_TIME * score_multiplier)} minutes")
            game_time -= int(ERR_TIME * score_multiplier)
    # Move if input was movement
    if x:
        game_time -= int(MOVE_TIME * score_multiplier)
        pos[index] += change
        print(f"Moved {direction} to {ROOM_NAMES[pos[1]][pos[0]]}")
    # Wait for user
    input("    Enter to Continue")
    # Remove over previous line
    print("\033[1A\r                     ")


def check_irene(pos):
    global game_time, score
    if pos == irene:
        print(f"You have found the elusive Irene Indiana! There were {game_time//60}h {game_time%60}m to spare")
        # Calculate score
        score += int(IRENE_SCORE * score_multiplier)
        score += int(game_time * TIME_SCORE * score_multiplier)
        print(f"Score: {score}")
        logging.warning(f"game_time: {game_time}")
        # Actually win
    else:
        print(f"You searched for Irene, but it seems she is not here. You wasted {IRENE_TIME} minutes")
        game_time -= IRENE_TIME


def note_print(x):
    global game_time, score
    print("\n - Encrypted Note - \n")
    start_time = time.time()
    a = random.randint(0,3)
    text = note_text[x]
    words = text.split(" ")
    new_string = []
    if a == 0:  # Scramble words in place
        for word in words:
            b = [char for char in word]
            random.shuffle(b)
            new_string.append("".join(b))
        print("Hint: Scrambled eggs")
    elif a == 1:  # Fill in the blanks
        letters = ""
        for word in words:
            b = ""
            for char in word:
                if random.randint(0,4) == 0:
                    letters += char
                    b += "_"
                else:
                    b += char
            new_string.append(b)
        letters = [char for char in letters]
        random.shuffle(letters)
        letters = "".join(letters)
        print(f"Hint: Some of the letters must have fallen off '{letters}'")
    elif a == 2:  #  
        alpha = "abcdefghijklmnopqrstuvwxyz"
        for word in words:
            b = "|"
            for char in word.lower():
                if char in alpha:
                    b += str(alpha.index(char) + 1) + '|'
                else:
                    b += char + '|'
            new_string.append(b)
        print("Hint: I thought these would be letters")
    else:
        alpha = sorted("".join(words).lower())
        i = 0
        while i <len(alpha):
            if i != 0 and alpha[i] == alpha[i-1]:
                alpha.pop(i)
            else:
                i += 1
        for word in words:
            b = "|"
            for char in word.lower():
                b += str(alpha.index(char) + 1) + '|'
            new_string.append(b)
        alpha = [f"{i+1}:{alpha[i]}" for i in range(len(alpha))]
        print(f"Hint: {' '.join(alpha)}")
    new_string = " ".join(new_string)
    print(f"\n{new_string}\n")
    print("Enter decrypted string: ")
    while True:
        x = input("> ").lower().strip()
        if x == text.lower().strip():
            total_time = time.time() - start_time
            print(f"Code cracked in {round(total_time)} seconds!")
            score += int(CODE_SCORE * score_multiplier )
            total_time = int(total_time / 6)
            print(f"{total_time} minutes have passed")
            game_time -= total_time
            break
        else:
            print("Incorrect. Enter the decrypted string")



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
    print("Descriptions file is missing. Cannot run")
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
    ["Yell to Runners", "Runner: ", ["I ... heard ... {} ... was ... near ... {} ..."], [0, 0]],
    ["Talk to Maths Teacher", "Maths Teacher: ", ["I thought {} was at {}", "I think {} said they would be at {}"], [3, 0]],
    ["Talk to Physics Teacher", "Physics Teacher: ", ["I thought {} was at {}"], [1, 1]],
    ["Talk to Enlglish Teacher", "English Teacher: ", ["I thought {} was at {}"], [0, 2]],
    ["Talk to Basketballers", "Basketballer: ", ["I thought {} was at {}"], [2, 3]]
]

POSSIBLE_NON_CLUE = [
    ["Leave school", ["You decided to stay; you need to find Irene", "You aren't allowed to leave"], [4, 0]],
    ["Talk to student at microwave", ["..."], [1, 3]]
]

# [['container desc', 'open attempt', 'open', [locx, locy], reward_funct],
# ['key desc', 'pick up key', [locx, locy]]]
POSSIBLE_CONTAINER = [
    ["Open Shipping Container", "Cannot open, the old rusty lock wont budge",
      "The acid dissolved the rusty latch and the door swings open", 'container_note', [0, 0],
      ["Acid (could be used to dissolve metal or remove rust)", "Picked up acid (don't spill it)", 'acid', [1,0]]],
    ["Talk to hooded kid", "He ignores you, entirely obsessed with the comforting glow of his smartphone",
      "The smell of the lollies, tantalisingly sweet and delicous, fills the air. The hooded kid notices and glances up.\
He gives you a key labelled 'staffroom'", 'staffroom_key', [0, 1],
      ["A dollar bag of lollies (could be used to bribe children)", "You pay for the dollar bag and put it in your pocket", 'lollies', [0, 4]]],
    ["A battered silver car, parked on a horrific angle, sits at the edge of the carpark. Could it contain a secret?", "You try the boot, but it's locked.",
      "You open the boot and find a note", 'car_note', [4, 0],
      ["Car keys with the same logo as the car in the carpark",
      "You picked up the car keys and quietly slid them into your pocket", 'car_keys', [4, 1]]]
]

POSSIBLE_CIPHER = [
    ["Engraved stone", "note"],
    ["Paper slip", "note1"],
    ["Letter", "note2"],
    ["Sticky note", "note3"],
    ["NoteA", "note4"],
    ["NoteB", "note5"],
    ["NoteC", "note6"],
    ["NoteD", "note7"],
    ["NoteE", "note8"],
    ["NoteF", "note9"],
]  # Not here yet

ROOM_NAMES = [
    ["Top Field", "Chemistry", "Science Corridor", "Maths Corridor", "Student Carpark"],
    ["Old Skatebowl", "Physics", "Garden", "Digital Tech", "Art Department"],
    ["English Block", "Library", "Social Sciences", "Accounting", "Hall"],
    ["Rear exit", "Student Centre", "Quad", "Driveway", "Design Tech"],
    ["Dairy", "Table Mountain", "Far Table Mountain", "Gym", "Bottom Field"]
]

# Rooms that Irene can be in
POSSIBLE_IRENE = [
    [0,0],
    [2,0],
    [1,1],
    [2,1],
    [3,1],
    [4,1],
    [1,2],
    [2,2],
    [3,2],
    [4,2],
    [0,3],
    [4,3],
    [0,4],
    [1,4],
    [2,4],
    [3,4]
]

# Rooms that you can search for irene in (excludes containers)
POSSIBLE_SEARCH = [
    [False, False, True, False, False],
    [False, True, False, True, False],
    [False, True, True, True, True],
    [True, False, False, False, True],
    [True, True, True, True, False]
]

ERR_TIME = 15
CIPHER_TIME = 5
KEY_TIME = 5
CONT_TIME = 15
NON_TIME = 5
SPEAK_TIME = 5
MOVE_TIME = 5
IRENE_TIME = 40
HARD_MULTIPLY = 2.5
EASY_MULTIPLY = 1
NEXT_STEP_SCORE = 50
CODE_SCORE = 10
IRENE_SCORE = 1000
TIME_SCORE = 1

# Variables
pos = [4, 0]
# Format - [speakers, non-clues, containers, keys, (to be ciphers)]
game = []
inventory = []
irene = [0,0]
note_text = {}
game_time = 0
hint = []
score_multiplier = 1
score = 0


game_state = False
game_loop = True

while game_loop:
    if not game_state:
        main_menu()
    else:
        action_menu()


print("\nThanks for playing 'Where in Onslow College is Irene Indiana?'")
