import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# https://apmonitor.com/pdc/index.php/Main/SimulateCOVID19
# https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/

N = 1000 # population size

def odes(x, t):
    # constants
    t_incubation = 3  # time for an exposed person to become infected
    t_infective = 10 # time for an infected person to recover
    beta = 0.3 # number of infectious interactions per day per infected
    alpha = 1/t_incubation # average number of exposed to infected per day
    gamma = 1/t_infective # average number of infected to recovered per day

    #ODEs to vector elements
    s = x[0]
    e = x[1]
    i = x[2]
    r = x[3]

    #define ODEs
    dsdt = -1*beta*s*i / N
    dedt = beta*s*i / N - alpha*e
    didt = alpha*e - gamma*i
    drdt = gamma*i

    return [dsdt, dedt, didt, drdt]

i0 = 1 # initial infected
e0 = 0 # initial exposed
r0 = 0 # initial recovered
s0 = N - i0 - e0 - r0
x0 = [s0, e0, i0, r0] # initial s, e, i, and r

t = np.linspace(0, 160, 160)

x = odeint(odes, x0, t)

s = x[:, 0]
e = x[:, 1]
i = x[:, 2]
r = x[:, 3]

plt.figure(figsize=(8, 5))
plt.subplot(2, 1, 1)
plt.plot(t, s, color='blue', lw=3, label = 'Susceptible')
plt.plot(t, e, color='green', lw=3, label = 'Exposed')
plt.plot(t, i, color='orange', lw=3, label = 'Infected')
plt.plot(t, r, color='red', lw=3, label = 'Recovered')
plt.legend()
plt.show()