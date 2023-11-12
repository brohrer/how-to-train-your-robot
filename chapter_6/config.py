import numpy as np
import logging


# Time control
CLOCK_FREQ_SIM = 10000  # Hertz
CLOCK_PERIOD_SIM = 1 / float(CLOCK_FREQ_SIM)  # seconds
CLOCK_FREQ_VIZ = 30  # Hertz
CLOCK_FREQ_DASH = 4  # Hertz
CLOCK_FREQ_RUN = 4  # Hertz
# CLOCK_FREQ_WATCH = .25  # Hertz
ALIVE_CHECK_FREQ = 1  # Hertz
WARMUP_PERIOD = 6  # seconds

# Logging settings
LOGGING_LEVEL_SIM = logging.ERROR
LOGGING_LEVEL_VIZ = logging.ERROR
LOGGING_LEVEL_DASH = logging.INFO

#
############################################
# Configuration parameters for the simulation

WORLD_WIDTH = 6
WORLD_HEIGHT = 6

GRAVITY = 0  # -3.0  # m / s^2

# Initialize crystals
# Terrain crystals
TERRAIN = {}
TERRAIN["id"] = "terrain"
TERRAIN["x"] = WORLD_WIDTH / 2
TERRAIN["y"] = WORLD_HEIGHT / 2
TERRAIN["x_atoms"] = (
    np.array([0.10, 0.20, 0.35, 0.50, 0.65, 0.80, 0.90]) * WORLD_WIDTH
)
TERRAIN["y_atoms"] = (
    np.array([0.73, 0.60, 0.45, 0.30, 0.15, 0.40, 0.66]) * WORLD_HEIGHT
)
n_atoms = TERRAIN["x_atoms"].size
TERRAIN["r_atoms"] = np.ones(n_atoms) * WORLD_WIDTH * 0.05
TERRAIN["stiffness_atoms"] = np.ones(n_atoms) * 1e3
TERRAIN["sliding_friction"] = 0.4
TERRAIN["inelasticity"] = 0.05
TERRAIN["free"] = False

# L-shaped body
# https://docs.google.com/presentation/d/1Bnaqb-zPWwU9d1gUB_AK_lo9aQqEHI837P5FWwwJhno/edit

x_spacing = 0.1
y_spacing = 0.1
atom_mass = 0.01
atom_stiffness = 1e3
sliding_friction = 0.25
inelasticity = 0.3

L_BODY = {}
L_BODY["id"] = "L"
L_BODY["x"] = 3.0
L_BODY["y"] = 4.0
L_BODY["v_x"] = -1.0
L_BODY["v_y"] = 0.5
L_BODY["v_rot"] = -0.5

# Initial positions of each atom
L_BODY["x_atoms"] = (
    np.array([0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 4, 5, 4, 5]) * x_spacing
)
L_BODY["y_atoms"] = (
    np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3]) * y_spacing
)
n_atoms = L_BODY["x_atoms"].size
L_BODY["r_atoms"] = np.ones(n_atoms) * x_spacing / 2
L_BODY["m_atoms"] = np.ones(n_atoms) * atom_mass
L_BODY["stiffness_atoms"] = np.ones(n_atoms) * atom_stiffness
L_BODY["sliding_friction"] = sliding_friction
L_BODY["inleasticity"] = inelasticity

# S-shaped body
# https://docs.google.com/presentation/d/1Bnaqb-zPWwU9d1gUB_AK_lo9aQqEHI837P5FWwwJhno/edit#slide=id.g20a84048ece_0_0
n_atoms = 16
S_BODY = {
    "id": "S",
    "x": 2,
    "y": 5,
    "v_x": -2.6,
    "v_y": 0.3,
    "v_rot": 1.2,
    "x_atoms": (
        np.array([0, 1, 2, 3, 0, 1, 2, 3, 2, 3, 4, 5, 2, 3, 4, 5]) * x_spacing
    ),
    "y_atoms": (
        np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]) * y_spacing
    ),
    "r_atoms": np.ones(n_atoms) * x_spacing / 2,
    "m_atoms": np.ones(n_atoms) * atom_mass,
    "stiffness_atoms": np.ones(n_atoms) * atom_stiffness,
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}

