import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from sorting_streams import Streams


class AnimateSubPlot(object):
    def __init__(
        self,
        initial_data: np.ndarray,
        figure: plt.figure,
        plane: plt.Axes,
        stream: classmethod = Streams.selectsort_stream,
        color: np.ndarray = "blue",
        cut_to_frame: int = 1,
    ):
        self.cut_to_frame = cut_to_frame if cut_to_frame < 1 else 1
        self.data: np.ndarray = initial_data.copy()
        self.datalen = len(initial_data)
        self.x_ax = [i for i in range(self.datalen)]

        self.stream: classmethod = stream(data=self.data)

        self.setup_plot(plane, color)

        self.ani = animation.FuncAnimation(figure, self.refresh, interval=0, blit=True)

    def setup_plot(self, ax: plt.Axes, color: np.ndarray):
        y = next(self.stream)
        self.scat = ax.scatter(self.x_ax, y, s=15, c=[color], edgecolor="k")
        return (self.scat,)

    def refresh(self, i):
        if i % self.cut_to_frame:
            return (self.scat,)
        else:
            data = np.c_[self.x_ax, next(self.stream)]
            self.scat.set_offsets(data)
            return (self.scat,)

