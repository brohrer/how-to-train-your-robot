import numpy as np
import logging

ATOM_RADIUS = 0.065  # 0.022

FIG_WIDTH = 6
FIG_HEIGHT = 6
FIG_SCALE = 1.5

GRAVITY = -0.3  # m / s^2

# Appearance
BACKGROUND_COLOR = "#222222"
CRYSTAL_COLOR = {
    "L": "#2EA3F2",
    "terrain": "#404243",
}

# Mechanical properties
ATOM_STIFFNESS = 1e4
DAMPING = 1

SPEED_LIMIT = 4.0

# Time control
CLOCK_FREQ_SIM = 1000  # Hertz
CLOCK_PERIOD_SIM = 1 / float(CLOCK_FREQ_SIM)
CLOCK_FREQ_VIZ = 30  # Hertz

# Logging settings
LOGGING_LEVEL_SIM = logging.INFO
LOGGING_LEVEL_VIZ = logging.INFO

# Initialize crystals
# Terrain crystals
n_atoms = 7
k = 1e3
TERRAIN = {}
TERRAIN["id"] = "terrain"
TERRAIN["x"] = np.array([0.10, 0.20, 0.35, 0.50, 0.65, 0.80, 0.90]) * FIG_WIDTH
TERRAIN["y"] = (
    np.array([0.73, 0.60, 0.45, 0.30, 0.15, 0.40, 0.66]) * FIG_HEIGHT
)
TERRAIN["r"] = np.ones(n_atoms) * FIG_WIDTH * 0.05
TERRAIN["k_external"] = np.ones(n_atoms) * k
TERRAIN["free"] = np.zeros(n_atoms)

# L-shaped
# https://docs.google.com/presentation/d/1Bnaqb-zPWwU9d1gUB_AK_lo9aQqEHI837P5FWwwJhno/edit
x_init = 3.0
y_init = 4.0
x_spacing = 0.1
y_spacing = 0.1
# diagonal spacing between atoms in the lattice
d_spacing = np.sqrt(x_spacing**2 + y_spacing**2)
atom_mass = 0.01
n_atoms = 16
k = 1e2
L_CRYSTAL = {}
L_CRYSTAL["id"] = "L"
# Initial positions of each atom
L_CRYSTAL["x"] = (
    np.array([0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 4, 5, 4, 5]) * x_spacing
    + x_init
)
L_CRYSTAL["y"] = (
    np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3]) * y_spacing
    + y_init
)
L_CRYSTAL["r"] = np.ones(n_atoms) * x_spacing / 2
L_CRYSTAL["m"] = np.ones(n_atoms) * atom_mass
L_CRYSTAL["k_external"] = np.ones(n_atoms) * k
L_CRYSTAL["k_internal"] = np.array(
    [
        [0, 1, k, x_spacing],
        [1, 2, k, x_spacing],
        [2, 3, k, x_spacing],
        [3, 4, k, x_spacing],
        [4, 5, k, x_spacing],
        [6, 7, k, x_spacing],
        [7, 8, k, x_spacing],
        [8, 9, k, x_spacing],
        [9, 10, k, x_spacing],
        [10, 11, k, x_spacing],
        [12, 13, k, x_spacing],
        [14, 15, k, x_spacing],
        [0, 6, k, y_spacing],
        [1, 7, k, y_spacing],
        [2, 8, k, y_spacing],
        [3, 9, k, y_spacing],
        [4, 10, k, y_spacing],
        [5, 11, k, y_spacing],
        [10, 12, k, y_spacing],
        [11, 13, k, y_spacing],
        [12, 14, k, y_spacing],
        [13, 15, k, y_spacing],
        [0, 7, k, d_spacing],
        [1, 6, k, d_spacing],
        [1, 8, k, d_spacing],
        [2, 7, k, d_spacing],
        [2, 9, k, d_spacing],
        [3, 8, k, d_spacing],
        [3, 10, k, d_spacing],
        [4, 9, k, d_spacing],
        [4, 11, k, d_spacing],
        [5, 10, k, d_spacing],
        [11, 12, k, d_spacing],
        [12, 15, k, d_spacing],
        [13, 14, k, d_spacing],
    ]
)
