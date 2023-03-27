import random
import time
import threading
import multiprocessing

def merge_sort(array):
    if len(array) > 1:
        mid = len(array) // 2
        left_array = array[:mid]
        right_array = array[mid:]

        merge_sort(left_array)
        merge_sort(right_array)

        i = j = k = 0

        while i < len(left_array) and j < len(right_array):
            if left_array[i] < right_array[j]:
                array[k] = left_array[i]
                i += 1
            else:
                array[k] = right_array[j]
                j += 1
            k += 1

        while i < len(left_array):
            array[k] = left_array[i]
            i += 1
            k += 1

        while j < len(right_array):
            array[k] = right_array[j]
            j += 1
            k += 1

def merge_sort_parallel_threads(array, num_threads=2):
    class MergeSortThread(threading.Thread):
        def __init__(self, array, start_index, end_index):
            threading.Thread.__init__(self)
            self.array = array
            self.start_index = start_index
            self.end_index = end_index
            self.start_time = None
            self.end_time = None

        def run(self):
            self.start_time = time.perf_counter()
            merge_sort(self.array[self.start_index:self.end_index])
            self.end_time = time.perf_counter()

    start_time = time.perf_counter()
    threads = []

    chunk_size = len(array) // num_threads
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < num_threads - 1 else len(array)
        thread = MergeSortThread(array, start_index, end_index)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    sorted_array = []
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < num_threads - 1 else len(array)
        sorted_array.extend(array[start_index:end_index])
    merge_sort(sorted_array)

    total_time = time.perf_counter() - start_time
    thread_times = [thread.end_time - thread.start_time for thread in threads]
    print(f'Tempo total threads: {total_time:.6f} segundos')
    # print(f'Tempos das threads: {thread_times}')

    return sorted_array

def merge_sort_parallel_process(array, num_processes=2):
    start_time = time.perf_counter()
    chunk_size = len(array) // num_processes
    processes = []
    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (i+1) * chunk_size if i < num_processes - 1 else len(array)
        process = multiprocessing.Process(target=merge_sort, args=(array[start_index:end_index],))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    sorted_array = []
    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (i+1) * chunk_size if i < num_processes - 1 else len(array)
        sorted_array.extend(array[start_index:end_index])    
    total_time = time.perf_counter() - start_time
    print(f'Tempo total processos: {total_time:.6f} segundos')
    return sorted_array


if __name__ == '__main__':
    multiprocessing.freeze_support()
    array = [random.randint(0, 100) for _ in range(100)]
    sorted_array = merge_sort_parallel_threads(array, num_threads=2)
    sorted_array1 = merge_sort_parallel_process(array, num_processes=2)

    print(sorted_array)


