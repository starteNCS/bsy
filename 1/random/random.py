from numpy.random import default_rng
import matplotlib.pyplot as plt

rng = default_rng()

a = 100
n = 100000

generated = rng.integers(0, a, n)
generated.sort

diff_arr = []
for i in range(n - 1):
    diff = abs(generated[i + 1] - generated[i])
    diff_arr.append(diff)

fig, ax = plt.subplots()
ax.hist(diff_arr, 50)
plt.show()
