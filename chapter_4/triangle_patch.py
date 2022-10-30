import matplotlib.patches as patches
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.gca()
path = [
    [.1, .3],
    [.2, .9],
    [.8, .4],
]
ax.add_patch(patches.Polygon(path))
fig.savefig("patch.png")
