import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

u0 = np.loadtxt('func.txt')
N = u0.size
steps = 255

A = np.eye(N) - np.roll(np.eye(N), 1, axis=1)
M = np.eye(N) - 0.5 * A

eigvals, V = np.linalg.eig(M)
V_inv = np.linalg.inv(V)

u0_ = V_inv @ u0
n_vals = np.arange(steps + 1)[:, None]
eigvals_ = eigvals ** n_vals
u_tilde_time = eigvals_ * u0_
u = np.real((V @ u_tilde_time.T).T)

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, N - 1)
ax.set_ylim(u.min() - 0.1, u.max() + 0.1)
line, = ax.plot([], [], lw=2, color='blue')
ax.grid(True, linestyle='--', alpha=0.5)

def animate(i):
    line.set_data(np.arange(N), u[i])
    return line,

anim = FuncAnimation(fig, animate, frames=steps + 1, interval=50, blit=True)
anim.save('process_evolution.gif', writer='pillow', fps=20)
plt.close()