import numpy as np
import matplotlib.pyplot as plt
import bintrees.rbtree as rbtree
import time

ankunft_tree = rbtree.RBTree()
lmb = 0.1
mue = 0.2
nmax = 20000
zwischenankunft = np.random.exponential(1. / lmb, nmax)

ankunft = np.cumsum(zwischenankunft)
bearbeitungszeit = np.random.exponential(1. / mue, nmax)
for z in zip(ankunft, bearbeitungszeit):
    ankunft_tree.insert(z[0], z[1])

tic = time.perf_counter()
start = []
end = []
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


while ankunft_tree.count > 0:
    current_item = ankunft_tree.pop_min()
    do_work(current_item[0], current_item[1])


start = np.array(start)
end = np.array(end)
toc = time.perf_counter()

plt.hist(end-ankunft,bins=100)
plt.show()
print(f"Took {toc - tic:0.4f}")