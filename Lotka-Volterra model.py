import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def odes(values, t):
    alpha = 0.1 #reproduction rate of prey
    beta = 0.02 #mortality rate of predator due ot prey
    delta = 0.02 #reproduction rate of predator per prey
    gamma = 0.4 #mortality rate of predator

    #ODEs to vector elements
    x = values[0]
    y = values[1]

    #define ODEs
    dxdt = alpha*x - beta*x*y
    dydt = delta*x*y - gamma*y

    return [dxdt, dydt]

x0 = 10
y0 = 10
values = [x0, y0] # initial predators and prey

t = np.linspace(0, 160, 160)

res = odeint(odes, values, t)

x = res[:, 0]
y = res[:, 1]

plt.figure(figsize=(8, 5))
plt.subplot(2, 1, 1)
plt.plot(t, x, color='blue', lw=3, label = 'Prey')
plt.plot(t, y, color='red', lw=3, label = 'Predators')
plt.legend()
plt.show()