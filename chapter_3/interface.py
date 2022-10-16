import time
from getkey import getkey


def run(q):
    last_key = "0"
    while True:
        key = getkey()
        key_time = time.time()

        if key in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            q.put((key_time, key))
            print(f"ts: {key_time}, ppl_reported: {key}")
            last_key = key

        if key == " ":
            remove_ppl = str(-int(last_key))
            q.put((key_time, remove_ppl))
            print(f"ts: {key_time}, ppl_undo: {last_key}")
            last_key = "0"
