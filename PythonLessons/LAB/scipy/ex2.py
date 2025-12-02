import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

with open('text1.txt', 'r') as f:
    lines = f.readlines()

N = int(lines[0].strip())
A = np.array([list(map(float, lines[i].split())) for i in range(1, 1 + N)])
b = np.array(list(map(float, lines[1 + N].split())))

x = solve(A, b)

plt.figure(figsize=(8, 5))
plt.bar(range(len(x)), x, color='steelblue', edgecolor='black', alpha=0.8)
plt.xlabel('i')
plt.ylabel('x[i]')
plt.title('Решение системы Ax = b')
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(range(len(x)))
plt.show()