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
        x = input("Easy (1) or Hard (2): \n> ")
        while x not in ['1', '2']:
            print("Please enter '1' for easy or '2' for hard")
            x = input("Easy (1) or Hard (2): \n> ").strip().lower()
        new_game(int(x)-1)
    elif user_input == '2':
        print_stats()
    elif user_input == '3':
        print(CREDITS)
    elif user_input == '4':
        for item in HELP:
            print(item)
            x = input("(enter to continue):\n> ")
    elif user_input == '5':
        game_loop = False
    else:
        print("That wasn't an option")


def new_game(difficulty):
    global pos, game_state, game, inventory, irene, note_text, trail, game_time, hint, score_multiplier, score, stats, crossiant
    pos = [4, 0]
    inventory = []
    note_text = {"croissant": "A mysterious flaky french pastry. You feel dizzy just looking at it",
                 "acid": "A beaker of strong acid",
                 "car_keys": "An old car key",
                 "staffroom_key": "A key with a ribbon labelled 'staffroom",
                 "lollies": "A small bag of party mix",
                 "car_note": "An old reciept",
                 "kid_note": "A sheet of paper that says 'lol'",
                 "container_note": "An old sports day roster",
                 "dirt_note": "An envelope containg $10,000 in cash"}
    # Speakers, No-clues, Containers, Keys, Ciphers/puzzles
    game = [[[None for i in range(5)] for j in range(5)] for k in range(5)]
    choices = []
    # Speakers
    for speaker in POSSIBLE_SPEAK:
        if random.random() < SPEAK_CHANCE[difficulty]:
            choices.append([0, speaker])
            game[speaker[3][0]][speaker[3][1]][0] = speaker[0:3]
            # Red herring
            game[speaker[3][0]][speaker[3][1]][0][2] = f"I haven't seen Irene, maybe she is at {ROOM_NAMES[random.randint(0,4)][random.randint(0,4)]}"
    # Non-Clues
    for non_clue in POSSIBLE_NON_CLUE:
        game[non_clue[2][0]][non_clue[2][1]][1] = non_clue[0:2]
    # Containers and their keys
    for container in POSSIBLE_CONTAINER:
        if random.random() < CONTAINER_CHANCE[difficulty]:
            key = container[-1]
            choices.append([1, key, container[0:-1]+[key[2]]])
            game[container[4][0]][container[4][1]][2] = container[0:-2]+[key[2]]
            game[key[3][0]][key[3][1]][3] = key[0:3]
    for cipher in POSSIBLE_CIPHER:  # Make list of all rooms and shuffle them.
        if random.random() < CIPHER_CHANCE[difficulty]:
            apos = [random.randint(0, 4), random.randint(0, 4)]
            cipher.append(apos)
            choices.append([2, cipher])
            game[apos[0]][apos[1]][4] = cipher[0:]
            # Red Herring
            red_loc = ROOM_NAMES[random.randint(0, 4)][random.randint(0, 4)]
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
    length = [random.randint(3, 7), random.randint(7, 12)][difficulty]
    for i in range(len(choices[:length])):
        choice = choices[i]
        key_type = choice[0]
        if key_type == 0:  # Speaker
            # Make dialogue/solution contain clue
            apos = choice[1][-1]
            game[apos[0]][apos[1]][key_type][2] = random.choice(choice[1][2]).format("Irene", ROOM_NAMES[prev[1]][prev[0]])
            trail.append([choice[1][0], apos])
        elif key_type == 1:  # Container
            note_loc = ROOM_NAMES[prev[1]][prev[0]]
            possible_texts = ["Check near {}",
                              "Perhaps she is at {}",
                              "She might be near {}",
                              "She often hangs out around {}"]
            note_text[choice[2][3]] = random.choice(possible_texts).format(note_loc)
            apos = choice[2][4]
            trail.append([choice[2][0], apos])
            apos = choice[1][3]  # Direction of next hint is to key then container
            trail.append([choice[1][0], apos])
            apos = choice[2][4]  # Direction of next clue is to container not to key
        elif key_type == 2:  # Note/Cipher
            note_loc = ROOM_NAMES[prev[1]][prev[0]]
            possible_texts = ["Check near {}",
                              "Perhaps she is at {}",
                              "She might be near {}",
                              "My friend saw her at {}",
                              "I was at {} before and she was there",
                              "I saw her friend at {}"]
            note_text[choice[1][1]] = random.choice(possible_texts).format(note_loc)
            apos = choice[1][2]
            trail.append([choice[1][0], apos])
        else:
            raise Exception("Invalid key_type")
        prev = apos
    trail.reverse()
    hint = trail[0]
    game_time = [EASY_TIME, HARD_TIME][difficulty] * (len(trail) + 1) + random.randint(-TIME_RANGE, TIME_RANGE)
    stats[0] += game_time
    score_multiplier = [EASY_MULTIPLY, HARD_MULTIPLY][difficulty]
    score = 0
    # Randomize time-slowing crossiant location
    crossiant = [[random.randint(0, 5), random.randint(0, 5)], True]
    game_state = True


