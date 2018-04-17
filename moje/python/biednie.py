import numpy as np

U = 1.000e-03

rho_h = 1.133e-02
Sigma = 8.253e-04
kin_visc = 1.00e-01
g = 1.11e-07

d= 85



rho_l = np.linspace(rho_h *0.9, rho_h, num=100)

for i in range(len(rho_l)):
    Eo = (rho_h-rho_l[i]) *g *d*d/Sigma
    print("[Eo = %10.3e, rho_l = %10.3e" % (Eo, rho_l[i]))

