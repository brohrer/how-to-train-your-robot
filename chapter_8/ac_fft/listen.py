import json
import sys
import time
import config
import tools.logging_setup as logging_setup

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


def run(listen_wave_q, listen_fft_q):
    logger = logging_setup.get_logger(
        config.LOGGER_NAME_LISTEN, config.LOGGING_LEVEL_LISTEN
    )

    try:
        # Query the input device to figure out what its sampling rate is
        # in samples per second.
        device_info = sd.query_devices(config.AUDIO_DEVICE_ID, "input")
        samplerate = device_info["default_samplerate"]
        blocksize = int(samplerate * config.AUDIO_BLOCK_DURATION)
        # print(device_info)
        # print(sd.query_devices())
    except Exception as e:
        print("Couldn't get the sample rate for the recording device")
        print(e)
        raise

    try:
        # Set up the stream and kick off the collection
        stream = sd.InputStream(
            device=config.AUDIO_DEVICE_ID,
            channels=1,
            samplerate=samplerate,
            blocksize=blocksize,
            latency="low",
        )

        with stream:
            while True:
                indata, overflowed = stream.read(blocksize)
                if overflowed:
                    logger.warning(
                        json.dumps(
                            {"ts": time.time(), "overflowed": overflowed}
                        )
                    )

                listen_wave_q.put(indata[:, [0]])
                listen_fft_q.put(indata[:, [0]])

    except Exception as e:
        print(e)
        raise
