from threading import Semaphore
import concurrent.futures
from time import sleep
import numpy as np

class Product:
    state: int = 0  # 0: frei, 1: bei produzent, 2: in auslage, 3: bei konsument
    product: float = 0
    id: int = 0


lmb = 0.1
mue = 0.2
nmax = 20
amount_worker = 5

warteraum: list = [Product() for i in range(nmax)]
warteraum_semaphore: list = [Semaphore() for i in range(nmax)]


def produce(index: int):
    warteraum_semaphore[index].acquire()
    warteraum[index].state = 1
    time = np.random.exponential(1 / lmb) / 10
    print(f"produce: {time} \n")
    sleep(time)
    product = np.random.exponential(1 / lmb)/ 10
    warteraum[index].product = product
    warteraum[index].state = 2
    warteraum_semaphore[index].release()


def consume(index: int):
    warteraum_semaphore[index].acquire()
    warteraum[index].state = 3
    print(f"consume: {warteraum[index].product} \n")
    sleep(warteraum[index].product)
    warteraum[index].state = 0
    warteraum_semaphore[index].release()


def producer_thread():
    with concurrent.futures.ThreadPoolExecutor(max_workers=amount_worker) as executor:
        while True:
            for i in range(nmax):
                if warteraum[i].state == 0:
                    executor.submit(produce, i)


def consumer_thread():
    with concurrent.futures.ThreadPoolExecutor(max_workers=amount_worker) as executor:
        while True:
            for i in range(nmax):
                if warteraum[i].state == 2:
                    executor.submit(consume, i)


def run():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer_thread)
        executor.submit(consumer_thread)


run()
