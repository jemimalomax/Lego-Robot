#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
import sys
# motor declarations
drive = MoveTank(OUTPUT_B, OUTPUT_C)
mLeft = LargeMotor(OUTPUT_B)
mRight = LargeMotor(OUTPUT_C)
# sensor declarations
us = UltrasonicSensor()
sound = Sound()
us.mode = 'US-DIST-CM'
cs = ColorSensor()
cs.mode = "COL-REFLECT"

# threshold values for line area
BLACK_CS_VALUE = 16
WHITE_CS_VALUE = 48


# Correct when travelling along strip
def correct():
    left_rotations = 0
    right_rotations = 0
    # Find min of rotations to get off grey to the right and 0.6
    while not BLACK_CS_VALUE < cs.value() < WHITE_CS_VALUE and left_rotations < 0.6:
        mLeft.on_for_rotations(SpeedPercent(12), 0.1)
        left_rotations += 0.1
    # Return to centre
    mLeft.on_for_rotations(SpeedPercent(12), -left_rotations)
    # Find min of rotations to get off grey to the left and 0.6
    while not BLACK_CS_VALUE < cs.value() < WHITE_CS_VALUE and right_rotations < 0.6:
        mRight.on_for_rotations(SpeedPercent(12), 0.1)
        right_rotations += 0.1
    # Return to centre
    mRight.on_for_rotations(SpeedPercent(12), -right_rotations)
    # Average results
    if left_rotations < right_rotations:
        mRight.on_for_rotations(SpeedPercent(12), (right_rotations - left_rotations) / 2)
    elif right_rotations < left_rotations:
        mLeft.on_for_rotations(SpeedPercent(12), (left_rotations - right_rotations) / 2)


# Correct when changing rows, similar process to correct method, but with smaller rotations and minimised
# adjustment
def correct_column():

    left_rotations = 0
    right_rotations = 0

    while cs.value() < WHITE_CS_VALUE and left_rotations < 0.6:
        mLeft.on_for_rotations(SpeedPercent(12), 0.075)
        left_rotations += 0.075

    mLeft.on_for_rotations(SpeedPercent(12), -left_rotations)

    while cs.value() < WHITE_CS_VALUE and right_rotations < 0.6:
        mRight.on_for_rotations(SpeedPercent(12), 0.075)
        right_rotations += 0.075

    mRight.on_for_rotations(SpeedPercent(12), -right_rotations)

    # Adjust, but only partially, to prevent too severe of an angle
    if left_rotations < right_rotations:
        mRight.on_for_rotations(SpeedPercent(12), (right_rotations - left_rotations) / 4)
    elif right_rotations < left_rotations:
        mLeft.on_for_rotations(SpeedPercent(12), (left_rotations - right_rotations) / 4)


# Forward to black-white stripe
drive.on_for_rotations(SpeedPercent(15), SpeedPercent(15), 0.7)

# Should be on start tile
tile = 1
sound.speak(str(tile))

# Turn right
mLeft.on_for_rotations(SpeedPercent(12), .985)
# Adjust
drive.on_for_rotations(SpeedPercent(12), SpeedPercent(12), -0.1)

# Up to tile 11
for i in range(10):
    # Head forwards while on black
    while cs.value() < WHITE_CS_VALUE:
        drive.on(20, 20)

    drive.on_for_rotations(SpeedPercent(15), SpeedPercent(15), 0.2)
    correct()
    # Head forwards while on white
    while cs.value() > BLACK_CS_VALUE:
        drive.on(20, 20)
    drive.on_for_rotations(SpeedPercent(15), SpeedPercent(15), 0.2)
    # Have reached a black tile
    tile += 1
    sound.speak(str(tile))
    correct()

# Should be at tile 11 - turn right, reverse and correct
drive.on_for_rotations(SpeedPercent(15), SpeedPercent(15), -0.1)
mLeft.on_for_rotations(SpeedPercent(12), 0.985)
drive.on_for_rotations(SpeedPercent(15), SpeedPercent(15), -0.5)
correct_column()