# T-shaped body
# https://docs.google.com/presentation/d/1Bnaqb-zPWwU9d1gUB_AK_lo9aQqEHI837P5FWwwJhno/edit#slide=id.g256fb254ae7_0_0
n_atoms = 16
T_BODY = {
    "id": "T",
    "x": 4,
    "y": 5,
    "v_x": 3 * np.random.sample(),
    "v_y": -2 * np.random.sample(),
    "v_rot": 4 * np.random.sample(),
    "x_atoms": (
        np.array([0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 2, 3, 2, 3]) * x_spacing
    ),
    "y_atoms": (
        np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3]) * y_spacing
    ),
    "r_atoms": np.ones(n_atoms) * x_spacing / 2,
    "m_atoms": np.ones(n_atoms) * atom_mass,
    "stiffness_atoms": np.ones(n_atoms) * atom_stiffness,
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}

# I-shaped body
# https://docs.google.com/presentation/d/1Bnaqb-zPWwU9d1gUB_AK_lo9aQqEHI837P5FWwwJhno/edit#slide=id.g256fb254ae7_0_44
I_BODY = {
    "id": "I",
    "x": 3.5,
    "y": 5.5,
    "v_x": -5 * np.random.sample(),
    "v_y": 2 * np.random.sample(),
    "v_rot": 3 * np.random.sample(),
    "x_atoms": (
        np.array([0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]) * x_spacing
    ),
    "y_atoms": (
        np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]) * y_spacing
    ),
    "r_atoms": np.ones(n_atoms) * x_spacing / 2,
    "m_atoms": np.ones(n_atoms) * atom_mass,
    "stiffness_atoms": np.ones(n_atoms) * atom_stiffness,
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}

# Square body
# https://docs.google.com/presentation/d/1Bnaqb-zPWwU9d1gUB_AK_lo9aQqEHI837P5FWwwJhno/edit#slide=id.g256fb254ae7_0_80
SQUARE_BODY = {
    "id": "square",
    "x": 1.5,
    "y": 5.5,
    "v_x": -4 * np.random.sample(),
    "v_y": -3 * np.random.sample(),
    "v_rot": -7 * np.random.sample(),
    "x_atoms": (
        np.array([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]) * x_spacing
    ),
    "y_atoms": (
        np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]) * y_spacing
    ),
    "r_atoms": np.ones(n_atoms) * x_spacing / 2,
    "m_atoms": np.ones(n_atoms) * atom_mass,
    "stiffness_atoms": np.ones(n_atoms) * atom_stiffness,
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}

BODIES = [
    TERRAIN,
    L_BODY,
    S_BODY,
    T_BODY,
    I_BODY,
    SQUARE_BODY,
]

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

#
############################################
# Configuration parameters for the animation

FIG_SCALE = 1.5
FIG_WIDTH = WORLD_WIDTH * FIG_SCALE
FIG_HEIGHT = WORLD_HEIGHT * FIG_SCALE

# Appearance
BACKGROUND_COLOR = "#222222"
BODY_COLOR = {
    "L": "#2EA3F2",
    "S": "#F28A5C",
    "T": "#03C03C",
    "I": "#FF1493",
    "square": "#E3FF00",
    "terrain": "#404243",
}

#
############################################
# Configuration parameters for the dashboard

DASH_X = 1050  # pixels from the left
DASH_Y = 100  # pixels from the top
DASH_WIDTH = 640  # In pixels
DASH_HEIGHT = 345  # In pixels

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
    "fontsize": 8,
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
    "labelsize": 6,
    "bottom": True,
    "top": False,
    # "left": True,
    # "right": False,
    "labelbottom": True,
    "labeltop": False,
    # "labelleft": True,
    # "labelright": False,
}
DASH_Y_TICK_PARAMS = {
    "axis": "y",
    "direction": "in",
    "color": DASH_SECOND_COLOR,
    "labelcolor": DASH_SECOND_COLOR,
    "labelsize": 6,
    # "bottom": True,
    # "top": False,
    "left": False,
    "right": False,
    # "labelbottom": True,
    # "labeltop": False,
    "labelleft": True,
    "labelright": False,
}
DASH_CONCERN_ZONE_PARAMS = {
    "edgecolor": "none",
    "facecolor": "#333333",
    "zorder": -2,
}
