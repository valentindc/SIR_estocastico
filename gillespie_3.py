import numpy as np
import matplotlib.pyplot as plt
from gillespie_cl import gillespie

q=gillespie()
w=gillespie()

for j in range(3):
    params_this_time = [0.5, 0.5, 2*(10**(4+j))]
    k= []
    outbreaks = 3000
    for i in range(outbreaks):
        ñ = q.sir_gillespie(params_this_time)[0]
        k.append(ñ)
        
    w.plot_ue_ut(k, params_this_time[2])
    plt.xlabel(r'$ \frac{n}{N^{2/3}}$', fontsize=15)
    plt.ylabel(r'$ \frac{U_n (N)}{U_n (\infty)}$', fontsize=15)

plt.show()

"""

fig = plt.figure(figsize=(5, 4), layout="constrained")
axs = fig.subplots(1, 1)

n_bins = 50

x1, y1 = axs.ecdf(k, label="CCDF", complementary=True)
n, bins, patches = axs.hist(k, bins=n_bins, density=True, histtype="step", cumulative=-1, label="Reversed Cumulative histogram")


# Label the figure.
fig.suptitle("Cumulative distributions")
axs.grid(True)
axs.legend()
axs.set_xlabel("#")
axs.set_ylabel("!")
axs.label_outer()

plt.show()
"""