def display(pos):
    print(" _ _ _ _ _")
    for y in range(4, -1, -1):
        string = "|"
        for x in range(5):
            if [x, y] == pos:
                string += "X|"
            elif [x, y] == hint:
                string += '?|'
            else:
                string += "_|"
        if y == 0:
            string += f'     Time: {game_time//60}h {game_time%60}m left   Current Score: {score}'
        print(string)


def print_stats():
    if not os.path.exists("game_data/user_stats.txt"):
        print("User stats file is missing. Cannot run. Reinstall it")
        quit()
    else:
        try:
            print("\nUSER STATS: \n")
            with open("game_data/user_stats.txt", 'r') as file:
                file = file.readlines()
                games = int(file[-1].split(' = ')[1]) + 0.000001
                x = file[0].split(' = ')[1][0:-1]
                print(f"Total in-game time: {x} (per game avg. {round(int(x)/games,2)})")
                x = file[1].split(' = ')[1][0:-1]
                print(f"Total moves: {x} (per game avg. {round(int(x)/games,2)})")
                x = file[2].split(' = ')[1][0:-1]
                print(f"Total score: {x} (per game avg. {round(int(x)/games,2)})")
                x = file[3].split(' = ')[1][0:-1]
                print(f"Total notes deciphered: {x} (per game avg. {round(int(x)/games,2)})")
                x = file[4].split(' = ')[1][0:-1]
                print(f"Total mistyped commands: {x} (per game avg. {round(int(x)/games,2)})")
                print(f"Total games played: {int(games)} (per game avg. 1)")
        except:
            print("User stats file is corrupt. Reinstall it")


def write_stats():
    global stats
    if not os.path.exists("game_data/user_stats.txt"):
        print("User stats file is missing. Cannot run. Reinstall it")
        quit()
    else:
        try:
            with open("game_data/user_stats.txt", 'r') as file:
                file = file.readlines()
                x = []
                for i in range(6):
                    x.append(int(file[i].split(' = ')[1]) + stats[i])
            with open("game_data/user_stats.txt", 'w') as file:
                file.write(f"TOTAL_TIME = {x[0]}\nTOTAL_MOVES = {x[1]}\nTOTAL_SCORE = {x[2]}\nTOTAL_DECIPHERS = {x[3]}\nTOTAL_ERRORS = {x[4]}\nGAMES_PLAYED = {x[5]}")
            stats = [0, 0, 0, 0, 0, 0]
        except:
            print("User stats file is corrupt. Reinstall it.")


