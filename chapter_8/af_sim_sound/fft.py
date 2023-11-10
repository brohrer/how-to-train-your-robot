import json
import time
import numpy as np
from numpy.fft import fft

import config
import tools.logging_setup as logging_setup
from tools.pacemaker import Pacemaker


def run(listen_fft_q, fft_freq_q, fft_spec_q):
    logger = logging_setup.get_logger(
        config.LOGGER_NAME_FFT, config.LOGGING_LEVEL_FFT
    )

    pacemaker = Pacemaker(config.CLOCK_FREQ_FFT)

    # How many milliseconds of data should be included in creating each frame?
    # A longer window means that the curve will be less jumpy, but also that
    # It will respond to sounds more slowly.
    window_length = config.FFT_WINDOW_LENGTH

    n_samples = int(window_length * config.SAMPLING_RATE / 1000)
    sample_window = np.zeros(n_samples)

    while True:
        overtime = pacemaker.beat()
        if overtime > config.CLOCK_PERIOD_FFT:
            logger.warning(
                json.dumps({"ts": time.time(), "overtime": overtime})
            )
        blocks = []
        while not listen_fft_q.empty():
            blocks.append(listen_fft_q.get())

        if len(blocks) == 0:
            time.sleep(config.EMPTY_Q_WAIT)
            continue
        snippet = np.concatenate(tuple(blocks)).ravel()

        if len(snippet) > sample_window.size:
            snippet = snippet[-sample_window.size :]

        shift = len(snippet)
        sample_window = np.roll(sample_window, -shift)
        sample_window[-shift:] = snippet

        freqs, mags = time_to_freq(sample_window, window_length)
        fft_freq_q.put((freqs, mags))
        fft_spec_q.put((freqs, mags))


def time_to_freq(
    timeseries,
    window_length,
    bins_per_octave=config.BINS_PER_OCTAVE,
    low_cutoff=config.LOW_CUTOFF,
):
    """
    Convert a set of time sequence sound measurements to frequencies.

    bins_per_octave (float) is the number of frequency bins per octave
    (doubling of freqency). For reference, there are 12 notes per octave
    in the chromatic scale of Western music. More notes per octave will
    result in a more finely sliced frequency breakdown. Fewer notes
    per octave will make the frequency response look less jumpy.

    low_cutoff (float) is the lowest frequency to consider in the plot.
    Including frquencies that are too low leads to some very jumpy
    lines. You can counter this by increasing the window length.
    """
    big_val = 1e6
    eps = 1e-3
    n_samples = timeseries.size

    # Transform the frequencies to a log scale
    log_freqs = np.log10(eps + np.arange(n_samples) * 1000 / window_length)
    # Define the edges of the frequency bins.
    # These are evenly spaced on a log scale.
    # Bins at the higher end will include a lot of different frequencies.
    # Bins at the lower end will have few, some one, and some none.
    bin_edges = np.arange(
        np.log10(low_cutoff),
        np.log10(config.SAMPLING_RATE / 2),
        np.log10(2) / bins_per_octave,
    )

    # Apply a Blackman window to keep the representation of pure tones sharp.
    windowed_timeseries = np.blackman(timeseries.size) * timeseries
    # Convert the time series to frequencies using the fast Fourier transform.
    energies = np.abs(fft(windowed_timeseries))
    # Convert energies at each frequency to decibels
    decibels = 10 * np.log10(energies + 1e-6)
    bin_centers = np.zeros(bin_edges.size - 1)
    # Initialize decibels to an easy-to-identify default
    bin_decibels = np.ones(bin_edges.size - 1) * big_val
    # Step through each frequency bin and aggregate responses
    for i_bin in range(int(bin_edges.size - 1)):
        bin_centers[i_bin] = (bin_edges[i_bin] + bin_edges[i_bin + 1]) / 2
        # Find all the frequencies that fall within the bin
        i_bin_freqs = np.where(
            np.logical_and(
                log_freqs >= bin_edges[i_bin],
                log_freqs < bin_edges[i_bin + 1],
            )
        )
        # Find the average decibels of all the bin's frequencies
        if i_bin_freqs[0].size > 0:
            bin_decibels[i_bin] = np.mean(decibels[i_bin_freqs])

    # Find the bins that didn't collect any frequencies and remove them.
    i_keep = np.where(bin_decibels != big_val)
    bin_centers = bin_centers[i_keep]
    bin_decibels = bin_decibels[i_keep]

    return bin_centers, bin_decibels
