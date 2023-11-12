import numpy as np


class RingBuffer:
    def __init__(self, size):
        self.n = size
        self.x = np.zeros(self.n, dtype=float)
        self.i = 0

    def pop(self):
        val = self.x[self.i]
        self.x[self.i] = 0.0
        self.i += 1
        if self.i >= self.n:
            self.i = 0
        return val

    def add(self, arr):
        m = arr.size
        if m > self.n:
            raise IndexError(
                f"Trying to add an array of size {arr.size}"
                + f" to a ring buffer of size {self.n}."
            )
        n_left = self.n - self.i
        if m > n_left:
            # If wrapping is necessary
            self.x[self.i :] += arr[: n_left]
            n_wrap = m - n_left
            self.x[: n_wrap] = arr[n_left :]

        else:
            # If no wrapping is necessary
            self.x[self.i : self.i + m] += arr
