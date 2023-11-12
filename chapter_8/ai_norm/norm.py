import config
import numpy as np


def run(fft_norm_q, norm_spec_q):
    normalizer = AdaptiveNormalizer()

    while True:
        while not fft_norm_q.empty():
            freqs, mags = fft_norm_q.get()
            normed_mags = normalizer.normalize(mags)
            norm_spec_q.put((freqs, normed_mags))


class AdaptiveNormalizer:
    def __init__(self):
        self.n_passes = config.NORM_INITIAL_PASSES
        self.contraction_rate = config.NORM_CONTRACTION_RATE
        self.expansion_rate = config.NORM_EXPANSION_RATE

    def initialize_limits(self, mags):
        eps = 1e-12
        self.lower_limits = -np.ones(mags.size) * eps
        self.upper_limits = np.ones(mags.size) * eps

    def normalize(self, mags):
        try:
            self.update_limits(mags)
        except AttributeError:
            self.initialize_limits(mags)
            self.update_limits(mags)

        normed = (mags - self.lower_limits) / (
            self.upper_limits - self.lower_limits
        )
        # Limit normed values to the interval [0, 1]
        normed = np.maximum(0.0, np.minimum(1.0, normed))

        return normed

    def update_limits(self, mags):
        # Find all the elements that are lower than the lower bound
        # or higher than the upper bound.
        i_low = np.where(mags < self.lower_limits)[0]
        i_high = np.where(mags > self.upper_limits)[0]

        # First move all the limits a little bit toward the value
        # of the magnitude for this pass.
        # For most of the elements, this will be a contraction.
        # Adding the 1 / n_passes term to the contraction rate
        # makes it quite a bit larger for the first few passes.
        # The helps the limits to migrate quickly to match the signal.
        self.lower_limits += (mags - self.lower_limits) * (
            self.contraction_rate + 1.0 / self.n_passes
        )
        self.upper_limits += (mags - self.upper_limits) * (
            self.contraction_rate + 1.0 / self.n_passes
        )

        # Then expand the limits more generously in cases where
        # they have been exceeded.
        self.lower_limits[i_low] += (
            mags[i_low] - self.lower_limits[i_low]
        ) * (self.expansion_rate + 1.0 / self.n_passes)
        self.upper_limits[i_high] += (
            mags[i_high] - self.upper_limits[i_high]
        ) * (self.expansion_rate + 1.0 / self.n_passes)

        self.n_passes += 1
