"""
In the process of writing this chapter, I tried my hand at writing
an svg-to-numpy path converter. The result is this clunky snippet.

Things I like about it:
* It cycles through all paths in the svg and writes each path to
    a Numpy .npy data file as a 2D array.
* It centers each path over (0, 0), and scales it to fall within
    a few units of the origin.

Things I don't like about it:
* I haven't tested it on anything but one Inkscape-generated svg.
* I ignore all svg curve commands and substitute straight lines instead.
* The logic feels kind of ham-fisted.


For context, here's the rest of the animation chapter:
https://brandonrohrer.com/httyr4
"""
import numpy as np
import xml.etree.ElementTree as ET

svg_filename = 'drawing.svg'


def main():
    tree = ET.parse(svg_filename)
    root = tree.getroot()

    for element in root.iter('*'):
        if element.tag[-4:] == "path":
            path_id = element.get("id")
            d_list = element.get("d").split(" ")

            points = []
            last_x = 0
            last_y = 0
            last_command = "m"
            absolute = True
            horizontal = False
            vertical = False

            for d_element in d_list:
                if d_element in [
                        "M", "L", "H", "V", "C", "S", "Q", "T", "A", "Z"]:
                    absolute = True
                    last_command = d_element
                    continue
                if d_element in [
                        "m", "l", "h", "v", "c", "s", "q", "t", "a", "z"]:
                    absolute = False
                    last_command = d_element
                    continue

                if last_command in ["h", "H"]:
                    horizontal = True
                else:
                    horizontal = False

                if last_command in ["v", "V"]:
                    vertical = True
                else:
                    vertical = False

                if horizontal:
                    if absolute:
                        x = float(d_element)
                    else:
                        x = last_x + float(d_element)

                elif vertical:
                    if absolute:
                        y = float(d_element)
                    else:
                        y = last_y + float(d_element)

                else:
                    # Hack: Treat all curves like "line_to" commands.
                    x_str, y_str = d_element.split(",")
                    if absolute:
                        x = float(x_str)
                        y = float(y_str)
                    else:
                        x = last_x + float(x_str)
                        y = last_y + float(y_str)

                points.append([x, y])
                last_x = x
                last_y = y

            save_path(points, path_id)


def save_path(points_list, path_id):
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

    # Flip the path vertically to account for the mouse coordinate system
    # of "positive y is lower down the screen"
    points[:, 1] = -1 * points[:, 1]

    path_filename = path_id + ".npy"
    np.save(path_filename, points)
    print(f"Path with {points[:, 1].size} points saved as {path_filename}")


main()
