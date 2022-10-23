import numpy as np
import matplotlib.pyplot as plt
from pacemaker import Pacemaker

pacemaker = Pacemaker(24)
fig = plt.figure(figsize=(4, 4))
ax = fig.add_axes((0, 0, 1, 1))
(ball,) = ax.plot(0, 0, marker="o", markersize=16)
ax.axis("equal")
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)

plt.ion()
plt.show()

for i in range(10000):

    # https://en.wikipedia.org/wiki/Lissajous_curve
    x = np.cos(i / 10)
    y = np.cos(i / 9.01)
    ball.set_xdata(x)
    ball.set_ydata(y)
    pacemaker.beat()
    fig.canvas.flush_events()
