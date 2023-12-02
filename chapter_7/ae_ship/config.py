import numpy as np
import logging


# Time control
CLOCK_FREQ_SIM = 500  # Hertz
CLOCK_PERIOD_SIM = 1 / float(CLOCK_FREQ_SIM)  # seconds
CLOCK_FREQ_VIZ = 30  # Hertz
CLOCK_FREQ_DASH = 4  # Hertz
CLOCK_FREQ_RUN = 4  # Hertz
HEARTBEAT_FREQ_KEYS = 4  # Hertz
ALIVE_CHECK_FREQ = 1  # Hertz

# Logging settings
LOGGING_LEVEL_SIM = logging.ERROR
LOGGING_LEVEL_VIZ = logging.ERROR
LOGGING_LEVEL_DASH = logging.INFO

KEYPRESS_REFRACTORY_PERIOD = 0.2  # seconds

############################################
#
# Configuration parameters for the simulation

WORLD_WIDTH = 7
WORLD_HEIGHT = 5.5

GRAVITY = 0.0

force_duration = 0.25  # seconds
FORCE_SHAPE = np.ones(int(force_duration * CLOCK_FREQ_SIM))

# Initialize crystals
atom_stiffness = 3e3
sliding_friction = 0.2
inelasticity = 0.1

WHITE = "#f8f8f8"
BLACK = "#000000"

body_scale = 0.2

POLY_PATHS = {}
POLY_PATHS["ship"] = body_scale * np.array(
    [
        [-0.47,	0.61],
        [-0.27,	0.50],
        [-0.27,	-0.50],
        [-0.47,	-0.61],
        [1.02,	0.00],
    ]
)

POLY_PATHS["thrust"] = body_scale * np.array(
    [
        [-0.31,	-0.21],
        [-0.80,	0.00],
        [-0.31,	0.21],
    ]
)

POLY_PATHS["a0"] = body_scale * np.array(
    [
        [-1.89,	-0.29],
        [-0.53,	-1.89],
        [0.40,	-1.59],
        [0.45,	-2.70],
        [2.41,	-1.89],
        [3.12,	0.12],
        [2.57,	1.79],
        [1.53,	2.30],
        [-0.48,	1.76],
        [-0.95,	0.87],
        [-0.31,	0.16],
    ]
)

POLY_PATHS["a00"] = body_scale * np.array(
    [
        [0.69, -1.84],
        [1.11, -0.75],
        [0.52, 0.92],
        [-0.51, 1.44],
        [-0.98, 1.31],
        [-0.85, -1.09],
    ]
)

POLY_PATHS["a01"] = body_scale * np.array(
    [
        [-1.54, -0.75],
        [-0.75, -1.67],
        [1.55, -0.69],
        [1.43, 1.72],
        [-0.12, 1.29],
        [-0.59, 0.40],
        [0.05, -0.30],
    ]
)

POLY_PATHS["a02"] = body_scale * np.array(
    [
        [-1.91, 0.29],
        [-1.31, -0.40],
        [-0.40, -0.09],
        [-0.33, -1.21],
        [1.61, -0.39],
        [1.95, 0.51],
        [0.40, 1.27],
    ]
)

GAME_LINEWIDTH = 2

FACECOLOR = {
    "ship": BLACK,
    "a0": BLACK,
    "a00": BLACK,
    "a01": BLACK,
    "a02": BLACK,
}

EDGECOLOR = {
    "ship": WHITE,
    "a0": WHITE,
    "a00": WHITE,
    "a01": WHITE,
    "a02": WHITE,
}

# params arrays have columns [x, y, radius, mass]
atom_params = {}
atom_params["ship"] = np.array(
    [[body_scale, body_scale, body_scale, 1.0]]
) * np.array(
    [
        [-0.37, -0.50, 0.15, 0.07],
        [-0.37, 0.50, 0.15, 0.07],
        [-0.13, -0.19, 0.28, 0.25],
        [-0.13, 0.19, 0.28, 0.25],
        [0.30, 0.00, 0.28, 0.25],
        [0.72, 0.00, 0.15, 0.07],
    ]
)

