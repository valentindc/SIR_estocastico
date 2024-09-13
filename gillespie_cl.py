import numpy as np
import scipy.special as sp

class gillespie():

    debug = False

    def __init__(self):
        if self.debug:
            print('intializing Gillespie algorithm')
        return
    
    def sir_gillespie(self, parms=[0.08, 0.05, 2000.0], i_0 =1, timecap =False):
        """
        parms = [beta, gamma, N]
        In the function definition a default value is given in case none is provided
        R_0:= beta/gamma; basic reproductive ratio (the average number of secondary
        cases arising from an average primary case in an entirely susceptible population)
        1/gamma:= recovery time
        i_0: initially infected
        Timecap: to cut the simulation short at a certain time if necessary
        """
        
        s_list, i_list, r_list, y_list, time_list = [], [], [], [], []
        
        # infections at t=0
        i = i_0
        
        # initially susceptible population
        s = parms[2]-i
        y = 0
        r = 0
        tcap = 20

        u = [s, i ,r ,y]

        #Initial values
        s_list.append(u[0])
        i_list.append(u[1])
        r_list.append(u[2])
        y_list.append(u[3])
        time_list.append(0)

        beta, gamma, n = parms

        # transition rates
        ainf = beta*s*i/n
        arec = gamma*i
   
        a0 = ainf + arec
        pinf = ainf/a0    # infection probability
        tp = 0
        tstep =0

        while i>0:
            r1 = np.random.uniform()
            r2 = np.random.uniform() 
            dt = -np.log(r2)/a0
            tp = tp+dt
            tstep = tstep+1

            if r1 < pinf:
                s = s-1
                i = i+1
                y = y+1
            else:    # prec=1-pinf
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
            time_list.append(tp)

            if timecap and (tp >tcap):
                return y_list[-1], tp, tstep, np.asarray(time_list), np.asarray(i_list)
                
        return y_list[-1], tp, tstep, np.asarray(time_list), np.asarray(i_list)
    
    
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
        q = sum(self.G(n) for n in range(n, int(5*N)))
        return q
