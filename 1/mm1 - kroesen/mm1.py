import numpy as np
import matplotlib.pyplot as plt
import time

lmb = 0.1
mue = 0.2
nmax = 500000
zwischenankunft = np.random.exponential(1./lmb,nmax)
ankunft = np.cumsum(zwischenankunft)
bearbeitungszeit = np.random.exponential(1./mue,nmax)

tic = time.perf_counter()
start = []
end = []
last = 0.
for z in zip(ankunft, bearbeitungszeit):
    if last<z[0]:
        start.append(z[0])
        end.append(z[0] + z[1])
        last = last + z[1]
    else:
        start.append(last)
        end.append(last + z[1])
        last = last + z[1]

start = np.array(start)
end = np.array(end)
toc = time.perf_counter()

plt.hist(end-ankunft,bins=100)
plt.show()

print(f"Took {toc - tic:0.4f}")