atom_params["a0"] = np.array(
    [[body_scale, body_scale, body_scale, 1.0]]
) * np.array(
    [
        [-1.63,	-0.36,	0.19,	0.09],
        [-1.12,	-0.52,	0.48,	0.36],
        [-0.27,	-0.80,	1.00,	2.33],
        [0.54,	-2.57,	0.15,	0.05],
        [0.77,	-2.22,	0.38,	0.23],
        [1.14,	-1.61,	0.79,	0.64],
        [1.68,	-1.18,	0.97,	0.97],
        [1.63,	0.11,	1.47,	3.39],
        [1.40,	0.79,	1.47,	3.39],
        [0.11,	1.02,	0.90,	1.26],
        [-0.52,	0.93,	0.38,	0.23],
    ]
)

atom_params["a00"] = np.array(
    [[body_scale, body_scale, body_scale, 1.0]]
) * np.array(
    [
        [0.41, -1.30, 0.27, 0.11],
        [0.18, -0.70, 0.71, 0.78],
        [0.70, -0.53, 0.27, 0.11],
        [0.45, -0.21, 0.40, 0.25],
        [-0.44, -0.51, 0.61, 0.58],
        [-0.19, 0.20, 0.88, 1.20],
        [-0.49, 0.92, 0.61, 0.58],
        [0.06, 0.87, 0.40, 0.25],
        [-0.72, 1.26, 0.40, 0.25],
    ]
)

atom_params["a01"] = np.array(
    [[body_scale, body_scale, body_scale, 1.0]]
) * np.array(
    [
        [-1.60, -0.83, 0.09, 0.02],
        [-1.34, -0.90, 0.24, 0.13],
        [-0.78, -1.07, 0.55, 0.71],
        [-0.23, -0.88, 0.53, 0.52],
        [0.32, -0.64, 0.53, 0.52],
        [0.86, -0.41, 0.53, 0.65],
        [0.36, 0.49, 0.96, 2.15],
        [-0.51, 0.40, 0.24, 0.09],
        [0.73, 0.97, 0.57, 0.51],
        [0.97, 1.30, 0.33, 0.17],
        [1.19, 1.60, 0.09, 0.03],
    ]
)

atom_params["a02"] = np.array(
    [[body_scale, body_scale, body_scale, 1.0]]
) * np.array(
    [
        [-1.65, 0.25, 0.17, 0.09],
        [-1.16, 0.12, 0.46, 0.49],
        [-0.72, 0.30, 0.49, 0.55],
        [-0.17, -0.99, 0.17, 0.09],
        [0.08, -0.58, 0.46, 0.33],
        [0.54, 0.18, 0.97, 1.48],
        [0.31, 0.43, 0.78, 0.94],
        [1.30, -0.05, 0.46, 0.33],
        [1.48, 0.32, 0.43, 0.29],
    ]
)

SHIP_BODY = {
    "id": "ship",  # There will only ever be one.
    "type": "ship",
    "color": WHITE,
    "x": 1,
    "y": 2,
    "v_x": 0.5 - np.random.sample(),
    "v_y": 0.5 - np.random.sample(),
    "v_rot": 0.5 - np.random.sample(),
    "x_atoms": atom_params["ship"][:, 0],
    "y_atoms": atom_params["ship"][:, 1],
    "r_atoms": atom_params["ship"][:, 2],
    "m_atoms": atom_params["ship"][:, 3],
    "stiffness_atoms": atom_stiffness,
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}

A0_BODY = {
    "type": "a0",
    "x": 3,
    "y": 5,
    "v_x": 0.5 - 3 * np.random.sample(),
    "v_y": 0.5 - 3 * np.random.sample(),
    "v_rot": 0.5 - 3 * np.random.sample(),
    "x_atoms": atom_params["a0"][:, 0],
    "y_atoms": atom_params["a0"][:, 1],
    "r_atoms": atom_params["a0"][:, 2],
    "m_atoms": atom_params["a0"][:, 3],
    "stiffness_atoms": atom_stiffness,
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}

