import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('signal01.dat')
t = np.arange(data.size)
window = 10
cumsum = np.cumsum(data)
cumsum = np.insert(cumsum, 0, 0.0)
i = np.arange(data.size)
start = np.maximum(0, i - window + 1)
window_sum = cumsum[i + 1] - cumsum[start]
window_len = i - start + 1
filtered_data = window_sum / window_len

plt.figure(figsize=(12, 5))
plt.plot(t, data, alpha=0.7)
plt.plot(t, filtered_data, linewidth=2)
plt.legend(['Сырой сигнал', 'Отфильтрованный'])
plt.grid()
plt.show()