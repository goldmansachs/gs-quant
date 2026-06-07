from concurrent.futures import ThreadPoolExecutor
import threading

def worker(item):
    return item * 2

with ThreadPoolExecutor() as executor:
    results = executor.map(worker, [1, 2, 3])
print(list(results))
