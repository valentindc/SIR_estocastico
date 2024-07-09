import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
from decimal import Decimal

class gillespie():

    debug = False

    def __init__(self):
        if self.debug:
            print('intializing Gillespie algorithm')
        return
    
    def sir_gillespie(self, parms=[0.08, 0.05, 2000.0]):
        """
        parms = [beta, gamma, N]
        In the function definition a default value is given in case none is provided
        R_0:= beta/gamma; basic reproductive ratio (the average number of secondary
        cases arising from an average primary case in an entirely susceptible population)
        1/gamma:= recovery time
        """
        R_0 = parms[0]/parms[1]
        s_list, i_list, r_list, y_list = [], [], [], []
        # infections at t=0
        i = 5
        # initially susceptible population
        s = parms[2]-i
        y = 0
        r = 0

        u = [s, i ,r ,y]

        #Initial values
        s_list.append(u[0])
        i_list.append(u[1])
        r_list.append(u[2])
        y_list.append(u[3])

        beta, gamma, n = parms

        ainf = beta*s*i/n
        arec = gamma*i
   
        a0 = ainf + arec
        pinf = ainf/a0
        #prec = arec/a0
        #tp = 0

        while i>0:
            r1 = np.random.uniform()
            #r2 = np.random.uniform() 
            #dt = -np.log(r2/a0)
            #tp = tp+dt

            if r1 < pinf:
                s = s-1
                i = i+1
                y = y+1
            else:
                r = r+1
                i = i-1
        
            if i==0: break
            ainf = beta*s*i/n
            arec = gamma*i
            a0 = ainf + arec
            pinf = ainf/a0

            s_list.append(s)
            i_list.append(i)
            r_list.append(r)
            y_list.append(y)

        #print(y_list[-1])
        # take the last value of total cases, divided by total population *100
        percent_infected = 100*y_list[-1]/parms[2] 
        # return only the values of total infected, percent of pop. infected and R_0
        return y_list[-1], percent_infected, R_0
    
        
    def G(self, n):
        """
        THIS EXPRESSION IS VALID ONLY ON THE EPIDEMIC THRESHOLD (alpha = 1 as per the article cited below)
        Using expression (10) given in http://dx.doi.org/10.1140/epjb/e2012-30117-0
        and the approximate for large n exactly after it
        """
        if 0 < n < 155:
            s = sp.gamma(n-0.5)/( ((2)*np.pi**0.5) * sp.gamma(n+1) )
            return s
        else:
            s = (4*np.pi)**-0.5
            if n==0: 
                t=0 
            else: 
                t= n**-1.5
            kk = s*t
            return kk


    def U(self, n, N):
        """
        just a summation but with care to move the upper limit as we're interested in 
        sweeping various orders of magnitude of populations size 
        """
        n = int(n) # force it into an integer just in case
        q = sum(self.G(n) for n in range(n, 2*N))
        return q

    
    def ecdf(self, a):
        """
        First step on building the ecdf over the argument list a
        """
        x, counts = np.unique(a, return_counts=True)
        cusum = np.cumsum(counts)
        return x, cusum / cusum[-1]


    def plot_ue_ut(self, a, N):
        """
        Using the output from ecdf()
        """
        x, y = self.ecdf(a)
        x = np.insert(x, 0, x[0])
        y = np.insert(y, 0, 0.)
        y_1 = 1- y  # As the ccdf is actually needed
        y_2 = np.zeros(shape=len(x))
        for aj in range(len(x)):
            """
            each element in the array will be the value of the ccdf (U_n following paper notation)
            divided by the theoretical expression built in the epidemic threshold evaluated on n
            """
            y_2[aj] = y_1[aj]/self.U(x[aj], N)

        x_1 = x/N**(2/3)    # figure 4 of the article uses this as the horizontal axis
        labell='%.1e' % Decimal(N)
   
#        plt.plot(x_1, y_2, drawstyle='steps-post', label=labell)
        plt.scatter(x_1, y_2, label=labell, s=10)
        plt.legend()
#        plt.plot(x_1, y_2, marker='o', label=labell)

        plt.grid(True)
        