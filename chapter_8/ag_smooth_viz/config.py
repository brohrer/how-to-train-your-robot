import logging

# One of {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL_LISTEN = logging.DEBUG
LOGGING_LEVEL_WAVE = logging.DEBUG
LOGGING_LEVEL_FFT = logging.DEBUG
LOGGING_LEVEL_FREQ = logging.DEBUG
LOGGING_LEVEL_SPEC = logging.DEBUG
LOGGING_LEVEL_MULTIFFT = logging.DEBUG
LOGGING_LEVEL_MULTIFREQ = logging.DEBUG
LOGGING_LEVEL_MULTISPEC = logging.DEBUG

LOGGER_NAME_LISTEN = "listen"
LOGGER_NAME_WAVE = "wave"
LOGGER_NAME_FFT = "fft"
LOGGER_NAME_FREQ = "freq"
LOGGER_NAME_SPEC = "spec"
LOGGER_NAME_MULTIFFT = "fft"
LOGGER_NAME_MULTIFREQ = "freq"
LOGGER_NAME_MULTISPEC = "spec"

FIGURE_NAME_WAVE = "Raw audio signal"
FIGURE_NAME_FREQ = "Frequency response"
FIGURE_NAME_SPEC = "Spectrogram"
FIGURE_NAME_MULTIFREQ = "Frequency response, multi-FFT"
FIGURE_NAME_MULTISPEC = "Spectrogram, multi-FFT"

CLOCK_FREQ_WAVE_VIZ = 30.0  # Hz
CLOCK_PERIOD_WAVE_VIZ = 1.0 / CLOCK_FREQ_WAVE_VIZ
CLOCK_FREQ_FFT = 30.0  # Hz
CLOCK_PERIOD_FFT = 1.0 / CLOCK_FREQ_FFT
CLOCK_FREQ_FFT_VIZ = 30.0  # Hz
CLOCK_PERIOD_FFT_VIZ = 1.0 / CLOCK_FREQ_FFT_VIZ
CLOCK_FREQ_SPEC = 20.0  # Hz
CLOCK_PERIOD_SPEC = 1.0 / CLOCK_FREQ_SPEC

# Choose the audio block duration to be a multiple
# of the raw audio time series visualization.
AUDIO_BLOCK_DURATION = 1 / (10.0 * CLOCK_FREQ_WAVE_VIZ)

# Blue Yeti, if plugged in
# device = 6
# Laptop builtin
# device = 0
AUDIO_DEVICE_ID = 6

SAMPLING_RATE = 44100

# A longer window means that the curve will be less jumpy, but also that
# It will respond to sounds more slowly.
FFT_WINDOW_DURATION_XSHORT = 0.02  # seconds
FFT_WINDOW_DURATION_SHORT = 0.05  # seconds
FFT_WINDOW_DURATION_MEDIUM = 0.1  # seconds
FFT_WINDOW_DURATION_LONG = 0.5  # seconds

FFT_WINDOW_DURATION = FFT_WINDOW_DURATION_MEDIUM
MULTIFFT_WINDOW_DURATION = FFT_WINDOW_DURATION_LONG

# How much to offset each FFT sample window from the last, in seconds.
FFT_STRIDE_DURATION = 1.0 / 30.0

BINS_PER_OCTAVE = 36
LOW_CUTOFF = 30

############################################
#
# Configure the raw audio time series plot

RAW_VIZ_MIN_AMPLITUDE = 0.5
REDUCTION_FACTOR = 30
RAW_VIZ_DURATION = 9.0
N_RAW_VIZ_SAMPLES = int(RAW_VIZ_DURATION * SAMPLING_RATE / REDUCTION_FACTOR)

RAW_VIZ_X = 10  # pixels from the left
RAW_VIZ_Y = 0  # pixels from the top
RAW_VIZ_WIDTH = 1100  # In pixels
RAW_VIZ_HEIGHT = 350  # In pixels

RAW_VIZ_BACKGROUND_COLOR = "#222222"
RAW_VIZ_FOREGROUND_COLOR = "#FFFFFF"
RAW_VIZ_SECOND_COLOR = "#888888"
RAW_VIZ_LEFT_BORDER = 0.08
RAW_VIZ_RIGHT_BORDER = 0.04
RAW_VIZ_BOTTOM_BORDER = 0.13
RAW_VIZ_TOP_BORDER = 0.08
RAW_VIZ_LINE_PARAMS = {
    "color": RAW_VIZ_FOREGROUND_COLOR,
    "linewidth": 0.5,
}

