import multiprocessing as mp
import interface_logging as interface
import adder_logging as adder

instructions = """
  Welcome to the People Counter

  Use keys 1-9 to count people.
  Use space bar to undo your last keypress.
"""
print(instructions)

q = mp.Queue()
p_interface = mp.Process(target=interface.run, args=(q,))
p_adder = mp.Process(target=adder.run, args=(q,))

p_interface.start()
p_adder.start()
