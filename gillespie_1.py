import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
from gillespie_cl import gillespie

"""
In this script I intend to do a sweep in r_0 values of the SIR model
implemented using gillespie algorithm
"""

sim = gillespie()

colorss = ['crimson', 'gold', 'blue', 'forestgreen', 'orangered', 'darkorchid', 'darkorange', 'black', 'deeppink']

n_bins = 50
o=[[], [], [], []]

for j in range(7):
    #                  beta,    gamma,  N
    params_this_time = [0.5+(-j*0.0125 + 0.04),    0.5,    2*10**5]
    r_0 = params_this_time[0]/params_this_time[1]
    o[0].append(params_this_time[2])
    k= []
    outbreaks = 5000
    for i in range(outbreaks):
        k.append(sim.sir_gillespie(params_this_time)[1])
    med = np.mean(k)
    labell='$R_{0} = %4.2f$' % (params_this_time[0]/ params_this_time[1] )
    weights = np.ones_like(k)/float(outbreaks)
    
    plt.hist(k, bins=n_bins, color=colorss[j], density=True, histtype='step',
             facecolor='g', alpha=0.75, label=labell, weights=weights)
    
    o[1].append(med)
    sd = np.std(k)
    o[2].append(sd)
    o[3].append(params_this_time[0]/ outbreaks*params_this_time[1])

plt.yscale('log')
plt.legend()
plt.show()


plt.scatter(o[3], o[1])
plt.xlabel('R_0')
plt.ylabel('Median % pop. outbreak')
plt.show()