RAW_VIZ_X_LABEL = "Seconds"
RAW_VIZ_Y_LABEL = "Audio amplitude"
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

############################################
#
# Configure the audio frequency response plot

FFT_VIZ_X = RAW_VIZ_X + RAW_VIZ_WIDTH  # pixels from the left
FFT_VIZ_Y = RAW_VIZ_Y + RAW_VIZ_HEIGHT + 35  # pixels from the top
FFT_VIZ_WIDTH = int(RAW_VIZ_WIDTH * 0.7)  # In pixels
FFT_VIZ_HEIGHT = RAW_VIZ_HEIGHT  # In pixels

FFT_VIZ_X_LABEL = "Frequency (Hz)"
FFT_VIZ_Y_LABEL = "Magnitude (dB)"
FFT_VIZ_Y_MIN = -20
FFT_VIZ_Y_MAX = 20
FFT_VIZ_TICK_LABELS = [
    "20",
    "50",
    "100",
    "200",
    "500",
    "1k",
    "2k",
    "5k",
    "10k",
    "20k",
]
FFT_VIZ_MAJOR_TICK_POSITIONS = [1.3, 1.7, 2, 2.3, 2.7, 3, 3.3, 3.7, 4, 4.3]
FFT_VIZ_MINOR_TICK_POSITIONS = [
    1.48,
    1.6,
    1.78,
    1.85,
    1.9,
    1.95,
    2.48,
    2.6,
    2.78,
    2.85,
    2.9,
    2.95,
    3.48,
    3.6,
    3.78,
    3.85,
    3.9,
    3.95,
]

############################################
#
# Configure the audio spectrogram

SPEC_VIZ_DURATION = RAW_VIZ_DURATION
# N_SPEC_VIZ_SAMPLES = int(SPEC_VIZ_DURATION / (FFT_STRIDE_FRACTION * FFT_

SPEC_VIZ_X = RAW_VIZ_X  # pixels from the left
SPEC_VIZ_Y = FFT_VIZ_Y  # pixels from the top
SPEC_VIZ_WIDTH = RAW_VIZ_WIDTH  # In pixels
SPEC_VIZ_HEIGHT = RAW_VIZ_HEIGHT  # In pixels

SPEC_VIZ_VMAX = 30
SPEC_VIZ_VMIN = -10

SPEC_VIZ_X_LABEL = "Seconds"
SPEC_VIZ_Y_LABEL = "Frequency (Hz)"

SPEC_VIZ_X_TICK_LABELS = [
    f"{-1 * 1.00 * RAW_VIZ_DURATION:.2}",
    f"{-1 * 0.67 * RAW_VIZ_DURATION:.2}",
    f"{-1 * 0.33 * RAW_VIZ_DURATION:.2}",
    f"{0.00 * RAW_VIZ_DURATION:.2}",
]
'''
SPEC_VIZ_MAJOR_X_TICK_POSITIONS = [
    0,
    (N_SPEC_VIZ_SAMPLES - 1) * 0.33,
    (N_SPEC_VIZ_SAMPLES - 1) * 0.67,
    (N_SPEC_VIZ_SAMPLES - 1),
]
'''

SPEC_VIZ_Y_TICK_LABELS = [
    "50",
    "100",
    "200",
    "500",
    "1k",
    "2k",
    "5k",
    "10k",
    "20k",
]
SPEC_VIZ_MAJOR_Y_TICK_POSITIONS = [2, 7, 16, 32, 44, 56, 72, 84, 96]

###########################################################
#
# Configure the audio frequency response plot for multi-fft

MULTIFFT_VIZ_Y = FFT_VIZ_Y + FFT_VIZ_HEIGHT  # pixels from the top

###############################################
#
# Configure the audio spectrogram for multi-fft

MULTISPEC_VIZ_Y = FFT_VIZ_Y + FFT_VIZ_HEIGHT  # pixels from the top
MULTISPEC_VIZ_N_Y_TICKS = 10

# MULTISPEC_VIZ_VMAX = 10
# MULTISPEC_VIZ_VMIN = -25
