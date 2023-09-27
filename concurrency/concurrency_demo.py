import concurrent.futures
import time
import random
import requests


def io_bound_task(index_value, delay=10):

    url = f'https://httpbin.org/delay/{delay}'

    print(f'Task {index_value} started at time {time.time()}')
    r = requests.get(url)
    print(f'Task {index_value} completed at time {time.time()}')

    return r.status_code


def cpu_bound_task(index_value, count=1e7):

    import random

    print(f'Task {index_value} started at time {time.time()}')

    mylist = []
    for i in range(count):
        mylist.append(random.random())
    print(f'Task {index_value} ended at time {time.time()}')

    return sum(mylist)


if __name__ == '__main__':

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {
            executor.submit(
                io_bound_task, i, random.randint(2, 10)
                ): i for i in range(100)
            }
        for future in concurrent.futures.as_completed(future_to_url):
            response = future_to_url[future]
            try:
                data = future.result()
            except Exception:
                pass
