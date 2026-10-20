from scipy import linalg
A=[[4, -2, 21], [1, 1, -3], [9, 5, 0]]
eig_val, V = linalg.eig(A)
print(eig_val)
print(V)
