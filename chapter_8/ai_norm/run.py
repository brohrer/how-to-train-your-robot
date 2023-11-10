import multiprocessing as mp
import listen
import multifft
import multispec
import norm

mp.set_start_method("fork")


listen_multifft_q = mp.Queue()
multifft_norm_q = mp.Queue()
norm_spec_q = mp.Queue()

p_listen = mp.Process(
    target=listen.run,
    args=(listen_multifft_q,),
)
p_multifft = mp.Process(
    target=multifft.run,
    args=(listen_multifft_q, multifft_norm_q),
)
p_norm = mp.Process(
    target=norm.run,
    args=(multifft_norm_q, norm_spec_q),
)
p_multispec = mp.Process(
    target=multispec.run,
    args=(norm_spec_q,),
)

p_listen.start()
p_multifft.start()
p_norm.start()
p_multispec.start()
