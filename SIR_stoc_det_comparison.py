import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10, 5)  #set default figure size
import numpy as np
from numpy import exp
from gillespie_cl import gillespie
from scipy.integrate import odeint

"""
All individuals in the population are assumed to be in one of the four states.
The states are: susceptible (S), exposed (E), infected (I) and removed (R).
Comments:
    Those in state R have been infected and either recovered or died.
    Those who have recovered are assumed to have acquired immunity.
    Those in the exposed group are not yet infectious.

The flow across states follows the path S-> E-> I-> R

Calling the factors involved in the relations between quantities:
    beta: the transmission rate (the rate at which individuals bump into others and expose them to the virus).
    sigma: the infection rate (the rate at which those who are exposed become infected)
    gamma: the recovery rate (the rate at which infected people recover or die).
    
The relations between fractions (s+ e+ i+ r= 1) of population in each state are given by the dynamic eq:
    (ds/dt)(t) = -beta(t)*s(t)*i(t)
    (de/dt)(t) = beta(t)*s(t)*i(t) - sigma*e(t) 
    (di/dt)(t) = sigma*e(t) - gamma*i(t)

Being the population (pop_size) a constant in the model, calculating 3 quantities (S, E & I) we already know R:
    R= pop_size -S -E -I

The cumulative amount of cases (C) is given by: C = I + R
The system of equations written above can be expressed in vector form.
Being   \vec{x} = (s, e, i) and F( x, t, R0) = (dx/dt)
    \vec{x} is the state vector (array_like)
    t is time (scalar)
    R0 is the effective transmission rate, defaulting to a constant
"""
     #sigma = 1 would mean each and every exposed person gets infected

def F(x,t, R0=1.06):
    """
    Time derivative of the state vector
    """
    gama  = 0.05
    sigma = 0.5
    s, e, i= x
    beta = R0(t)*gama if callable(R0) else R0*gama  # If need be, R0 can be the constant value set
    q = beta*s*i

    s_dot = -q
    e_dot = q - sigma*e
    i_dot = sigma*e - gama*i

    return s_dot, e_dot, i_dot

# Also needed are the initial conditions: 
s0=0.999 
i0=0.001 
e0= 4*i0

x_0 = s0, i0, e0

def solve_path(R0, t_vec, x_init=x_0):
    """
    Solve for i(t) and c(t) via numerical integration, given the time path for R0.
    """
    G = lambda x, t: F(x, t, R0)
    s_path, e_path, i_path = odeint(G, x_init, t_vec).transpose()

    c_path = 1 - s_path - e_path    # cumulative cases
    return i_path, c_path

t_length = 450
grid_size = 1000
t_vec = np.linspace(0, t_length, grid_size)

label_ = [f'$R_0 = 2$']
i_paths, c_paths = [], []
i_path, c_path = solve_path(2, t_vec)
i_paths.append(i_path)
c_paths.append(c_path)

params_this_time = [1, 0.5, 3*(10**(5))]
q=gillespie()

ñ = q.sir_gillespie(params_this_time, i_0=4*i0*params_this_time[2])
t_list = ñ[3]
inf_list= ñ[4]

fig, ax = plt.subplots(sharex=False, sharey=False)

color = 'crimson'
for path, label in zip(i_paths, label_):
    ax.set_ylabel('Deterministic infected(t)', color=color)  # we already handled the x-label with ax1
    ax.tick_params(axis='y', labelcolor=color)
    ax.plot(t_vec, path, color=color, label=label)

ax2 = ax.twinx()  # instantiate a second Axes that shares the same x-axis

peak_infected_t_st = float(t_list[np.argmax(inf_list)])
peak_infected_t_det = float(t_vec[np.argmax(i_paths)])

razon_t = peak_infected_t_det/peak_infected_t_st

t_list = np.multiply(t_list, razon_t)

color = 'indigo'
ax2.set_ylabel('Stochastic infected(t)', color=color)
ax2.plot(t_list, inf_list, color=color, label='stochastic')
ax2.tick_params(axis='y', labelcolor=color)
ax.legend(loc='upper left')
fig.savefig('chequeo.pdf', format='pdf')
fig.show()


