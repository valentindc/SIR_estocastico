import numpy as np
import matplotlib.pyplot as plt
from gillespie_cl import gillespie

q=gillespie()

for j in range(3):
    params_this_time = [0.55, 0.5, 2*(10**(4+j))]
    inf_list, t_list= [], []
    outbreaks = 30
    for i in range(outbreaks):
        ñ = q.sir_gillespie(params_this_time, timecap=True)
        t_list.append(ñ[4])
        inf_list.append(ñ[5])

t_arr = np.asarray(t_list, dtype="object")
#print(np.shape(t_arr))

"""
for j in range(np.shape(t_arr)):
    for k in range(100):
        print(t_list[(t_list>(10*k))])

    print()
"""



def tolerant_mean(arrs):
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return arr.mean(axis = -1), arr.std(axis=-1)

y, error = tolerant_mean(inf_list)
x = tolerant_mean(t_list)[0]
#plt.plot(np.arange(len(y))+1, y, color='green')
plt.plot(x, y, marker = '*')

for j in range(np.shape(t_arr)[0]):
    plt.scatter(t_list[j], inf_list[j], s=1)        
plt.xlabel(r'$t$', fontsize=15)
plt.ylabel(r'$i(t)$', fontsize=15)


plt.show()
