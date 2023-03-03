import logging

# Initial state
GROUND_X = 4
GROUND_Y = 1
BOT_X = 4
BOT_Y = 3.5

# Mechanical properties
BOT_MASS = 2
UNSTRETECHED_LENGTH = BOT_Y - GROUND_Y
STIFFNESS = 30
DAMPING = 2

# Environment
SCALE = .1
INCIDENCE = 1 / 50

# Time control
CLOCK_FREQ_SIM = 1000  # Hertz
CLOCK_PERIOD_SIM = 1 / float(CLOCK_FREQ_SIM)
CLOCK_FREQ_VIZ = 39  # Hertz

# Logging settings
LOGGING_LEVEL_SIM = logging.INFO
LOGGING_LEVEL_VIZ = logging.INFO
