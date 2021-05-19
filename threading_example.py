import math
import numpy as np
from timebudget import timebudget
import threading
import multiprocessing

''' Compare addition speed of a vector length 1e8 in for loop vs threading vs multiprocessing
'''


class Adder_process(multiprocessing.Process):
    def __init__(self, values, queue):
        self.values = values
        self.result = None
        self.queue = queue
        super(Adder_process, self).__init__()

    def run(self):
        self.result = 0
        for i in range(len(self.values)):
            self.result += self.values[i]
        self.queue.put(self.result)


@timebudget
def sum_with_process(values: list, n_processors=1):
    result = 0
    workloads = np.array_split(values, n_processors)
    result_queue = multiprocessing.Queue()
    workers = []
    for i in range(n_processors):
        workers.append(Adder_process(workloads[i], queue=result_queue))
        workers[-1].start()

    for i in range(len(workers)):
        workers[i].join()
        result += result_queue.get()
    return result


class Adder_thread(threading.Thread):
    def __init__(self, values):
        self.values = values
        self.result = None
        super(Adder_thread, self).__init__()

    def run(self):
        self.result = 0
        for i in range(len(self.values)):
            self.result += self.values[i]


@timebudget
def sum_with_thread(values: list, n_threads=1):
    result = 0
    workloads = np.array_split(values, n_threads)
    workers = []
    for i in range(n_threads):
        workers.append(Adder_thread(workloads[i]))
        workers[-1].start()

    for i in range(len(workers)):
        workers[i].join()
        result += workers[i].result
    return result


@timebudget
def sum_normally(values: list):
    result = 0
    for i in range(len(values)):
        result += values[i]
    return result


@timebudget
def numpy_sum(values):
    return np.sum(values)


def main():
    list_to_add = np.random.random(int(1e8))
    workers = 8

    sum_with_thread_result = sum_with_thread(list_to_add, workers)
    print(sum_with_thread_result)

    sum_with_process_result = sum_with_process(list_to_add, workers)
    print(sum_with_process_result)

    sum_normally_result = sum_normally(list_to_add)
    print(sum_normally_result)

    sum_numpy = numpy_sum(list_to_add)


if __name__ == "__main__":
    main()
