import numpy as np
import matplotlib.pyplot as plt
from gillespie_cl import gillespie
from tqdm import tqdm

"""
In this script I intend to do a sweep in r_0 values of the SIR model
implemented using gillespie algorithm
"""

sim = gillespie()

colorss = ['crimson', 'gold', 'blue', 'forestgreen', 'orangered', 'darkorchid', 'darkorange', 'black', 'deeppink']
n_bins = 50
o=[[], [], [], []]

for j in range(7):
    #                   beta,                    gamma,     N
    params_this_time = [0.5+(-j*0.0125 + 0.04),    0.5,    2*10**5]
    outbreaks = 4000
    r_0 = params_this_time[0]/params_this_time[1]
    k = np.zeros(shape=outbreaks)
    for i in tqdm(range(outbreaks)):
        p = sim.sir_gillespie(params_this_time, i_0=1)
        k[i] =p[0]
    
    labell='$R_{0} = %4.2f$' % (params_this_time[0]/ params_this_time[1] )
    weights = np.ones_like(k)/float(outbreaks)
    plt.hist(k, bins=n_bins, color=colorss[j], density=True, histtype='step', facecolor='g', alpha=0.75, label=labell, weights=weights)

plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
plt.yscale('log')
plt.xlabel('Total infected per outbreak')
plt.legend()
plt.title(f'Outbreak size for different $R_{0}$')
plt.show()

