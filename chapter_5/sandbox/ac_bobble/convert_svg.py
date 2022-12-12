import numpy as np
import xml.etree.ElementTree as ET


def convert(svg_filename, ids):
    tree = ET.parse(svg_filename)
    root = tree.getroot()

    for element in root.iter("*"):
        path_id = element.get("id")
        if path_id in ids:
            points = get_path(element)
            save_path(points, path_id)


def get_path(element):
    d_list = element.get("d").split(" ")

    points = []
    last_x = 0
    last_y = 0
    last_command = "m"
    absolute = True
    horizontal = False
    vertical = False

    # TODO: properly handle c and q elements (curves)
    for d_element in d_list:
        if d_element in [
            "M",
            "L",
            "H",
            "V",
            "C",
            "S",
            "Q",
            "T",
            "A",
            "Z",
        ]:
            absolute = True
            last_command = d_element
            continue
        if d_element in [
            "m",
            "l",
            "h",
            "v",
            "c",
            "s",
            "q",
            "t",
            "a",
            "z",
        ]:
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

    return points


def save_path(points_list, path_id):
    points = np.array(points_list)

    # Convert from pts to inches
    scale = 72
    points = points / scale

    # Flip the path vertically to account for the mouse coordinate system
    # of "positive y is lower down the screen"
    points[:, 1] = -1 * points[:, 1]

    path_filename = path_id + ".npy"
    np.save(path_filename, points)
    print(f"Path with {points[:, 1].size} points saved as {path_filename}")
