import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sympy as sp


x = sp.symbols('x')
y = sp.Function('y')(x)
ode = sp.Eq(y.diff(x), -2 * y)
ics = {y.subs(x, 0): sp.sqrt(2)}
sol_sym = sp.dsolve(ode, ics=ics)
y_sym_expr = sol_sym.rhs
y_sym_func = sp.lambdify(x, y_sym_expr, 'numpy')
sp.pprint(sol_sym)


def dydx(x, y):
    return -2 * y
sol_num = solve_ivp(dydx, [0, 10], [sp.sqrt(2).evalf()], t_eval=np.linspace(0, 10, 500))
x_plot = np.linspace(0, 10, 500)
y_sym = y_sym_func(x_plot)
y_num = sol_num.y[0]


plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(x_plot, y_sym, label='SymPy')
plt.plot(sol_num.t, y_num, label='SciPy', linestyle='--')
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Оба решения')
plt.legend()
plt.grid()
plt.subplot(1, 2, 2)
plt.plot(x_plot, y_sym - y_num)
plt.xlabel('x')
plt.ylabel('Разность (SymPy - SciPy)')
plt.grid()
plt.tight_layout()
plt.show()