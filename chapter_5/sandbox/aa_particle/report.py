import json
import os
import numpy as np
import matplotlib.pyplot as plt

filenames = os.listdir()
for filename in filenames:
    if filename.__contains__("ani.log"):
        log_id = filename.split("_")[0]
        tss = []
        with open(filename, "rt") as f:
            lines = f.readlines()
            for line in lines:
                try:
                    row_dict = dict(json.loads(line))
                    tss.append(row_dict["ts"])
                except Exception:
                    pass

        tss = np.array(tss)

        fig = plt.figure()
        ax = fig.gca()
        ax.plot(
            tss[1:],
            np.diff(tss),
            linestyle="none",
            marker=".",
            color="black",
            alpha=0.7,
        )
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Time gap (seconds)")
        plt.savefig(f"{log_id}_report.png")