def action_menu():
    global pos, game, inventory, game_time, game_state, hint, trail, score, score_multiplier, stats
    # Print Map and Time remaining
    if game_time <= 0:
        print("You have run out of game_time!")
        game_state = False
        stats[5] += 1
        write_stats()
        return
    if pos == crossiant[0] and crossiant[1]:
        crossiant[1] = False
        print("Congratulations! You have found the mysterious time slowing croissant")
        inventory.append('croissant')
        stats[0] += int(game_time * 1.2) - game_time
        game_time = int(game_time * 1.2)
        print("Item added to inventory")
        # Wait for user
        input("    Enter to Continue")
        # Remove over previous line
        print("\033[1A\r                     ")
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
    print("'esc' to exit the game")
    actions = [[i, game[pos[0]][pos[1]][i]] for i in range(5) if game[pos[0]][pos[1]][i] is not None]
    # Print Actions
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
    elif ans == 'esc':
        ans = input("Are you sure you want to leave? 'y'/'n':\n> ")
        if ans == 'y':
            stats = [0, 0, 0, 0, 0, 0]
            game_state = False
            return
        else:
            print("Returning to game")
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
    elif ans == 'e':
        x = False
        print("INVENTORY")
        for item in inventory:
            if 'note' in item:
                try:
                    item_i = [i[0] for i in POSSIBLE_CIPHER].index(item)
                    print(f"{POSSIBLE_CIPHER[item_i]} - {note_text[item]}")
                except:
                    print(f"Note - {note_text[item]}")
            else:
                print(f"{item.title()} - {note_text[item]}")
        print()
    else:
        x = False
        try:
            y = int(ans) - 1
            if y >= 0 and y < len(actions):
                # Do action
                match(actions[y][0]):
                    case 0:  # Speak
                        game_time -= int(SPEAK_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        print(f"{actions[y][1][1]} {actions[y][1][2]}") # Add formatting for clue
                    case 1:  # Non-clue
                        game_time -= int(NON_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        print(f"{random.choice(actions[y][1][1])}")
                    case 2:  # Container
                        game_time -= int(CONT_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        if actions[y][1][-1] in inventory:
                            print(actions[y][1][2])
                            # Do container action
                            print("You found a note (added to inventory)")
                            inventory.append(actions[y][1][3]) # Pickup item
                            print(f"It reads: |{note_text[actions[y][1][3]]}|")
                            actions.pop(y)
                        else:
                            print(actions[y][1][1])
                    case 3:  # Keys
                        game_time -= int(KEY_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        print(actions[y][1][1])
                        inventory.append(actions[y][1][2])
                        print("Item added to inventory")
                        game[pos[0]][pos[1]][3].pop(0) # Remove key from room
                    case 4:  # Cipher
                        game_time -= int(CIPHER_TIME * score_multiplier)
                        print(f"Selected - {actions[y][1][0]}")
                        note_print(actions[y][1][1])
                # Check if room and action is next hint
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
        except:
            print(f"Not a valid input! Wasted {int(ERR_TIME * score_multiplier)} minutes")
            stats[4] += 1
            game_time -= int(ERR_TIME * score_multiplier)
    # Move if input was movement
    if x:
        stats[1] += 1
        game_time -= int(MOVE_TIME * score_multiplier)
        pos[index] += change
        print(f"Moved {direction} to {ROOM_NAMES[pos[1]][pos[0]]}")
    # Wait for user
    input("    Enter to Continue")
    # Remove over previous line
    print("\033[1A\r                     ")


def check_irene(pos):
    global game_time, score, game_state, stats
    if pos == irene:
        print("=" * 76 + "\n")
        print(f"    You have found the elusive Irene Indiana! There were {game_time//60}h {game_time%60}m to spare")
        # Calculate score
        score += int(IRENE_SCORE * score_multiplier)
        score += int(game_time * TIME_SCORE * score_multiplier)
        print(f"                                    Score: {score}")
        print("\n" + "=" * 76 + "\n")
        # Actually win
        stats[0] -= game_time
        stats[5] += 1
        stats[2] += score
        write_stats()
        game_state = False
    else:
        print(f"You searched for Irene, but it seems she is not here. You wasted {IRENE_TIME} minutes")
        game_time -= IRENE_TIME


def note_print(x):
    global game_time, score, stats
    print("\n - Encrypted Note - \n")
    start_time = time.time()
    text = note_text[x]
    # Maths Mode
    if random.randint(0,2) == 0:
        if random.randint(0,1) == 0:  # Addition
            if score_multiplier <= EASY_MULTIPLY:
                numbers = [random.randint(1,99) for i in range(2)]
            else:
                numbers = [random.randint(100,999) for i in range(2)]
            hint = f"(esc to exit)\n{numbers[0]} + {numbers[1]} = "
            answer = sum(numbers)
        else:  # Multiplication
            if score_multiplier <= EASY_MULTIPLY:
                numbers = [random.randint(2,16) for i in range(2)]
            else:
                numbers = [random.randint(10,99) for i in range(2)]
            hint = f"(esc to exit)\n{numbers[0]} * {numbers[1]} = "
            answer = numbers[0] * numbers[1]
        while True:
            x = input(hint).strip().lower()
            if ',' in x:
                x = "".join(x.split(','))
            if x == str(answer):
                total_time = time.time() - start_time
                print(f"Code cracked in {round(total_time)} seconds!")
                print(f"The note reads |{text}|")
                stats[3] += 1
                score += int(CODE_SCORE * score_multiplier)
                total_time = int(total_time / 6)
                print(f"{total_time} minutes have passed")
                game_time -= total_time
                return
            elif x == 'esc':
                return
            else:
                print("That isn't quite right.")
    # Word Mode
    if score_multiplier > EASY_MULTIPLY:
        a = random.randint(0, 3)
    else:
        a = random.randint(0, 1)
    words = text.split(" ")
    new_string = []
    if a == 0:  # Scramble words in place
        if score_multiplier > EASY_MULTIPLY:
            b = [char for char in text if char != ' ']
            random.shuffle(b)
            i = 0
            for word in words:
                new_string.append("".join(b[i:i+len(word)-1]))
                i += len(word)
            print("Hint: Really Scrambled eggs")
        else:
            for word in words:
                b = [char for char in word]
                random.shuffle(b)
                new_string.append("".join(b))
            print("Hint: Scrambled eggs")
    elif a == 1:  # Fill in the blanks
        letters = ""
        if score_multiplier > EASY_MULTIPLY:
            c = 1
        else:
            c = 3
        for word in words:
            b = ""
            for char in word:
                if random.randint(0, c) == 0:
                    letters += char
                    b += "_"
                else:
                    b += char
            new_string.append(b)
        letters = [char for char in letters]
        random.shuffle(letters)
        letters = "".join(letters)
        print(f"Hint: Some of the letters must have fallen off '{letters}'")
    elif a == 2: # Alphabetical
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
    else: # Numerical
        alpha = sorted("".join(words).lower())
        i = 0
        while i < len(alpha):
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
    print("Enter decrypted phrase (or 'esc' to exit): ")
    while True:
        x = input("> ").lower().strip()
        if x == text.lower().strip():
            total_time = time.time() - start_time
            print(f"Code cracked in {round(total_time)} seconds!")
            stats[3] += 1
            score += int(CODE_SCORE * score_multiplier)
            total_time = int(total_time / 6)
            print(f"{total_time} minutes have passed")
            game_time -= total_time
            return
        elif x == 'esc':
            return
        else:
            print("Incorrect. Enter the decrypted phrase")



# Constants
CREDITS = """

===========================
    Made by Samuel Smith
===========================

"""

HELP = ["""

=====================
      Help & Tips
=====================

'Where in Onslow College is Irene Indiana?' is a grid based puzzle game.
You must follow notes, interrogate teachers and students and crack ciphers
to find Irenes location before the clock runs out.""", """

    MECHANICS

You will have to make a desicion every turn, entered by typing the respective
word or letter into the command line. Every desicion will cost you time.

W - move forward one square on the map
A - move left one square on the map
D - move right one square on the map
S - move down one square on the map

H - Recieve a hint on what you should do next. This will decrease your
score multiplier by 10%, so use it sparingly.
E - Open your inventory. This will list all the items and notes you have collected
use this to track where you have been
ESC - quit the current game and return to this menu
I - Search for Irene Indiana in your current room. This will take a long time
so only do this if you think she is here
""", """

    MAP
    
 _ _ _ _ _
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|X|     Time: 6h 0m left   Current Score: 0

This is your map. It tells you your location in the school (shown by the X)
Your time left and your current score is shown to the right of this map.""",
"""

    CLUES

Most rooms contain clues (in the form of encrypted notes, conversations
with other characters or notes hidden in containers).
These clues lead you to other clue containing rooms. Some rooms can false
clues that use unnecessary certainty in describing Irene's location.
You must follow these clue trails until there are no more leads.
> You have found Irene's location.
Search for her to finish the game and get your score.
"""]

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
    print("Descriptions file is missing. Cannot run. Reinstall game")
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
    ["Talk to English Teacher", "English Teacher: ", ["I thought {} was at {}"], [0, 2]],
    ["Talk to Basketballers", "Basketballer: ", ["I saw {} at {}"], [2, 3]],
    ["Talk to Phys-Ed Teahcer", "Phys-Ed Teahcer: ", ["I might've seen {} around {} before"], [3, 4]]
]

POSSIBLE_NON_CLUE = [
    ["Leave school", ["You decided to stay; you need to find Irene", "You aren't allowed to leave"], [4, 0]],
    ["Talk to student at microwave", ["..."], [1, 3]],
    ["Shoot a hoop", ["You missed.", "The ball bounces of the backboard and hits one of the students in the head. You should go soon"], [3, 4]],
    ["Talk to the magpies", ["... (birds can't speak)"], [4, 4]]
]

# [['container desc', 'open attempt', 'open', [locx, locy], reward_funct],
# ['key desc', 'pick up key', [locx, locy]]]
POSSIBLE_CONTAINER = [
    ["Open Shipping Container", "Cannot open, the old rusty lock wont budge",
     "The acid dissolved the rusty latch and the door swings open", 'container_note', [0, 0],
     ["Acid (could be used to dissolve metal or remove rust)", "Picked up acid (don't spill it)", 'acid', [1,0]]],
    ["Talk to hooded kid", "He ignores you, entirely obsessed with the comforting glow of his smartphone",
     "The smell of the lollies, tantalisingly sweet and delicous, fills the air. The hooded kid notices and glances up.\
He gives you a note.", 'kid_note', [0, 1],
      ["A dollar bag of lollies (could be used to bribe children)", "You pay for the dollar bag and put it in your pocket", 'lollies', [0, 4]]],
    ["A battered silver car, parked on a horrific angle, sits at the edge of the carpark. Could it contain a secret?", "You try the boot, but it's locked.",
      "You open the boot and find a note", 'car_note', [4, 0],
      ["Car keys with the same logo as the car in the carpark",
      "You picked up the car keys and quietly slid them into your pocket", 'car_keys', [4, 1]]],
    ["A freshly disturbed patch of dirt lies in the middle of the field. Could something be hidden underneath?", "Need something to dig with", 
    "You dig up a small wooden box with a note inside", "dirt_note", [4,4],
        ["Spade (could be used to dig holes)", "Picked up the spade", "spade", [2,1]]]
]

POSSIBLE_CIPHER = [
    ["Engraved stone", "note"],
    ["Paper slip", "note1"],
    ["Letter", "note2"],
    ["Sticky note", "note3"],
    ["Handwritten Note", "note4"],
    ["Folded note", "note5"],
    ["Crumpled Note", "note6"],
    ["Late slip", "note7"],
    ["Paper plane", "note8"],
    ["Origami Crane", "note9"],
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
    [True, False, True, False, False],
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
SPEAK_CHANCE = [0.5, 0.9]
CONTAINER_CHANCE = [0.8, 0.95]
CIPHER_CHANCE = [0.4, 0.9]

NEXT_STEP_SCORE = 50
CODE_SCORE = 10
IRENE_SCORE = 1000
TIME_SCORE = 1

# assuming roughly 40 minutes per room (if speedrunning on easy)
EASY_TIME = 37
HARD_TIME = 74
TIME_RANGE = 30

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
# Time, moves, score, deciphers, errors, games
stats = [0, 0, 0, 0, 0, 0]
crossiant = [[0,0], False]

game_state = False
game_loop = True

while game_loop:
    if not game_state:
        main_menu()
    else:
        action_menu()


print("\nThanks for playing 'Where in Onslow College is Irene Indiana?'")
