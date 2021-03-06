##
# MapGenerator.py
# 16/06/2022
# SamuelSmith
# Generates a simple map to move around in

SIZE_X = 5
SIZE_Y = 5
ISIZE_Y = SIZE_Y - 1
ISIZE_X = SIZE_X - 1

pos = [0,0]

ROOMS = [['Top field', 'Chemistry classrooms', 'Science hallway',
          'Maths corridor', 'Student carpark'],
         ['Old Skatebowl', 'Physics classrooms', 'Garden',
          'Digital Tech classes', 'Art department'],
         ['English block', 'Library', 'Social Sciences',
          'Accounting & Business', 'Hall'],
         ['Rear driveway', 'Student Centre', 'Quad', 'Main Driveway',
          'Design Tech'],
         ['Dairy', 'Table mountain: (main)', 'Table mountain (far)',
          'Gym','Bottom field']]

DESCRIPTIONS = [["A group of students, mostly dressed in athletic clothing except for the one kid who is wearing jeans and a sweatshirt, are sprinting around the track. The teacher stands on the very far end of the field, holding a stopwatch. The students are now only 10 metres away.",
                "Students line the benches, discussing several different colourless flasks. Glassware sits precariously atop stands, handled by students whose safety glasses are entirely covered in fog from their masks.",
                "The science hallway is empty. A drop of water lands on your shoulder, the roof still leaking. There are cones in front of the bathrooms here, vandalised one too many times for the hundredth time.",
                "You stand in the middle of the maths corridor. You can see all the teachers scribbling all sorts of equations on the board. You see that some students are on their phones and some are half-asleep.",
                "You stand at the entrance to the student carpark. A bunch of old cheap cars and a couple of scooters are parked here. You can see Raroa Intermediate and some kids running around on their field. At the far end of the carpark, someone is setting up a Christmas tree shop. It's still August."],
                ["You stand on the grass field that was once a skate bowl. You can see the old court and the shattered glass that covers the cracked concrete. Some kid with his hood up stands nearby staring at his phone. It doesn't seem like anyone else is here.",
                "The students are standing around some elaborate setup of strings, weights, pulleys and springs. Some of them are holding stopwatches and the board is covered in complex equations. The teacher is absent.",
                "You stand in the garden between the science department and the IT department. There are a couple of birds hopping about on the roofs.",
                "Students are noisily typing away at the computers which cover the desks. They are all talking and laughing or explaining some piece of code.",
                "You stand in the corner of the room. Students sit in pairs or threes and chat while they draw assorted items lining the centre of the long desks. The teacher is busy printmaking. The dark room is closed but you can hear someone in there. (make sometimes you catch Irene and sometimes you ruin someone's film)"],
                ["Students sit at their laptops, typing away at some essay. The teacher looks up at you.",
                "The library is quiet. Some students wander up and down the isles, occasionally pulling out a book and flipping through some of the pages. One of the computers is free.",
                "You silently enter the social sciences classroom. The teacher is in the middle of a history presentation. You stand quietly in the corner.",
                "The students are busy poring over sheets of numbers. The teacher looks up at you and motions for you to wait before returning to a conversation with one of the students.",
                "You stand in the hall. There is a student in the corner setting up some audio system, looking incredibly confused and surrounded by a mess of cables. The benches have been laid out. There must be some presentation this afternoon."],
                ["A few pieces of garbage tumble around in circles from the wind. You can see the road leading down to the dairy and hear the construction of one of the neighbouring houses. You should get moving.",
                "There is a teacher seated at a table with a few students, quietly chatting away. Another student waits at the microwave, staring deep into the pale glow. You can't make out what they are heating, but it looks like it is steaming.",
                "A few students mill around, sinking some shots. You wonder whether they're allowed to be out here during class time. You can see that your bike is still locked up at the other end of the quad and you can't wait to go home.",
                "You stand on the main driveway, the buses not due for at least another hour. You should get moving.",
                "Students bend over the workpieces busying themselves with tools. You can see the teacher in the machine room, occupied with the table saw. The room is rife with deafening hammer strikes and the whir of power tools and you consider grabbing some earmuffs but decide against it."],
                ["The dairy, a forbidden place, stands before you, the hot chips and pies reaching out their inviting smell. You can still hear the chatter of the students from back at the school, reminding you that you aren't supposed to leave the school grounds. Better hurry back soon.",
                "You stand atop table mountain (really just some classrooms on a small flat hill). There isn't anyone in sight, but you can hear a teacher in one of the classrooms.",
                "You stand on the far end of table mountain, on the wooden decking between the classrooms. A small group of pine trees tower above you. It is deadly silent.",
                "The gym is noisy with shouts and shoes scuffing on the wood floor, a class busy playing dodgeball. The teacher doesn't notice you, watching the game carefully. You flinch, a dodgeball narrowly missing your face.",
                "The bottom field is vacant, apart from a few magpies. You can see cars and trucks rushing past the other side of the fence. A section of the field is fenced off, new grass seed having just been planted"]]


def display(pos):
    for y in range(ISIZE_Y, -1, -1):
        string = ""
        for x in range(SIZE_X):
            if [x,y] == pos:
                string += "##"
            else:
                string += "_|"
        if y == 0:
            string += " - " + ROOMS[pos[1]][pos[0]]
        print(string)

display(pos)
while True:
    print(" =================== ")
    print(DESCRIPTIONS[pos[1]][pos[0]])
    ans = input("> ")
    if ans == 'q':
        break
    if ans == 'w' and pos[1] < ISIZE_Y:
        index, change, direction = 1, 1, 'north'
    elif ans == 's' and pos[1] > 0:
        index, change, direction = 1, -1, 'south'
    elif ans == 'a' and pos[0] > 0:
        index, change, direction = 0, -1, 'east'
    elif ans == 'd' and pos[0] < ISIZE_X:
        index, change, direction = 0, 1, 'west'
    else:
        print("Not a valid input!")
        display(pos)
        continue
    pos[index] += change
    print(f"Heading {direction}")
    display(pos)

