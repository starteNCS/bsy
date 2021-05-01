import numpy as np
import matplotlib.pyplot as plt
import bintrees.rbtree as rbtree
import time
import threading

ankunft_tree = rbtree.RBTree()
lmb = 0.1
mue = 0.2
nmax = 20000
nmaxthreads = nmax

tree_sema = threading.BoundedSemaphore(value=nmaxthreads)

zwischenankunft = np.random.exponential(1. / lmb, nmax)

ankunft = np.cumsum(zwischenankunft)
bearbeitungszeit = np.random.exponential(1. / mue, nmax)
for z in zip(ankunft, bearbeitungszeit):
    ankunft_tree.insert(z[0], z[1])

tic = time.perf_counter()
start: list = []
end: list = []
latest = 0.


def do_work(key: float, value: float):
    global latest
    if latest < key:
        start.append(key)
        end.append(key + value)
        latest = latest + value
    else:
        start.append(latest)
        end.append(latest + value)
        latest = latest + value


# def process_task

while ankunft_tree.count > 0:
    with tree_sema:
        current_item = ankunft_tree.pop_min()
        threading.Thread(target=do_work, args=(
            current_item[0], current_item[1]), daemon=True).start()
        # do_work(current_item[0], current_item[1])


start = np.array(start)
end = np.array(end)
toc = time.perf_counter()

print(f"Took {toc - tic:0.4f}")

plt.hist(end-ankunft, bins=100)
plt.show()
