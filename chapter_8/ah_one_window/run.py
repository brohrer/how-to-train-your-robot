import multiprocessing as mp
import listen
# import wave
# import fft
# import freq
# import spec
import multifft
# import multifreq
import multispec

mp.set_start_method("fork")


# listen_wave_q = mp.Queue()
# listen_fft_q = mp.Queue()
# fft_freq_q = mp.Queue()
# fft_spec_q = mp.Queue()
listen_multifft_q = mp.Queue()
# multifft_freq_q = mp.Queue()
multifft_spec_q = mp.Queue()

p_listen = mp.Process(
    target=listen.run,
    # args=(listen_wave_q, listen_fft_q, listen_multifft_q),
    args=(listen_multifft_q,),
)
# p_wave = mp.Process(
#     target=wave.run,
#     args=(listen_wave_q,),
# )
# p_fft = mp.Process(
#     target=fft.run,
#     args=(listen_fft_q, fft_freq_q, fft_spec_q),
# )
# p_freq = mp.Process(
#     target=freq.run,
#     args=(fft_freq_q,),
# )
# p_spec = mp.Process(
#     target=spec.run,
#     args=(fft_spec_q,),
# )
p_multifft = mp.Process(
    target=multifft.run,
    # args=(listen_multifft_q, multifft_freq_q, multifft_spec_q),
    args=(listen_multifft_q, multifft_spec_q),
)
# p_multifreq = mp.Process(
#     target=multifreq.run,
#     args=(multifft_freq_q,),
# )
p_multispec = mp.Process(
    target=multispec.run,
    args=(multifft_spec_q,),
)

p_listen.start()
p_multifft.start()
p_multispec.start()
# p_multifreq.start()
# p_fft.start()
# p_spec.start()
# p_freq.start()
# p_wave.start()
