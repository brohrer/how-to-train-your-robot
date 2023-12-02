import numpy as np
import logging

FIG_WIDTH = 6
FIG_HEIGHT = 6
FIG_SCALE = 1.5

GRAVITY = -1.0  # m / s^2

# Appearance
BACKGROUND_COLOR = "#222222"
BODY_COLOR = {
    "L": "#2EA3F2",
    "terrain": "#404243",
}

SPEED_LIMIT = 10.0

# Time control
CLOCK_FREQ_SIM = 1000  # Hertz
CLOCK_PERIOD_SIM = 1 / float(CLOCK_FREQ_SIM)
CLOCK_FREQ_VIZ = 30  # Hertz

# Logging settings
LOGGING_LEVEL_SIM = logging.INFO
LOGGING_LEVEL_VIZ = logging.INFO

# Initialize crystals
# Terrain crystals
TERRAIN = {}
TERRAIN["id"] = "terrain"
TERRAIN["x"] = FIG_WIDTH / 2
TERRAIN["y"] = FIG_HEIGHT / 2
TERRAIN["x_atoms"] = (
    np.array([0.10, 0.20, 0.35, 0.50, 0.65, 0.80, 0.90]) * FIG_WIDTH
)
TERRAIN["y_atoms"] = (
    np.array([0.73, 0.60, 0.45, 0.30, 0.15, 0.40, 0.66]) * FIG_HEIGHT
)
n_atoms = TERRAIN["x_atoms"].size
TERRAIN["r_atoms"] = np.ones(n_atoms) * FIG_WIDTH * 0.05
TERRAIN["stiffness_atoms"] = np.ones(n_atoms) * 1e3
TERRAIN["free"] = False

# L-shaped
# https://docs.google.com/presentation/d/1Bnaqb-zPWwU9d1gUB_AK_lo9aQqEHI837P5FWwwJhno/edit

x_spacing = 0.1
y_spacing = 0.1
# diagonal spacing between atoms in the lattice
d_spacing = np.sqrt(x_spacing**2 + y_spacing**2)
atom_mass = 0.01

L_BODY = {}
L_BODY["id"] = "L"
L_BODY["x"] = 3.0
L_BODY["y"] = 4.0
L_BODY["v_x"] = -0.1
L_BODY["v_y"] = 0.05
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
L_BODY["stiffness_atoms"] = np.ones(n_atoms) * 1e2
