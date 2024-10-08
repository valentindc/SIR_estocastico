import numpy as np
import matplotlib.pyplot as plt
from gillespie_cl import gillespie
from tqdm import tqdm

def tolerant_mean(arrs):
    """
    This function is necessary to handle the variable dimension fo arrays both of time and infections
    It uses a masked array to handle the fact for a given ran M a given index n the i_M[n] may be empty
    It returns both mean and std just in case.
    """
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return arr.mean(axis = -1), arr.std(axis=-1)


q=gillespie()
fig, ax = plt.subplots()
marksize = 0.1

inf_list_1, t_list_1= [], []
outbreaks = 50



params_ = [0.45, 0.5, 2*(10**(5))] # To make 50 outbreaks with R_0<1
for i in tqdm(range(outbreaks)):
    ñ = q.sir_gillespie(params_, i_0=1200, timecap=True) #timecap= True makes it so the simulations goes only up to t<=tcap, parameter can be changed in gillespie_cl.py
    t_list_1.append(ñ[3])
    inf_list_1.append(ñ[4])

r_0_label = f'$R_{0} = %1.2f $' %(params_[0]/params_[1])

t_arr = np.asarray(t_list_1, dtype="object")

for j in range(np.shape(t_arr)[0]):
    line1, = ax.plot(t_list_1[j], inf_list_1[j], marker='+', ms=marksize, color='indigo' )
    
line1.set_label(r_0_label)
y, error = tolerant_mean(inf_list_1) # There was an attempt at using the the mean +-std to draw a "most likely outbreak area"
x = tolerant_mean(t_list_1)[0]

label1 = f'Avg for R_0 = %1.2f'%(params_[0]/params_[1])
ax.plot(x, y, color='darkorange', label= label1)



params_ = [0.55, 0.5, 2*(10**(5))] # To make 50 outbreaks with R_0>1
r_0_label = f'$R_{0} = %1.2f $' %(params_[0]/params_[1])
inf_list, t_list= [], []

for i in tqdm(range(outbreaks)):
    ñ = q.sir_gillespie(params_, timecap=True, i_0=1200)
    t_list.append(ñ[3])
    inf_list.append(ñ[4])

for j in range(np.shape(t_arr)[0]):
    line2, =ax.plot(t_list[j], inf_list[j], marker= 'x', ms=marksize, color='crimson')

y_2, error_2 = tolerant_mean(inf_list)
x_2 = tolerant_mean(t_list)[0]

label2 = f'Avg for R_0 = %1.2f'%(params_[0]/params_[1])

ax.plot(x_2, y_2, color='darkgreen', label=label2)
line2.set_label(r_0_label)
plt.xlabel(r'$t$', fontsize=15)
plt.ylabel(r'$i(t)$', fontsize=15)
plt.legend(loc='upper left')

#Output is all the infections curves and their respective average for each r_0
plt.show()
