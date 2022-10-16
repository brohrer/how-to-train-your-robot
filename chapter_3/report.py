import json
import os
import numpy as np
import matplotlib.pyplot as plt

filenames = os.listdir()
for filename in filenames:
    if filename.__contains__("adder.log"):
        log_id = filename.split("_")[0]
        times = []
        count = []
        with open(filename, "rt") as f:
            lines = f.readlines()
            for line in lines:
                try:
                    row_dict = dict(json.loads(line))
                    times.append(row_dict["ts"])
                    count.append(row_dict["ppl_count"])
                except Exception:
                    pass

        times = np.array(times)
        count = np.array(count)

        try:
            minutes = (times - np.min(times)) / 60
        except ValueError:
            minutes = 0
            count = 0

        fig = plt.figure()
        ax = fig.gca()
        ax.plot(minutes, count)
        ax.set_xlabel("Counting time (minutes)")
        ax.set_ylabel("Total people")
        plt.savefig(f"{log_id}_report.png")