# Up to tile 41 i.e. traverse two big tiles
for i in range(2):
    while cs.value() < BLACK_CS_VALUE:
        drive.on(5, 5)
    drive.off()
    drive.on_for_rotations(SpeedPercent(15), SpeedPercent(15), 0.1)
    while cs.value() > BLACK_CS_VALUE:
        drive.on(5, 5)
    drive.off()
    drive.on_for_rotations(SpeedPercent(15), SpeedPercent(15), 0.1)
    tile += 15
    sound.speak(str(tile))
    drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), -.05)
    correct_column()
ninetyTurn = .985
mRight.on_for_rotations(SpeedPercent(12), ninetyTurn)
drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), -.15)
mLeft.on_for_rotations(SpeedPercent(12), ninetyTurn)
drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), -.3)
# TOWER AREA SECTION
rowAdjust = False
first = mLeft

# Rotations to turn 90 degrees

# How many rotations to go back as an adjustment
backDistance = -0.33
# Variable to adjust speed easily
speed = 40
# Colour boundary values
# if we figure out how to not consider grout as black tiles, we can raise this threshold to 20
BLACK_CS_VALUE = 18.0
GREY_CS_VALUE = 22
WHITE_CS_VALUE = 40

# Initial tile number
black_tile_num = 41

# Initial big tile tower could be in
big_tile = 0
tiles = 0


# Method to travel between rows in tower area
def straight_up_column():
    global big_tile
    global rowAdjust
    global black_tile_num
    global first
    # Backwards adjustment
    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -backDistance)
    # Get off black tile onto grey
    while cs.value() <= BLACK_CS_VALUE:
        while cs.value() <= BLACK_CS_VALUE:
            drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .2)
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .15)
    # Get off grey tile onto next black
    while cs.value() > BLACK_CS_VALUE:
        while cs.value() > BLACK_CS_VALUE:
            drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .1)
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .2)
    # Update count
    black_tile_num = black_tile_num + 15
    sound.speak(str(black_tile_num))


# Scan a range of angles to find one that points most directly to tower
def find_direction(turn):
    global rowAdjust
    global black_tile_num
    global first
    global big_tile
    current_us = us.value()
    angleRotations = 0
    # Check 15 angles to the left by rotating and then checking
    for q in range(15):
        mLeft.on_for_rotations(SpeedPercent(20), turn)
        # Update smallest ultrasonic value if applicable and save rotation amount
        if us.value() < current_us:
            current_us = us.value()
            angleRotations = q
    # Go back to initial angle
    for q in range(15):
        mLeft.on_for_rotations(SpeedPercent(20), -turn)
    # Repeat process for left
    for q in range(15):
        mRight.on_for_rotations(SpeedPercent(20), turn)
        if us.value() < current_us:
            current_us = us.value()
            angleRotations = -q
    # Angle is such that robot probably crosses to another grey tile to get to tower
    if angleRotations >= 3:
        big_tile = big_tile + 1
    if angleRotations <= -3:
        big_tile = big_tile - 1
    sound.speak("Rotations" + str(angleRotations))
    # Go back to initial angle
    for q in range(15):
        mRight.on_for_rotations(SpeedPercent(20), -turn)
    sound.speak("go to angle")
    # Go to best angle
    if angleRotations > 0:
        for q in range(angleRotations):
            mLeft.on_for_rotations(SpeedPercent(20), turn)
    else:
        for q in range(-angleRotations):
            mRight.on_for_rotations(SpeedPercent(20), turn)


