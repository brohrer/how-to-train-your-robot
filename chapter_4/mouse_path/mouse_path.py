"""
Convert mouse clicks and drags to a path.

Run script with sudo.

TODO: Test with Mac
"""
import time
import mouse
import numpy as np
from pacemaker import Pacemaker


def main():
    pacemaker = Pacemaker(24)  # Hz
    last_x = -9999
    last_y = -9999
    points = []

    while True:
        # Read mouse clicks and drags
        (x, y) = mouse.get_position()
        if x != last_x and y != last_y and mouse.is_pressed(button="right"):
            last_x = x
            last_y = y
            points.append([x, y])
            print(f"{x}, {y}")

        if mouse.is_pressed(button="left"):
            save_path(points)
            last_x = -9999
            last_y = -9999
            points = []

        pacemaker.beat()


def save_path(points_list):
    points = np.array(points_list)

    # Needs at least 2 points to make a path
    if points.size < 4:
        return

    # Center the points over (0, 0)
    points = points - np.mean(points, axis=0)

    # Scale the points so that they fall within a few units of (0, 0).
    # Mean distance of a point from the origin is 1.
    distances = np.sqrt(points[:, 0] ** 2 + points[:, 1] ** 2)
    scale = np.mean(distances)
    points = points / (scale + 1e-6)

    path_filename = "path_" + str(int(time.time())) + ".npy"
    np.save(path_filename, points)
    print(f"Path with {points[:, 1].size} points saved as {path_filename}")


main()
