from time import time
from multiprocessing import Process, cpu_count, Manager, current_process
import logging


def factorize_helper(n, output_dict):
    divs = [1, n]
    name = current_process().name
    for i in range(2, n//2+1):
        if n % i == 0:
            if i not in divs:
                divs.append(i)
                divs.append(n // i)
    divs.sort()
    logging.debug(f"{n}: {divs}")
    output_dict[name] = divs


def factorize(*number):
    time_start = time()
    with Manager() as manager:
        processes = []
        factors = manager.dict()
        for n in number:
            pr = Process(target=factorize_helper, args=(n, factors))
            processes.append(pr)
            pr.start()

        for pr in processes:
            pr.join()

        print(factors)
        sorted_factors = dict(sorted(factors.items()))
        tuple_factors = tuple(sorted_factors.values())
        print(tuple_factors)

        time_finish = time()
        logging.debug(f"Total execution time: {time_finish - time_start}")
        logging.debug(f"Number of CPU cores: {cpu_count()}")
        return tuple_factors


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(processName)s %(message)s')

    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158,
                 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212,
                 2662765, 5325530, 10651060]
