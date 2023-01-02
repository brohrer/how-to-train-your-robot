import numpy as np

try:
    from svg.path import parse_path
    from svg.path.path import Line, CubicBezier, QuadraticBezier, Arc, Move
    import xml.etree.ElementTree as ET

    IMPORT_SUCCESS = True
except ModuleNotFoundError:
    IMPORT_SUCCESS = False


VERBOSE = False
POINTS_PER_LENGTH = 1 / 30
MIN_POINTS = 4
MAX_POINTS = 72


def convert(svg_filename, ids):
    if not IMPORT_SUCCESS:
        return

    tree = ET.parse(svg_filename)
    root = tree.getroot()

    for element in root.iter("*"):
        path_id = element.get("id")
        if path_id in ids:
            points = get_path(element)
            save_path(points, path_id)


def get_path(element):
    element_d = element.get("d")
    paths = parse_path(element_d)

    points = []
    for path in paths:
        # Handle each path type
        if isinstance(path, Move) or isinstance(path, Line):
            complex_point = path.end
            points.append([complex_point.real, complex_point.imag])

        if (
            isinstance(path, CubicBezier)
            or isinstance(path, QuadraticBezier)
            or isinstance(path, Arc)
        ):
            n_pts = int(POINTS_PER_LENGTH * path.length())
            n_pts = np.minimum(np.maximum(n_pts, MIN_POINTS), MAX_POINTS)
            pts = np.linspace(0, 1, n_pts + 1)
            for pt in pts[1:]:
                complex_point = path.point(pt)
                points.append([complex_point.real, complex_point.imag])
    return points


def save_path(points_list, path_id):
    points = np.array(points_list)

    # Make this smaller
    scale = 720
    points = points / scale

    # Flip the path vertically to account for the mouse coordinate system
    # of "positive y is lower down the screen"
    points[:, 1] = -1 * points[:, 1]

    path_filename = path_id + ".npy"
    np.save(path_filename, points)

    if VERBOSE:
        print(f"Path with {points[:, 1].size} points saved as {path_filename}")


if __name__ == "__main__":
    convert("flybot.svg", ["head"])
