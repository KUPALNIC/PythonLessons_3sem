import h5py
import matplotlib.pyplot as plt
import numpy as np

# Читаем данные
with h5py.File("simulation_results.h5", "r") as f:
    t = f["time"][:]
    r = f["radius"][:]
    T = f["temperature"][:]
    eta = f["eta"][:]

# Находим индекс момента максимальной интенсивности (взрыва) в центре
# Превращение идет быстрее всего там, где dT/dt максимален в центре
dT_dt_center = np.diff(T[:, 0]) / np.diff(t)
idx_explosion = np.argmax(dT_dt_center)
t_explosion = t[idx_explosion]

# 1. График температур в ключевых точках
plt.figure(figsize=(10, 5))
plt.plot(t, T[:, 0], "r-", label="Центр (r = 0)")
plt.plot(t, T[:, len(r) // 2], "g--", label="Середина (r = R/2)")
plt.plot(t, T[:, -1], "b-", label="Поверхность (r = R)")
plt.axvline(
    t_explosion, color="gray", linestyle=":", label=f"Взрыв ({t_explosion:.1f} с)"
)
plt.xlabel("Время, с")
plt.ylabel("Температура, К")
plt.title("Динамика температуры в шаре")
plt.legend()
plt.grid(True)
plt.savefig("temperature_plots.png")
plt.show()

# 2. ТЕПЛОВАЯ КАРТА (Heatmap)
plt.figure(figsize=(12, 6))
# Создаем сетку для отображения
X, Y = np.meshgrid(t, r)
# Транспонируем T, чтобы сопоставить размерностям сетки
mesh = plt.pcolormesh(X, Y, T.T, cmap="jet", shading="auto")
plt.colorbar(mesh, label="Температура, К")
plt.xlabel("Время, с")
plt.ylabel("Радиус шара, м")
plt.title("Пространственно-временная тепловая карта (Heatmap)")
plt.savefig("heatmap.png")
plt.show()
