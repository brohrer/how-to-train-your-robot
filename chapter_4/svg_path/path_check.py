import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(5, 5))
ax = fig.gca()
path = np.load("path4603.npy")

ax.add_patch(patches.Polygon(
    path,
    edgecolor="black",
    facecolor="none",
    linewidth=2,
))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
plt.show()
fig.savefig("patch.png")
