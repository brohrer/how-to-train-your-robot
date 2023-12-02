import numpy as np
import logging


# Time control
CLOCK_FREQ_SIM = 300  # Hertz
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

WORLD_WIDTH = 6.5
WORLD_HEIGHT = 6.5

GRAVITY = -3.0  # m / s^2

force_duration = 0.25  # seconds
FORCE_SHAPE = np.ones(int(force_duration * CLOCK_FREQ_SIM))

# Initialize crystals
atom_stiffness = 1e3
sliding_friction = 0.2
inelasticity = 0.1

fish = {
    "id": "fish",
    "color": "#e02421",  # red
    "x": 3,
    "y": 5,
    "v_x": 0.5 - np.random.sample(),
    "v_y": 0.5 - np.random.sample(),
    "v_rot": 0.5 - np.random.sample(),
    "x_atoms": np.array([0.0]),
    "y_atoms": np.array([0.0]),
    "r_atoms": np.array([0.6]),
    "m_atoms": np.array([8.0]),
    "stiffness_atoms": np.array([atom_stiffness]),
    "sliding_friction": sliding_friction,
    "inelasticity": inelasticity,
}

BODIES = {
    fish["id"]: fish,
}

# Color palette inspired by this image:
# https://www.looper.com/img/gallery/why-the-big-bang-theory-fans-love-sheldons-ball-pit-scene/fans-always-get-a-big-kick-out-of-sheldons-ball-pit-scene-1673479140.jpg
ball_colors = [
    "#1aac5a",  # green
    "#214e9e",  # blue
    "#fdc440",  # yellow
]
ball_radius = 0.17
n_rows_balls = 10
n_cols_balls = 10
for i in range(n_rows_balls):
    for j in range(n_cols_balls):
        x = ball_radius * 1.2 + j * ball_radius * 2.5
        y = ball_radius * 1.2 + i * ball_radius * 2.5
        body_id = f"ball_{x}_{y}"
        ball_body = {
            "id": body_id,
            "color": np.random.choice(ball_colors),
            "x": x,
            "y": y,
            "v_x": 0.5 - np.random.sample(),
            "v_y": 0.5 - np.random.sample(),
            "v_rot": 0.5 - np.random.sample(),
            "x_atoms": np.array([0.0]),
            "y_atoms": np.array([0.0]),
            "r_atoms": np.array([ball_radius]),
            "m_atoms": np.array([0.2]),
            "stiffness_atoms": np.array([atom_stiffness]),
            "sliding_friction": sliding_friction,
            "inelasticity": inelasticity,
        }
        BODIES[body_id] = ball_body

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

BACKGROUND_COLOR = "#372b38"

############################################
#
# Configuration parameters for the dashboard

DASH_X = 1100  # pixels from the left
DASH_Y = 100  # pixels from the top
DASH_WIDTH = 800  # In pixels
DASH_HEIGHT = 400  # In pixels

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
