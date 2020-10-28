import PyGnuplot as gp
import numpy as np
i = 5
X = np.arange(i)
Y = np.sin(X / (2 * np.pi))
Z = Y ** 2.0
gp.s([X, Y, Z])
gp.c('splot sin(x) u 1:2:3 with lines')
while True:
    i=i+1
    X = np.arange(i)
    Y = np.sin(X / (2 * np.pi))
    Z = Y ** 2.0
    gp.s([X, Y, Z])
    gp.c('replot')