# Method for once tower has spotted
def found():
    global rowAdjust
    global black_tile_num
    global big_tile
    global first
    # Find optimal large angle
    find_direction(.06)
    # Find optimal sub-angle
    find_direction(.025)
    # If we are not close to the tower
    if us.value() > 220:
        # Go forward one rotation, in 2 parts.
        for q in range(2):
            # Head towards tower
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), .5)
            # Update black tile count if going over stripe
            if cs.value() <= BLACK_CS_VALUE:
                drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), .1)
                if cs.value() <= BLACK_CS_VALUE and not rowAdjust:
                    black_tile_num = black_tile_num + 15
                    sound.speak(black_tile_num)
                    rowAdjust = True
            if cs.value() >= WHITE_CS_VALUE:
                drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), .1)
                if cs.value() >= WHITE_CS_VALUE and not rowAdjust:
                    black_tile_num = black_tile_num + 15
                    sound.speak(black_tile_num)
                    rowAdjust = True
        # If we still aren't close enough, call function again
        if us.value() > 220:
            found()
    # If we are closer than 22 cm, go forward for half a rotation
    drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 0.5)
    # Report final tower
    sound.beep()
    for a in range(3):
        sound.speak("Big tile" + str(big_tile))
    # End loop
    sys.exit()


# Row iteration for tower area.
def current_row(towards, away, direction):
    global black_tile_num
    global big_tile
    global rowAdjust
    # Need to do for 3 grey tiles in each row
    for q in range(3):
        big_tile = big_tile + 1 * direction
        # If tower is sufficiently close
        if us.value() < 700:
            sound.speak("tower spotted")
            # Not the closest tile
            if us.value() > 400:
                rowAdjust = True
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), .3)
            found()

        # if the robot cannot sense the tower directly ahead, rotate left 90 degrees
        # if it is currently on a black square, go forwards until it is on white again and set the colour to white
        elif q < 2:
            sound.speak("could not see tower")
            global tiles
            tiles = 0
            # Back off grey back to strip
            if BLACK_CS_VALUE + 3 < cs.value() < WHITE_CS_VALUE - 3:
                while BLACK_CS_VALUE + 3 < cs.value() < WHITE_CS_VALUE - 3:
                    drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), -.1)
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), -.3)
            # Check whether on white tile
            if cs.value() > WHITE_CS_VALUE:
                initialColor = True
            else:
                initialColor = False
            drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -.05)
            # Back off grey if necessary
            while BLACK_CS_VALUE < cs.value() < WHITE_CS_VALUE:
                drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), backDistance)

            towards.on_for_rotations(SpeedPercent(50), ninetyTurn)
            # Check if colour has changed
            if cs.value() > WHITE_CS_VALUE:
                currentColor = True
            else:
                currentColor = False
            # Update black tile number manually, as otherwise not picked up
            if initialColor is True and currentColor is False:
                tiles = 1
                black_tile_num = black_tile_num + direction * 1
                sound.speak(str(black_tile_num))
            # While not at a middle tile
            while tiles < 3:
                # Go forward while on black
                while cs.value() < BLACK_CS_VALUE:
                    while cs.value() < BLACK_CS_VALUE:
                        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .1)
                    # If on black
                    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .15)
                # Update count of strip tile
                tiles = tiles + 1
                # If not at final grey tile of row
                if tiles < 4:
                    # Go forward on black, update black tile counter
                    if cs.value() <= BLACK_CS_VALUE:
                        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .1)
                        if cs.value() <= BLACK_CS_VALUE:
                            black_tile_num = black_tile_num + direction * 1
                            sound.speak(str(black_tile_num))
                # Otherwise, go forwards while on black
                while cs.value() > BLACK_CS_VALUE and tiles < 3:
                    while cs.value() > BLACK_CS_VALUE:
                        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .1)
                    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .15)
                # Update black tile count
                if tiles < 3:
                    tiles = tiles + 1
                    black_tile_num = black_tile_num + direction * 1
                    sound.speak(str(black_tile_num))

            # Turn
            away.on_for_rotations(SpeedPercent(100), ninetyTurn)
            # Reverse
            drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), backDistance)
            # Update stripe tile count
            tiles = tiles + 1
            if q == 2:
                return


