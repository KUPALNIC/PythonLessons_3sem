import sympy as sp

rho, lam, mu = sp.symbols('rho lambda mu', real=True, positive=True)

A = sp.Matrix([
    [0, 0, 0, -1/rho, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, -1/rho, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, -1/rho, 0, 0, 0],
    [-(lam + 2*mu), 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -mu, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, -mu, 0, 0, 0, 0, 0, 0],
    [-lam, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-lam, 0, 0, 0, 0, 0, 0, 0, 0]
])

eigenvals = A.eigenvals()

for val in eigenvals:
    sp.pprint(val)