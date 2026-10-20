import h5py
import matplotlib.pyplot as plt
import numpy as np

# 1. Загружаем данные из файла
with h5py.File("simulation_results.h5", "r") as f:
    t = f["time"][:]
    r = f["radius"][:]
    T = f["temperature"][:]
    eta = f["eta"][:]

# 2. Ищем момент наибольшей интенсивности реакции (t_нир) в центре шара
deta_dt_center = np.diff(eta[:, 0]) / np.diff(t)
idx_nir = np.argmax(deta_dt_center)
t_nir = t[idx_nir]

# 3. Извлекаем профиль температуры в этот момент
T_profile = T[idx_nir, :]

# 4. СТРОИМ ОДИН КРУПНЫЙ КРАСИВЫЙ ГРАФИК
plt.figure(figsize=(8, 5.5))

# Отрисовка профиля (переводим радиус в см)
plt.plot(
    r * 100,
    T_profile,
    "r-",
    lw=2.5,
    label=f"Профиль Т при t = {t_nir:.1f} с",
)

# Оформление осей и сетки
plt.xlabel("Радиус шара, см", fontsize=11)
plt.ylabel("Температура T, К", fontsize=11)
plt.title(
    f"Распределение температуры в шаре в момент t_нир ({t_nir:.1f} с)",
    fontsize=12,
    pad=15,
)
plt.grid(True, which="both", linestyle="--", alpha=0.7)
plt.legend(fontsize=10)

# Автоматическое выравнивание полей и сохранение
plt.tight_layout()
plt.savefig("temperature_profile_at_t_nir.png", dpi=300)
plt.show()
