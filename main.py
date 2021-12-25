import random
from animated_scatter import AnimateSubPlot
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from sorting_streams import Streams


def data_gen(num_elems: int):
    MAX_NUM = 1000000

    # uniform distribution
    # data_arr = np.random.randint(low=-MAX_NUM, high=MAX_NUM, size=num_elems)

    # binomial (discrete normal) distribution
    data_arr = np.random.binomial(p=0.8, n=MAX_NUM, size=num_elems) - MAX_NUM

    return data_arr


def main(num_elems: int = 200):
    # uncomment this to edit the starting data size
    # num_elems = 0
    # while not 1 <= num_elems <= 20000:
    #     print("Input an integer from 1 to 20000.")
    #     try:
    #         num_elems = int(input("--> "))
    #     except:
    #         pass

    # uncomment what you dont need
    streams_arr = [
        [Streams.selectsort_stream, "Selection Sort"],
        [Streams.shellsort_stream, "Shell Sort"],
        # [Streams.quicksort_stream, "Quick Sort"],
        [Streams.quicksort_norec_stream, "Quick Sort (Stack)"],
        [Streams.mergesort_stream, "Merge Sort"],
        [Streams.radix_stream, "Radix Sort"],
    ]

    # Change plot_shape[1] to reduce the data range (hence the number of columns)
    plot_shape = (len(streams_arr), 3)

    # Data generation Process
    data_dict = {
        c: data_gen(random.randint(c * num_elems + 35, (c + 1) * num_elems))
        for c in range(plot_shape[1])
    }
    # Leave this line for more randomness
    # data_dict = None

    fig, axs_arr = plt.subplots(nrows=plot_shape[0], ncols=plot_shape[1])

    ani_list = np.empty(shape=plot_shape, dtype=FuncAnimation)
    for p_row in range(plot_shape[0]):
        stream_func, sort_name = streams_arr[p_row % len(streams_arr)]
        for p_col in range(plot_shape[1]):
            if data_dict is not None:
                cur_data = data_dict[p_col]
            else:
                cur_data = data_gen(
                    random.randint(p_col * num_elems + 25, (p_col + 1) * num_elems)
                )

            cur_plane = axs_arr[p_row, p_col] if plot_shape[1] > 1 else axs_arr[p_row]
            cur_plane.set_title(f"{len(cur_data)} data points")
            if not p_col:
                cur_plane.set_ylabel(sort_name)

            ani_list[p_row, p_col] = AnimateSubPlot(
                cur_data,
                fig,
                cur_plane,
                stream=stream_func,
                # cut_to_frame=random.randint(1, 10),
                color=np.random.rand(3),  # random colot for every plane
            ).ani

    fig.set_size_inches(plot_shape[1] * 6, plot_shape[0] * 2.5)
    fig.tight_layout(pad=2.0)
    # fig.suptitle("Epжaн Cocaть Би6y", y=0.995)
    fig.suptitle("Animated Sorted Algorithms", y=0.995)
    plt.show()


if __name__ == "__main__":
    main()
