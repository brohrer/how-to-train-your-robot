import json
import time
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter
import matplotlib.pyplot as plt

import config
import tools.logging_setup as logging_setup
from tools.pacemaker import Pacemaker


def run(fft_spec_q):
    logger = logging_setup.get_logger(
        config.LOGGER_NAME_SPEC, config.LOGGING_LEVEL_SPEC
    )

    frame = Frame()
    pacemaker = Pacemaker(config.CLOCK_FREQ_SPEC)

    while True:
        overtime = pacemaker.beat()
        running_behind = False
        if overtime > config.CLOCK_PERIOD_SPEC:
            logger.warning(
                json.dumps({"ts": time.time(), "overtime": overtime})
            )
            running_behind = True
        frequencies = None
        while not fft_spec_q.empty():
            frequencies, magnitudes = fft_spec_q.get()
            frame.update(frequencies, magnitudes)

        if not running_behind:
            frame.update_viz()


class Frame:
    def __init__(self):
        pass

    def _initialize_frame(self, frequencies, magnitudes):
        self.fig = plt.figure(
            facecolor=config.RAW_VIZ_BACKGROUND_COLOR,
            num=config.FIGURE_NAME_MULTISPEC,
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
                config.SPEC_VIZ_X,
                config.MULTISPEC_VIZ_Y,
                config.SPEC_VIZ_WIDTH,
                config.SPEC_VIZ_HEIGHT,
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

        n_spec_viz_samples = int(
            config.SPEC_VIZ_DURATION / config.FFT_STRIDE_DURATION)
        self.img_data = np.zeros((frequencies.size, n_spec_viz_samples))
        self.img = self.ax.imshow(
            self.img_data,
            aspect="auto",
            # vmin=config.MULTISPEC_VIZ_VMIN,
            # vmax=config.MULTISPEC_VIZ_VMAX,
            vmin=config.SPEC_VIZ_VMIN,
            vmax=config.SPEC_VIZ_VMAX,
        )

        spec_viz_major_x_tick_positions = [
            0,
            (n_spec_viz_samples - 1) * 0.33,
            (n_spec_viz_samples - 1) * 0.67,
            (n_spec_viz_samples - 1),
        ]
        x_major_formatter = FixedFormatter(config.SPEC_VIZ_X_TICK_LABELS)
        x_major_locator = FixedLocator(spec_viz_major_x_tick_positions)
        # x_major_locator = FixedLocator(config.SPEC_VIZ_MAJOR_X_TICK_POSITIONS)
        self.ax.xaxis.set_major_locator(x_major_locator)
        self.ax.xaxis.set_major_formatter(x_major_formatter)

        i_ticks = np.round(
            np.linspace(
                0, frequencies.size - 1, config.MULTISPEC_VIZ_N_Y_TICKS
            )
        ).astype(int)
        y_major_locator = FixedLocator(i_ticks)
        tick_labels = []
        for i in i_ticks:
            f = 10 ** frequencies[frequencies.size - 1 - i]
            if f > 1000:
                label = str(float(int(f / 100)) / 10.0) + "k"
            else:
                label = int(f)
            tick_labels.append(label)
        y_major_formatter = FixedFormatter(tick_labels)

        # y_major_formatter = FixedFormatter(config.SPEC_VIZ_Y_TICK_LABELS)
        # y_major_locator = FixedLocator(
        #     frequencies.size - 1 -
        #     np.array(config.SPEC_VIZ_MAJOR_Y_TICK_POSITIONS))
        self.ax.yaxis.set_major_locator(y_major_locator)
        self.ax.yaxis.set_major_formatter(y_major_formatter)

        self.ax.tick_params(**config.RAW_VIZ_X_TICK_PARAMS)
        self.ax.tick_params(**config.RAW_VIZ_Y_TICK_PARAMS)

        self.ax.spines["top"].set_visible(True)
        self.ax.spines["bottom"].set_visible(True)
        self.ax.spines["right"].set_visible(True)
        self.ax.spines["left"].set_visible(True)
        self.ax.spines["top"].set_color(config.RAW_VIZ_SECOND_COLOR)
        self.ax.spines["bottom"].set_color(config.RAW_VIZ_SECOND_COLOR)
        self.ax.spines["left"].set_color(config.RAW_VIZ_SECOND_COLOR)
        self.ax.spines["right"].set_color(config.RAW_VIZ_SECOND_COLOR)

        self.ax.set_xlabel(
            config.SPEC_VIZ_X_LABEL, **config.RAW_VIZ_LABEL_PARAMS
        )
        self.ax.set_ylabel(
            config.SPEC_VIZ_Y_LABEL, **config.RAW_VIZ_LABEL_PARAMS
        )

        plt.ion()
        plt.show()

    def update(self, frequencies, magnitudes):
        try:
            self.img_data = np.roll(self.img_data, -1, axis=1)
        except AttributeError:
            self._initialize_frame(frequencies, magnitudes)
            self.img_data = np.roll(self.img_data, -1, axis=1)

        self.img_data[:, -1] = magnitudes[::-1]

    def update_viz(self):
        try:
            self.img.set(data=self.img_data)
            self.fig.canvas.flush_events()
        except AttributeError:
            pass
