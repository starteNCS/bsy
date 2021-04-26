import numpy as np
import matplotlib.pyplot as plt
import bintrees.rbtree as rbtree

ankunft_tree = rbtree.RBTree()
lmb = 0.1
mue = 0.2
nmax = 1000000
zwischenankunft = np.random.exponential(1. / lmb, nmax)

ankunft = np.cumsum(zwischenankunft)
bearbeitungszeit = np.random.exponential(1. / mue, nmax)
for z in zip(ankunft, bearbeitungszeit):
    ankunft_tree.insert(z[0], z[1])

start = []
end = []
latest = 0.


def do_work(key: float, value: float):
    if latest < key:
        start.append(key)
        end.append(key + value)
        last = latest + value
    else:
        start.append(latest)
        end.append(latest + value)
        last = latest + value


while ankunft_tree.count > 0:
    current_item = ankunft_tree.min_item()
    do_work(current_item[0], current_item[1])
    ankunft_tree.remove(current_item[0])

start = np.array(start)
end = np.array(end)
plt.hist(end-ankunft,bins=100)
plt.show()