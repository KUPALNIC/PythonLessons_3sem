import numpy as np

matrix = [np.random.randint(-10, 10, size=(4,4)) for _ in range(10)]
print(np.max([np.linalg.det(mat) for mat in matrix]))