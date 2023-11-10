import queue
import sys
from matplotlib.ticker import FixedLocator, FixedFormatter
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft

try:
    import sounddevice as sd
except ModuleNotFoundError:
    print()
    print("sounddevice module isn't installed yet. Try")
    print("    python3 -m pip install sounddevice -U")
    print()
    print("If that doesn't work visit")
    print("https://e2eml.school/play_and_record_sounds.html")
    print()
    sys.exit()


def animate_frequency_response(
    # How many times should the visualization be updated per second?
    interval=30,
    # How many milliseconds of data should be included in creating each frame?
    # A longer window means that the curve will be less jumpy, but also that
    # It will respond to sounds more slowly.
    window=200,
    # Setting device to None tells sounddevice to automatically figure out which is
    # the default device
    device=None,
):
    global plotdata
    try:
        # Query the input device to figure out what its sampling rate is
        # in samples per second.
        device_info = sd.query_devices(device, "input")
        samplerate = device_info["default_samplerate"]
    except Exception as e:
        print("Couldn't get the sample rate for the recording device")
        print(e)
        raise

    q = queue.Queue()
    # Get some fake data to initialize the plot with
    n_samples = int(window * samplerate / 1000)
    plotdata = np.zeros((n_samples, 1))

    def audio_callback(indata, frames, time, status):
        """
        This is called repeatedly from a separate thread.
        It helps read in data for each audio block.
        """
        # Fancy indexing creates a (necessary!) copy:
        q.put(indata[:, [0]])

    def update_plot(frame):
        """
        This is called by matplotlib for each plot update.

        Typically, audio callbacks happen more frequently than plot updates,
        therefore the queue tends to contain multiple blocks of audio data.
        """
        global plotdata
        while True:
            try:
                data = q.get_nowait()
            except queue.Empty:
                break
            shift = len(data)
            plotdata = np.roll(plotdata, -shift, axis=0)
            plotdata[-shift:, :] = data

        freqs, mags = time_to_freq(plotdata[:, 0])
        lines[0].set_ydata(mags)
        return lines

    def time_to_freq(
        timeseries,
        bins_per_octave=12,
        low_cutoff=60,
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
        log_freqs = np.log10(eps + np.arange(n_samples) * 1000 / window)
        # Define the edges of the frequency bins.
        # These are evenly spaced on a log scale.
        # Bins at the higher end will include a lot of different frequencies.
        # Bins at the lower end will have few, some one, and some none.
        bin_edges = np.arange(
            np.log10(low_cutoff),
            np.log10(samplerate / 2),
            np.log10(2) / bins_per_octave,
        )

        # Convert the time series to frequencies using the fast Fourier transform.
        energies = np.abs(fft(timeseries))
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

    bin_centers, bin_mags = time_to_freq(plotdata)

    # Create and format the frequency domain plot
    fig = plt.figure()
    ax = fig.add_axes((0.13, 0.15, 0.81, 0.79))
    lines = ax.plot(bin_centers, bin_mags)
    ax.axis((np.min(bin_centers), np.max(bin_centers), -30, 30))
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("magnitude (dB)")
    x_major_formatter = FixedFormatter(
        ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]
    )
    x_major_locator = FixedLocator(
        [1.3, 1.7, 2, 2.3, 2.7, 3, 3.3, 3.7, 4, 4.3]
    )
    x_minor_locator = FixedLocator(
        [
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
    )
    ax.xaxis.set_major_locator(x_major_locator)
    ax.xaxis.set_minor_locator(x_minor_locator)
    ax.xaxis.set_major_formatter(x_major_formatter)
    ax.grid(which="both")

    try:
        # Set up the stream and kick off the collection
        stream = sd.InputStream(
            device=device,
            channels=1,
            samplerate=samplerate,
            callback=audio_callback,
        )
        # This sets up the animation
        ani = FuncAnimation(fig, update_plot, interval=interval, blit=True)
        with stream:
            plt.show()

    except Exception as e:
        print(e)
        raise


if __name__ == "__main__":
    animate_frequency_response(interval=2000, window=10000)
