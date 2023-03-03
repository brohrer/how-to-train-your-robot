import logging

# Environment
N_PEG_ROWS = 19
N_PEG_COLS = 10
PEG_RADIUS = 0.05
PEG_EDGE_SPACING = 0.06
PEG_TOP_SPACING = 0.5
PEG_BOTTOM_SPACING = 0.3

PEG_ROW_SPACING = 0.35 / 2
PEG_COL_SPACING = PEG_ROW_SPACING * 2.5

FIG_WIDTH = (
    (N_PEG_COLS - 0.5) * PEG_COL_SPACING
    + (N_PEG_COLS + 1) * 2 * PEG_RADIUS
    + 2 * PEG_EDGE_SPACING
)
FIG_HEIGHT = (
    (N_PEG_ROWS - 1) * PEG_ROW_SPACING
    + N_PEG_ROWS * 2 * PEG_RADIUS
    + PEG_BOTTOM_SPACING
    + PEG_TOP_SPACING
)
FIG_SCALE = 2

GRAVITY = -9.8  # m / s^2

# Appearance
BOARD_COLOR = "#222222"
# PEG_COLOR = "#999999"
PEG_COLOR = "#333399"

# Mechanical properties
PEG_STIFFNESS = 1e4
DAMPING = 1.0

# Time control
CLOCK_FREQ_SIM = 1000  # Hertz
CLOCK_PERIOD_SIM = 1 / float(CLOCK_FREQ_SIM)
CLOCK_FREQ_VIZ = 24  # Hertz

# Logging settings
LOGGING_LEVEL_SIM = logging.INFO
LOGGING_LEVEL_VIZ = logging.INFO
