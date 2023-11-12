import json
import time
import numpy as np
import matplotlib.pyplot as plt

import config
import tools.logging_setup as logging_setup
from tools.pacemaker import Pacemaker


def run(listen_wave_q):
    logger = logging_setup.get_logger(
        config.LOGGER_NAME_WAVE, config.LOGGING_LEVEL_WAVE
    )

    frame = Frame()
    pacemaker = Pacemaker(config.CLOCK_FREQ_WAVE_VIZ)

    while True:
        overtime = pacemaker.beat()
        if overtime > config.CLOCK_PERIOD_WAVE_VIZ:
            logger.warning(
                json.dumps({"ts": time.time(), "overtime": overtime})
            )
        blocks = []
        while not listen_wave_q.empty():
            blocks.append(listen_wave_q.get())
        if len(blocks) > 0:
            snippet = np.concatenate(tuple(blocks))
            frame.update(snippet)


class Frame:
    def __init__(self):
        self.n_samples = config.N_RAW_VIZ_SAMPLES
        self.recent_history = np.zeros(self.n_samples)

        self.fig = plt.figure(
            facecolor=config.RAW_VIZ_BACKGROUND_COLOR,
            num=config.FIGURE_NAME_WAVE,
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
                config.RAW_VIZ_X,
                config.RAW_VIZ_Y,
                config.RAW_VIZ_WIDTH,
                config.RAW_VIZ_HEIGHT,
            )
        except Exception:
            # If unsuccessful, don't worry about it.
            pass

        t_min = -config.RAW_VIZ_DURATION
        t_max = 0.0
        time_values = np.linspace(t_min, t_max, self.n_samples)

        self.ax = self.fig.add_axes(
            (
                config.RAW_VIZ_LEFT_BORDER,
                config.RAW_VIZ_BOTTOM_BORDER,
                1 - (config.RAW_VIZ_LEFT_BORDER + config.RAW_VIZ_RIGHT_BORDER),
                1 - (config.RAW_VIZ_BOTTOM_BORDER + config.RAW_VIZ_TOP_BORDER),
            )
        )
        self.ax.set_facecolor(config.RAW_VIZ_BACKGROUND_COLOR)
        self.ax.set_xlim(t_min, t_max)
        self.ax.set_ylim(
            -config.RAW_VIZ_MIN_AMPLITUDE, config.RAW_VIZ_MIN_AMPLITUDE
        )
        """
        # Do some customization
        x_formatter = FixedFormatter(config.RAW_VIZ_X_TICK_LABELS)
        y_formatter = FixedFormatter(config.RAW_VIZ_Y_TICK_LABELS)
        x_locator = FixedLocator(config.RAW_VIZ_X_TICK_POSITIONS)
        y_locator = FixedLocator(config.RAW_VIZ_Y_TICK_POSITIONS)
        self.ax.xaxis.set_major_formatter(x_formatter)
        self.ax.yaxis.set_major_formatter(y_formatter)
        self.ax.xaxis.set_major_locator(x_locator)
        self.ax.yaxis.set_major_locator(y_locator)
        """

        self.ax.tick_params(**config.RAW_VIZ_X_TICK_PARAMS)
        self.ax.tick_params(**config.RAW_VIZ_Y_TICK_PARAMS)

        self.ax.spines["top"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_color(config.RAW_VIZ_SECOND_COLOR)

        self.ax.grid(**config.RAW_VIZ_GRID_PARAMS)

        self.line = self.ax.plot(
            time_values, self.recent_history, **config.RAW_VIZ_LINE_PARAMS
        )[0]
        self.ax.set_xlabel(
            config.RAW_VIZ_X_LABEL, **config.RAW_VIZ_LABEL_PARAMS
        )
        self.ax.set_ylabel(
            config.RAW_VIZ_Y_LABEL, **config.RAW_VIZ_LABEL_PARAMS
        )

        plt.ion()
        plt.show()

    def update(self, snippet):
        # Reduce the snippet by a factor to make it more plottable.
        # If we keep ALL the data points, it takes too long to update.
        snip = snippet[:: config.REDUCTION_FACTOR].ravel()

        self.recent_history = np.roll(self.recent_history, -snip.size)
        self.recent_history[-snip.size :] = snip
        self.line.set_ydata(self.recent_history)
        self.fig.canvas.flush_events()