"""
A00_BODY = {
    "type": "a00",
    "x": 4,
    "y": 5,
    "v_x": 0.5 - np.random.sample(),
    "v_y": 0.5 - np.random.sample(),
    "v_rot": 0.5 - np.random.sample(),
    "x_atoms": atom_params["a00"][:, 0],
    "y_atoms": atom_params["a00"][:, 1],
    "r_atoms": atom_params["a00"][:, 2],
    "m_atoms": atom_params["a00"][:, 3],
    "stiffness_atoms": atom_stiffness,
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}

A01_BODY = {
    "type": "a01",
    "x": 2,
    "y": 5,
    "v_x": 0.5 - np.random.sample(),
    "v_y": 0.5 - np.random.sample(),
    "v_rot": 0.5 - np.random.sample(),
    "x_atoms": atom_params["a01"][:, 0],
    "y_atoms": atom_params["a01"][:, 1],
    "r_atoms": atom_params["a01"][:, 2],
    "m_atoms": atom_params["a01"][:, 3],
    "stiffness_atoms": atom_stiffness,
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}

A02_BODY = {
    "type": "a02",
    "x": 3,
    "y": 2,
    "v_x": 0.5 - np.random.sample(),
    "v_y": 0.5 - np.random.sample(),
    "v_rot": 0.5 - np.random.sample(),
    "x_atoms": atom_params["a02"][:, 0],
    "y_atoms": atom_params["a02"][:, 1],
    "r_atoms": atom_params["a02"][:, 2],
    "m_atoms": atom_params["a02"][:, 3],
    "stiffness_atoms": atom_stiffness,
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}
"""

right_wall = {
    "x_left": WORLD_WIDTH,
    "y_left": 1.0,
    "x_right": WORLD_WIDTH,
    "y_right": 0.0,
}
left_wall = {
    "x_left": 0.0,
    "y_left": 0.0,
    "x_right": 0.0,
    "y_right": 1.0,
}
floor = {
    "x_left": 1.0,
    "y_left": 0.0,
    "x_right": 0.0,
    "y_right": 0.0,
}
ceiling = {
    "x_left": 0.0,
    "y_left": WORLD_HEIGHT,
    "x_right": 1.0,
    "y_right": WORLD_HEIGHT,
}

WALLS = [
    right_wall,
    left_wall,
    floor,
    ceiling,
]

############################################
#
# Configuration parameters for the animation

FIG_SCALE = 1.5
FIG_WIDTH = WORLD_WIDTH * FIG_SCALE
FIG_HEIGHT = WORLD_HEIGHT * FIG_SCALE

BACKGROUND_COLOR = BLACK

############################################
#
# Configuration parameters for the dashboard

DASH_X = 1300  # pixels from the left
DASH_Y = 50  # pixels from the top
DASH_WIDTH = 600  # In pixels
DASH_HEIGHT = 300  # In pixels

DASH_BACKGROUND_COLOR = "#222222"
DASH_FOREGROUND_COLOR = "#FFFFFF"
DASH_SECOND_COLOR = "#888888"
DASH_BORDER = 0.2
DASH_LINE_PARAMS = {
    "color": DASH_FOREGROUND_COLOR,
    "linewidth": 1,
}

DASH_X_LABEL = "seconds"
DASH_Y_LABEL = "compute budget p90"
DASH_LABEL_PARAMS = {
    "color": DASH_SECOND_COLOR,
    "fontsize": 9,
}
DASH_X_TICK_LABELS = ["60", "45", "30", "15", "now"]
DASH_Y_TICK_LABELS = ["50%", "100%", "150%", "200%"]
DASH_X_TICK_POSITIONS = [-59, -45, -30, -15, 0]
DASH_Y_TICK_POSITIONS = [0.5, 1.0, 1.5, 2.0]

DASH_GRID_PARAMS = {
    "color": DASH_SECOND_COLOR,
    "linewidth": 1,
    "linestyle": "dotted",
}
DASH_X_TICK_PARAMS = {
    "axis": "x",
    "direction": "in",
    "color": DASH_SECOND_COLOR,
    "labelcolor": DASH_SECOND_COLOR,
    "labelsize": 7,
    "bottom": True,
    "top": False,
    "labelbottom": True,
    "labeltop": False,
}
DASH_Y_TICK_PARAMS = {
    "axis": "y",
    "direction": "in",
    "color": DASH_SECOND_COLOR,
    "labelcolor": DASH_SECOND_COLOR,
    "labelsize": 7,
    "left": False,
    "right": False,
    "labelleft": True,
    "labelright": False,
}
DASH_CONCERN_ZONE_PARAMS = {
    "edgecolor": "none",
    "facecolor": "#333333",
    "zorder": -2,
}
