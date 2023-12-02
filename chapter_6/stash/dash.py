import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import FixedLocator, FixedFormatter

# import logging_setup
from pacemaker import Pacemaker
import config


def run(sim_dash_duration_q):
    # logger = logging_setup.get_logger("viz", config.LOGGING_LEVEL_DASH)
    frame = Frame()
    # clock_period = 1 / float(config.CLOCK_FREQ_DASH)
    pacemaker = Pacemaker(config.CLOCK_FREQ_DASH)

    while True:
        pacemaker.beat()

        while not sim_dash_duration_q.empty():
            duration = sim_dash_duration_q.get()
            frame.update_history(duration)

        frame.update()


class Frame:
    def __init__(self):
        self.i_sample = 0
        self.n_samples = config.CLOCK_FREQ_SIM
        self.one_second_history = np.zeros(self.n_samples)
        self.one_minute_history = np.zeros(60)

        self.fig = plt.figure(facecolor=config.DASH_BACKGROUND_COLOR)

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
                config.DASH_X,
                config.DASH_Y,
                config.DASH_WIDTH,
                config.DASH_HEIGHT,
            )
        except Exception:
            # If unsuccessful, don't worry about it.
            pass

        t_min = -59.0
        t_max = 0.0
        time_values = np.linspace(t_min, t_max, int(t_max - t_min + 1))

        self.ax = self.fig.add_axes(
            (
                config.DASH_BORDER,
                config.DASH_BORDER,
                1 - 2 * config.DASH_BORDER,
                1 - 2 * config.DASH_BORDER,
            )
        )
        self.ax.set_facecolor(config.DASH_BACKGROUND_COLOR)
        self.ax.set_xlim(t_min, t_max)
        self.ax.set_ylim(0.0, 2.0)

        # Do some customization
        x_formatter = FixedFormatter(config.DASH_X_TICK_LABELS)
        y_formatter = FixedFormatter(config.DASH_Y_TICK_LABELS)
        x_locator = FixedLocator(config.DASH_X_TICK_POSITIONS)
        y_locator = FixedLocator(config.DASH_Y_TICK_POSITIONS)
        self.ax.xaxis.set_major_formatter(x_formatter)
        self.ax.yaxis.set_major_formatter(y_formatter)
        self.ax.xaxis.set_major_locator(x_locator)
        self.ax.yaxis.set_major_locator(y_locator)

        self.ax.tick_params(**config.DASH_X_TICK_PARAMS)
        self.ax.tick_params(**config.DASH_Y_TICK_PARAMS)

        self.ax.spines["top"].set_visible(False)
        self.ax.spines["bottom"].set_visible(True)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_color(config.DASH_SECOND_COLOR)

        self.ax.plot([t_min, t_max], [2.0, 2.0], **config.DASH_GRID_PARAMS)
        self.ax.plot([t_min, t_max], [1.5, 1.5], **config.DASH_GRID_PARAMS)
        self.ax.plot([t_min, t_max], [1.0, 1.0], **config.DASH_GRID_PARAMS)
        self.ax.plot([t_min, t_max], [0.5, 0.5], **config.DASH_GRID_PARAMS)

        # Create a shaded patch showing the zone of concern
        path = [
            [t_min, 1.0],
            [t_min, 10.0],
            [t_max, 10.0],
            [t_max, 1.0],
        ]
        self.ax.add_patch(
            patches.Polygon(path, **config.DASH_CONCERN_ZONE_PARAMS)
        )

        self.line = self.ax.plot(
            time_values, self.one_minute_history, **config.DASH_LINE_PARAMS
        )[0]
        self.ax.set_xlabel(config.DASH_X_LABEL, **config.DASH_LABEL_PARAMS)
        self.ax.set_ylabel(config.DASH_Y_LABEL, **config.DASH_LABEL_PARAMS)

        plt.ion()
        plt.show()

    def update_history(self, duration):
        duration_cycles = duration * config.CLOCK_FREQ_SIM
        self.one_second_history[self.i_sample] = duration_cycles
        self.i_sample += 1
        if self.i_sample == self.n_samples:
            self.i_sample = 0
            p90 = np.percentile(self.one_second_history, 90)
            self.one_minute_history[0] = p90
            self.one_minute_history = np.roll(self.one_minute_history, -1)

    def update(self):
        self.line.set_ydata(self.one_minute_history)
        self.ax.set_ylim(0, np.maximum(2.0, np.max(self.one_minute_history)))
        self.fig.canvas.flush_events()
