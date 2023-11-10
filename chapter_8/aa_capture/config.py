import logging

CLOCK_FREQ_WAVE_VIZ = 30.0  # Hz
CLOCK_PERIOD_WAVE_VIZ = 1.0 / CLOCK_FREQ_WAVE_VIZ

# Choose the audio block duration to be a multiple
# of the raw audio time series visualization.
AUDIO_BLOCK_DURATION = 1 / (10.0 * CLOCK_FREQ_WAVE_VIZ)
AUDIO_DEVICE = 0

# One of {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL_LISTEN = logging.DEBUG
LOGGING_LEVEL_WAVE = logging.DEBUG

############################################
#
# Configure the raw audio time series plot

RAW_VIZ_MIN_AMPLITUDE = 0.1
REDUCTION_FACTOR = 30
RAW_VIZ_DURATION = 3.0
RAW_SAMPLING_DURATION = 44100
N_RAW_VIZ_SAMPLES = int(
    RAW_VIZ_DURATION * RAW_SAMPLING_DURATION / REDUCTION_FACTOR
)

RAW_VIZ_X = 300  # pixels from the left
RAW_VIZ_Y = 50  # pixels from the top
RAW_VIZ_WIDTH = 900  # In pixels
RAW_VIZ_HEIGHT = 400  # In pixels

RAW_VIZ_BACKGROUND_COLOR = "#222222"
RAW_VIZ_FOREGROUND_COLOR = "#FFFFFF"
RAW_VIZ_SECOND_COLOR = "#888888"
RAW_VIZ_BORDER = 0.1
RAW_VIZ_LINE_PARAMS = {
    "color": RAW_VIZ_FOREGROUND_COLOR,
    "linewidth": .5,
}

RAW_VIZ_X_LABEL = "seconds"
RAW_VIZ_Y_LABEL = "compute budget p90"
RAW_VIZ_LABEL_PARAMS = {
    "color": RAW_VIZ_SECOND_COLOR,
    "fontsize": 9,
}
RAW_VIZ_X_TICK_LABELS = ["60", "45", "30", "15", "now"]
RAW_VIZ_Y_TICK_LABELS = ["50%", "100%", "150%", "200%"]
RAW_VIZ_X_TICK_POSITIONS = [-59, -45, -30, -15, 0]
RAW_VIZ_Y_TICK_POSITIONS = [0.5, 1.0, 1.5, 2.0]

RAW_VIZ_GRID_PARAMS = {
    "color": RAW_VIZ_SECOND_COLOR,
    "linewidth": 1,
    "linestyle": "dotted",
}
RAW_VIZ_X_TICK_PARAMS = {
    "axis": "x",
    "direction": "in",
    "color": RAW_VIZ_SECOND_COLOR,
    "labelcolor": RAW_VIZ_SECOND_COLOR,
    "labelsize": 7,
    "bottom": True,
    "top": False,
    "labelbottom": True,
    "labeltop": False,
}
RAW_VIZ_Y_TICK_PARAMS = {
    "axis": "y",
    "direction": "in",
    "color": RAW_VIZ_SECOND_COLOR,
    "labelcolor": RAW_VIZ_SECOND_COLOR,
    "labelsize": 7,
    "left": False,
    "right": False,
    "labelleft": True,
    "labelright": False,
}