# Move forward further onto black tile
drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), .2)
# row 1
current_row(mRight, mLeft, 1)
# Reverse adjustment
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -.3)

mRight.on_for_rotations(SpeedPercent(40), ninetyTurn)
sound.speak("next black")
# Go to black tile
while cs.value() > BLACK_CS_VALUE:
    while cs.value() > BLACK_CS_VALUE:
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(20), .1)
    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -.05)
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(20), .15)
# Face forwards
mLeft.on_for_rotations(SpeedPercent(100), ninetyTurn)
# Go to next row
straight_up_column()
# Big tile count changes by 3, but will be decremented shortly, so increase by 4 here
big_tile = big_tile + 4
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .15)
mLeft.on_for_rotations(SpeedPercent(40), ninetyTurn)
while cs.value() <= BLACK_CS_VALUE:
    while cs.value() <= BLACK_CS_VALUE:
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .1)
    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .1)
mRight.on_for_rotations(SpeedPercent(40), ninetyTurn)
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), backDistance)
# row 2
current_row(mLeft, mRight, -1)
# Adjustment
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -.18)
# Turn towards next black tile
mLeft.on_for_rotations(SpeedPercent(40), ninetyTurn)
# Go to black tile
sound.speak("next black")
while cs.value() > BLACK_CS_VALUE:
    while cs.value() > BLACK_CS_VALUE:
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(20), .1)
    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -.05)

drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(20), .15)
# Face forwards and move up to next row
mRight.on_for_rotations(SpeedPercent(100), ninetyTurn)
straight_up_column()
# Will shortly be incremented by 1, so will increment by 2 instead of 3
big_tile = big_tile + 2
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -.2)
# Turn towards centre of strip for the 3 big grey tiles.
mRight.on_for_rotations(SpeedPercent(40), ninetyTurn)
# Go forwards until on white
while cs.value() <= BLACK_CS_VALUE:
    while cs.value() <= BLACK_CS_VALUE:
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .15)
    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .15)
# Turn to face forwards
mLeft.on_for_rotations(SpeedPercent(40), ninetyTurn)
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -backDistance - .15)
# row 3
current_row(mRight, mLeft, 1)
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -.18)
mRight.on_for_rotations(SpeedPercent(40), ninetyTurn)
# Go to next black tile for easier column travel
sound.speak("next black")
while cs.value() > BLACK_CS_VALUE:
    while cs.value() > BLACK_CS_VALUE:
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(20), .1)
    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), -.05)
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(20), .15)
mLeft.on_for_rotations(SpeedPercent(100), ninetyTurn)
# Face forwards
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), backDistance)
# Get off strip onto grey
while cs.value() <= BLACK_CS_VALUE:
    while cs.value() <= BLACK_CS_VALUE:
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .2)
    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .15)
# Get off grey onto next strip
while cs.value() > BLACK_CS_VALUE:
    while cs.value() > BLACK_CS_VALUE:
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .1)
    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .15)
black_tile_num = black_tile_num + 15
sound.speak(str(black_tile_num))
# Big tile count changes by 3, but will be decremented shortly, so increase by 4 here
big_tile = big_tile + 4
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .15)
# Turn into row
mLeft.on_for_rotations(SpeedPercent(40), ninetyTurn)
# Go over black to white tile
while cs.value() <= BLACK_CS_VALUE:
    while cs.value() <= BLACK_CS_VALUE:
        drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .1)
    drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), .1)
# Face forwards
mRight.on_for_rotations(SpeedPercent(40), ninetyTurn)
drive.on_for_rotations(SpeedPercent(speed - 20), SpeedPercent(speed - 20), backDistance)
# row 4
current_row(mLeft, mRight, -1)
# Report tile 9 as a last resort, as no other tile name has been said
sound.beep()
sound.speak("tile 9")
