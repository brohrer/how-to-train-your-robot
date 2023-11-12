import multiprocessing as mp
import listen
import wave
import fft
import freq
import spec

mp.set_start_method("fork")


listen_wave_q = mp.Queue()
listen_fft_q = mp.Queue()
fft_freq_q = mp.Queue()
fft_spec_q = mp.Queue()

p_listen = mp.Process(
    target=listen.run,
    args=(listen_wave_q, listen_fft_q),
)
p_wave = mp.Process(
    target=wave.run,
    args=(listen_wave_q,),
)
p_fft = mp.Process(
    target=fft.run,
    args=(listen_fft_q, fft_freq_q, fft_spec_q),
)
p_freq = mp.Process(
    target=freq.run,
    args=(fft_freq_q,),
)
p_spec = mp.Process(
    target=spec.run,
    args=(fft_spec_q,),
)

p_listen.start()
p_fft.start()
# Kick off the visualizations in an order that encourages them to
# hide each others window header bar.
p_spec.start()
p_freq.start()
p_wave.start()
