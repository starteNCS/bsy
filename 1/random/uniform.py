from numpy.random import default_rng
import matplotlib.pyplot as plt
import numpy as np

rng = default_rng()

n = 100000
m = 10

while True:
    random_uniform = rng.uniform(size=n)
    f_result = []
    for i in random_uniform:
        f = -(1/m)*np.log(i)
        f_result.append(f)

    print("f(p) = -(1/m) * ln(p)")
    print("Average: ", np.average(f_result))
    print("Varianz: ", np.var(f_result))

    fig, ax = plt.subplots()
    ax.hist(f_result, 50)
    plt.show()

    m = int(input())