import numpy as np
import matplotlib.pyplot as plt
from gillespie_cl import gillespie
from decimal import Decimal
from tqdm import tqdm

q=gillespie()

fig = plt.figure(figsize=(9, 9), layout="constrained")
axs = fig.subplots(3, sharex=False, sharey=False)

outbreaks=3000

for j in tqdm(range(3)):
    parameters = [1, 1, 10**(3+j)]
    k= np.zeros(shape=outbreaks)
    
    for i in tqdm(range(outbreaks)):
        infPerOutbreak = q.sir_gillespie(parameters)[0]
        k[i] = infPerOutbreak

    k = np.sort(k)
    
    ccdf_label="CCDF, N= %.1e" % Decimal(parameters[2])
    plot2 = axs[0].ecdf(k, complementary=True, label=ccdf_label)
    
    ys =np.asarray(plot2.get_ydata())
    ys = np.delete(ys, -1)
    xs =np.asarray(plot2.get_xdata())
    xs = np.delete(xs, -1)
    
    u_n_inf = [q.U(x, parameters[2]) for x in k]
    axs[1].plot(k, u_n_inf, ms= 5, label='Theoretical U_n')

    xnorm = np.divide(xs, parameters[2]**(2/3)) # As I don't intend to use simply n as the x axis, "normalize" it with N
    y2 = np.divide(ys, u_n_inf)

    N_label='%.1e' % Decimal(parameters[2])
    axs[2].scatter(xnorm, y2, s= 5,label= N_label)
    
axs[2].set_ylabel(r'$ \frac{U_n (N)}{U_n (\infty)}$')
axs[2].set_yticks(np.linspace(min(y2), max(y2), dtype=int))

# Label the figure.
fig.suptitle("Cumulative distributions")
for ax in axs:
    ax.grid(True)
    ax.legend()
    ax.label_outer()

plt.show()

