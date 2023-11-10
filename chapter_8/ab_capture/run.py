import multiprocessing as mp
import listen
import wave

mp.set_start_method("fork")


listen_wave_q = mp.Queue()

p_listen = mp.Process(
    target=listen.run,
    args=(listen_wave_q,),
)
p_wave = mp.Process(
    target=wave.run,
    args=(listen_wave_q,),
)

p_listen.start()
p_wave.start()
