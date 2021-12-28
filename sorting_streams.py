import numpy as np
import random


class Streams(object):
    """
    Contains methods in format 
        >>> def method_name(data: np.ndarray):
    Can be provided to the animated_scatter.
    AnimateSubPlot class to use as sorting methods.\n\n
    End the methods with
        >>> yield from endless_loop(data)
    to avoid the IterationStopped exception.
    """

    @staticmethod
    def endless_loop(value: np.ndarray):
        while True:
            yield value

    @staticmethod
    def selectsort_stream(data: np.ndarray) -> np.ndarray:
        for i in range(len(data)):
            minpos = i
            for j in range(i + 1, len(data)):
                if data[j] < data[minpos]:
                    minpos = j
            data[minpos], data[i] = data[i], data[minpos]
            yield data
        yield from Streams.endless_loop(data)

    @staticmethod
    def shellsort_stream(data: np.ndarray):
        n = len(data)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = data[i]
                j = i
                while j >= gap and data[j - gap] > temp:
                    data[j] = data[j - gap]
                    yield data
                    j -= gap
                data[j] = temp
                # yield data
            gap //= 2

        yield from Streams.endless_loop(data)

    @staticmethod
    def quicksort_stream(data: np.ndarray):
        elem_num = len(data) - 1
        if not elem_num:
            yield from Streams.endless_loop(data)

        def quicksort(low, high):
            if low < high:

                def partition(low, high):
                    i = low - 1
                    pivot = data[high]

                    for j in range(low, high):
                        if data[j] <= pivot:
                            i = i + 1
                            data[i], data[j] = data[j], data[i]
                            yield data

                    data[i + 1], data[high] = data[high], data[i + 1]
                    yield data
                    return i + 1

                pi = yield from partition(low, high)

                yield from quicksort(low=low, high=pi - 1)
                yield from quicksort(low=pi + 1, high=high)

        yield from quicksort(
            0, elem_num,
        )

        yield from Streams.endless_loop(data)

    @staticmethod
    def mergesort_stream(data: np.ndarray):
        def merge_sort(start, end):
            if end - start > 1:
                middle = (start + end) // 2

                yield from merge_sort(start, middle)
                yield from merge_sort(middle, end)
                left = data[start:middle].copy()
                right = data[middle:end].copy()

                l_ind = 0
                r_ind = 0
                d_ind = start
                while l_ind < len(left) and r_ind < len(right):
                    if left[l_ind] < right[r_ind]:
                        data[d_ind] = left[l_ind]
                        l_ind += 1
                    else:
                        data[d_ind] = right[r_ind]
                        r_ind += 1

                    yield data
                    d_ind += 1

                while l_ind < len(left):
                    data[d_ind] = left[l_ind]
                    yield data
                    l_ind += 1
                    d_ind += 1

                while r_ind < len(right):
                    data[d_ind] = right[r_ind]
                    yield data
                    r_ind += 1
                    d_ind += 1

                yield data

        yield from merge_sort(0, len(data))

        yield from Streams.endless_loop(data)

    @staticmethod
    def quicksort_norec_stream(data: np.ndarray):
        def partition(l, h):
            i = l - 1
            x = data[h]
            for j in range(l, h):
                if data[j] <= x:
                    i = i + 1
                    data[i], data[j] = data[j], data[i]
                    yield data
            data[i + 1], data[h] = data[h], data[i + 1]
            yield data
            return i + 1

        def quicksort_stack(l, h):
            size = h - l + 1
            stack = [0] * (size)
            top = -1
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = h
            while top >= 0:
                h = stack[top]
                top = top - 1
                l = stack[top]
                top = top - 1
                p = yield from partition(l, h)
                if p - 1 > l:
                    top = top + 1
                    stack[top] = l
                    top = top + 1
                    stack[top] = p - 1
                if p + 1 < h:
                    top = top + 1
                    stack[top] = p + 1
                    top = top + 1
                    stack[top] = h

        yield from quicksort_stack(0, len(data) - 1)
        yield from Streams.endless_loop(data)

    @staticmethod
    def radix_stream(data: np.ndarray):
        r = 10
        min_elem, max_elem = min(data), max(data)
        maxLen = max(
            len(str(min_elem)) if min_elem >= 0 else len(str(min_elem)) - 1,
            len(str(max_elem)) if max_elem >= 0 else len(str(max_elem)) - 1,
        )

        for x in range(maxLen):
            bins = [[] for _ in range(r + 9)]
            for y in data:
                if y >= 0:
                    bins[int((y / 10 ** x) % r + 9)].append(y)
                else:
                    bins[int((y / 10 ** x) % r)].append(y)

            cur_start = 0
            for section in bins:
                for i, elem in enumerate(section):
                    data[i + cur_start] = elem
                    yield data
                cur_start += len(section)
            # yield data

        yield from Streams.endless_loop(data)

    @staticmethod
    def bogosort_stream(data: np.ndarray):
        n = len(data)

        def is_sorted():
            for i in range(0, n - 1):
                if data[i] > data[i + 1]:
                    return False
            return True

        def shuffle():
            for i in range(0, n):
                r = random.randint(0, n - 1)
                data[i], data[r] = data[r], data[i]

        while not is_sorted():
            shuffle()
            yield data

        yield from Streams.endless_loop(data)

    @staticmethod
    def randsort_stream(data: np.ndarray):
        n = len(data)

        def is_sorted():
            for i in range(0, n - 1):
                if data[i] > data[i + 1]:
                    return False
            return True

        while not is_sorted():
            for i in range(0, n):
                r = random.randint(0, n - 1)
                if (i < r and data[i] >= data[r]) or (i > r and data[i] <= data[r]):
                    data[i], data[r] = data[r], data[i]
                yield data

        yield from Streams.endless_loop(data)
