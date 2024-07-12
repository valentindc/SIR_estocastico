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
        p = sim.sir_gillespie(params_this_time)
        k.append(p[1])
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


"""
sline = plt.plot(, color="red", linewidth=2)
iline = plt.plot(, color="green", linewidth=2)
rline = plt.plot(, color="blue", linewidth=2)

plt.xlabel("Time", fontweight="bold")
plt.ylabel("Number", fontweight="bold")
legend = plt.legend(title="Population", loc=5, bbox_to_anchor=(1.25,0.5))
frame = legend.get_frame()
frame.set_facecolor("white")
frame.set_linewidth(0)
"""

"""
def u(a, x):
    return a[0]*x**a[1]

linear = odr.Model(u)
mydata = odr.RealData(x= o[0], y= o[1], sy= o[2])
myodr = odr.ODR(mydata, linear, beta0=[1, 0.33])
output = myodr.run()
output.pprint()
plt.plot(o[0], u(output.beta, o[0]), "g-")
"""

r_0 = params_this_time[0]/params_this_time[1]
plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
#plt.scatter(o[0], o[1])
#plt.errorbar(o[0], o[1], yerr=o[2], fmt="o", ecolor='m')
plt.xlabel(r'total pop.')
plt.ylabel(r'pop. infected')
plt.xscale('log')
plt.yscale('log')

plt.title(f'$R_{0} = %4.2f, outbreaks/(pop. size) = %4.0f $' % (r_0, outbreaks))
plt.show()
