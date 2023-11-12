import json
import time
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter
import matplotlib.pyplot as plt

import config
import tools.logging_setup as logging_setup
from tools.pacemaker import Pacemaker


def run(fft_freq_q):
    logger = logging_setup.get_logger(
        config.LOGGER_NAME_FREQ, config.LOGGING_LEVEL_FREQ
    )

    frame = Frame()
    pacemaker = Pacemaker(config.CLOCK_FREQ_FFT_VIZ)

    while True:
        overtime = pacemaker.beat()
        if overtime > config.CLOCK_PERIOD_FFT_VIZ:
            logger.warning(
                json.dumps({"ts": time.time(), "overtime": overtime})
            )
        frequencies = None
        while not fft_freq_q.empty():
            frequencies, magnitudes = fft_freq_q.get()
        if frequencies is not None:
            frame.update(frequencies, magnitudes)


class Frame:
    def __init__(self):
        pass

    def _initialize_frame(self, frequencies, magnitudes):
        self.fig = plt.figure(
            facecolor=config.RAW_VIZ_BACKGROUND_COLOR,
            num="Frequency response",
        )

        # Set the window location for the dashboard.
        try:
            # My machine uses backend QtAgg.
            # This approach won't work for other backends.
            # To find out which backend you are using
            # uncomment this snippet.
            # import matplotlib
            # print(matplotlib.get_backend())
            mngr = plt.get_current_fig_manager()
            # to put it into the upper left corner for example:
            mngr.window.setGeometry(
                config.FFT_VIZ_X,
                config.FFT_VIZ_Y,
                config.FFT_VIZ_WIDTH,
                config.FFT_VIZ_HEIGHT,
            )
        except Exception:
            # If unsuccessful, don't worry about it.
            pass

        self.ax = self.fig.add_axes(
            (
                config.RAW_VIZ_LEFT_BORDER,
                config.RAW_VIZ_BOTTOM_BORDER,
                1 - (config.RAW_VIZ_LEFT_BORDER + config.RAW_VIZ_RIGHT_BORDER),
                1 - (config.RAW_VIZ_BOTTOM_BORDER + config.RAW_VIZ_TOP_BORDER),
            )
        )
        self.ax.set_facecolor(config.RAW_VIZ_BACKGROUND_COLOR)

        self.line = self.ax.plot(
            frequencies, magnitudes, **config.RAW_VIZ_LINE_PARAMS
        )[0]
        self.ax.axis(
            (
                np.min(frequencies),
                np.max(frequencies),
                config.FFT_VIZ_Y_MIN,
                config.FFT_VIZ_Y_MAX,
            )
        )

        x_major_formatter = FixedFormatter(config.FFT_VIZ_TICK_LABELS)
        x_major_locator = FixedLocator(config.FFT_VIZ_MAJOR_TICK_POSITIONS)
        x_minor_locator = FixedLocator(config.FFT_VIZ_MINOR_TICK_POSITIONS)
        self.ax.xaxis.set_major_locator(x_major_locator)
        self.ax.xaxis.set_minor_locator(x_minor_locator)
        self.ax.xaxis.set_major_formatter(x_major_formatter)

        self.ax.tick_params(**config.RAW_VIZ_X_TICK_PARAMS)
        self.ax.tick_params(**config.RAW_VIZ_Y_TICK_PARAMS)

        self.ax.spines["top"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_color(config.RAW_VIZ_SECOND_COLOR)

        self.ax.grid(**config.RAW_VIZ_GRID_PARAMS)

        self.ax.set_xlabel(
            config.FFT_VIZ_X_LABEL, **config.RAW_VIZ_LABEL_PARAMS
        )
        self.ax.set_ylabel(
            config.FFT_VIZ_Y_LABEL, **config.RAW_VIZ_LABEL_PARAMS
        )

        plt.ion()
        plt.show()

    def update(self, frequencies, magnitudes):
        try:
            self.line.set_ydata(magnitudes)
        except AttributeError:
            self._initialize_frame(frequencies, magnitudes)
            self.line.set_ydata(magnitudes)

        self.fig.canvas.flush_events()
