from shutil import which

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline



# Константы для перевода в энергию
h = 6.62607015e-34  # Дж·с
c = 299792458       # м/с
eV = 1.602176634e-19


def w_to_E(list):
    # E=np.array([])
    E=(h*c)/(list*1e-9) / eV
    return E

# =====================================================================
# 1. ИСХОДНЫЕ ДАННЫЕ И ПРАВИЛЬНЫЙ ПЕРЕВОД В НАНОМЕТРЫ (нм)
# =====================================================================

# Данные Неона (Ne): длины волн в Ангстремах (Å) переводим в нм (делением на 10)
neon_drum = np.array([
    2842, 2826, 2802, 2782, 2766, 2728, 2718, 2702, 2690, 2672,
    2656, 2632, 2624, 2600, 2590, 2572, 2550, 2528, 2500, 2486, 2218
])
neon_wl = np.array([
    6717.04, 6678.28, 6598.95, 6532.88, 6506.53, 6402.24, 6382.99, 6334.42,
    6304.79, 6266.49, 6217.28, 6163.59, 6143.06, 6096.14, 6074.34, 6030.00,
    5975.53, 5944.83, 5881.89, 5852.49, 5400.56
]) / 10.0  # Перевод Å -> нм

# Данные Ртути (Hg): длины волн ОСТАВЛЯЕМ КАК ЕСТЬ, они уже в нм
mercury_drum = np.array([2896, 2662, 2456, 2444, 2260, 1834, 1160, 598])
mercury_wl = np.array([690.7, 623.4, 579.1, 577.0, 546.1, 491.6, 435.8, 404.7])

# Объединяем опорные точки для построения единой калибровочной кривой
calib_drum = np.concatenate((neon_drum, mercury_drum))
calib_wl = np.concatenate((neon_wl, mercury_wl))

# Сортируем массивы по возрастанию делений барабана для корректной интерполяции
sort_idx = np.argsort(calib_drum)
calib_drum = calib_drum[sort_idx]
calib_wl = calib_wl[sort_idx]

# Построение калибровочного кубического сплайна (барабан -> длина волны в нм)
calib_enegry = w_to_E(calib_wl)
# calib_spline = CubicSpline(calib_drum, calib_wl)

calib_spline = CubicSpline(calib_drum, calib_enegry)
calib_spline_wl = CubicSpline(calib_drum, calib_wl)
# =====================================================================
# 2. ОБРАБОТКА ДАННЫХ ДЛЯ ВОДОРОДА (H)
# =====================================================================

# Экспериментальные деления барабана для линий Бальмера (alpha, beta, gamma, delta)
hydrogen_drum = np.array([2782, 1778, 1134, 702]) # Слева направо: alpha, beta, gamma, delta
m_levels = np.array([3, 4, 5, 6])

#йод
j_drum=np.array([2660, 2572])
j_wl = calib_spline_wl(j_drum)
j_energy = calib_spline(j_drum)




# Определяем длины волн линий водорода по калибровочной кривой (в нм)

hydrogen_wl = calib_spline(hydrogen_drum)
hydrogen_energy = calib_spline(hydrogen_drum)


# Вычисляем энергию излученных фотонов в эВ: E = h*c / lambda
# E_photon = (h * c) / (hydrogen_wl * 1e-9) / eV

#hw = Ry(1/2**2-1/n**2)

# Линеаризация по Бору: En = -R/n^2. Для переходов серии Бальмера (n=2):
# E_m = E_photon
x_axis = (1/4-1/(m_levels**2))

# Находим постоянную Ридберга R через линейный МНК-фиттинг (прямая y = R*x + const)
R_experimental, intercept = np.polyfit(x_axis, hydrogen_energy, 1)

print("--- РЕЗУЛЬТАТЫ РАСЧЕТА ---")
for i, line in enumerate(['H_alpha', 'H_beta', 'H_gamma', 'H_delta']):
    print(f"Линия {line}: барабан = {hydrogen_drum[i]}, рассчит. \lambda = {hydrogen_energy[i]:.2f} нм")
print(f"\nЭкспериментальное значение постоянной Ридберга R: {R_experimental:.3f} эВ")
print(f"Теоретическое значение R: 13.606 эВ")

# =====================================================================
# 3. ПОСТРОЕНИЕ ГРАФИКОВ (ДВЕ РАЗНЫЕ ФИГУРЫ)
# =====================================================================

# --- График №1: Градуировка монохроматора ---
plt.figure(figsize=(8, 6))
drum_fine = np.linspace(calib_drum.min(), calib_drum.max(), 500)

plt.plot(drum_fine, calib_spline(drum_fine), 'g-', linewidth=2, label='Интерполяционный сплайн')
plt.scatter(neon_drum, w_to_E(neon_wl), color='orange', edgecolors='black', s=40, label='Реперы Неона (Ne)')
plt.scatter(mercury_drum, w_to_E(mercury_wl), color='blue', edgecolors='black', s=40, label='Реперы Ртути (Hg)')
plt.scatter(j_drum, j_energy, color='pink', edgecolors='black', s=100, label='Реперы йода')
plt.scatter(hydrogen_drum, hydrogen_energy, color='red', marker='X', s=100, zorder=5, label='Искомые линии Водорода (H)')

plt.xlabel('Деления отсчетного барабана')
plt.ylabel('Энергия E, эВ')
plt.title('График №1. Градуировочная кривая спектрометра УМ-2')
plt.minorticks_on()
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()

# --- График №2: Определение постоянной Ридберга через энергию ---
plt.figure(figsize=(8, 6))
plt.scatter(x_axis, hydrogen_energy, color='red', s=60, zorder=5, label='Экспериментальные уровни $E$')

# Отрисовка аппроксимирующей прямой по МНК
x_fine = np.linspace(x_axis.min() - 0.02, x_axis.max() + 0.02, 100)
plt.plot(x_fine, R_experimental * x_fine + intercept, 'b--', label=f'МНК-аппроксимация ($R_{{эксп}} = {R_experimental:.2f}$ эВ)')

plt.xlabel('Величина аргумента $-1/m^2$')
plt.ylabel('Энергия энергетического уровня $E$, эВ')
plt.title('График №2. Линеаризация уровней энергии для расчета постоянной Ридберга')
plt.minorticks_on()
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()

# Вывод обоих окон на экран
# plt.show()

# Оценка погрешности интерполяции сплайна (leave-one-out cross-validation)
errors = []
for i in range(len(calib_drum)):
    # Исключаем i-ю точку
    train_drum = np.delete(calib_drum, i)
    train_wl = np.delete(calib_wl, i)

    # Строим сплайн по оставшимся
    test_spline = CubicSpline(train_drum, train_wl, extrapolate=False)

    # Считаем разность в исключенной точке (если она не на самом краю)
    try:
        pred_wl = test_spline(calib_drum[i])
        if not np.isnan(pred_wl):
            errors.append(calib_wl[i] - pred_wl)
    except:
        pass

# Среднеквадратичная ошибка сплайна в нм
delta_spline_wl = np.sqrt(np.mean(np.square(errors)))
print(f"Погрешность интерполяции калибровочной кривой (сплайна): ±{delta_spline_wl:.3f} нм")


import scipy.stats as stats

# Количество точек (для водорода их 4: alpha, beta, gamma, delta)
N = len(x_axis)

# Считаем предсказанные моделью значения энергии фотонов
E_pred = R_experimental * x_axis + intercept

# Остаточная сумма квадратов (ошибки точек относительно прямой)
residuals = hydrogen_energy - E_pred
rss = np.sum(residuals**2)

# Дисперсия остатков (число степеней свободы N - 2, так как параметров два: R и intercept)
s_sq = rss / (N - 2)

# Сумма квадратов отклонений аргумента X от своего среднего значения
x_mean = np.mean(x_axis)
ss_x = np.sum((x_axis - x_mean)**2)

# Стандартная ошибка коэффициента наклона (постоянной Ридберга)
standard_error_R = np.sqrt(s_sq / ss_x)

# Вычисляем доверительный интервал (например, для доверительной вероятности 95%)
confidence_level = 0.95
alpha_level = 1 - confidence_level
# Квантиль распределения Стьюдента
t_stat = stats.t.ppf(1 - alpha_level/2, df=N-2)

# Итоговая абсолютная погрешность
delta_R = t_stat * standard_error_R

print(f"Постоянная Ридберга R = {R_experimental:.3f} ± {delta_R:.3f} эВ (при доверительной вероятности 95%)")
print(f"Относительная погрешность: E = {(delta_R / R_experimental)*100:.2f}%")


print(f" частоты I2 ")
print(*j_wl)
j_e2 = (j_energy[1]-j_energy[0])/5
print((j_energy[1]-j_energy[0])/5)

j_border_energy = calib_spline(1960)
print(f'граница {j_border_energy}')

E_el = j_energy[0] - 0.5*j_e2 + 0.5*0.027
print(f'энергия электронного перехода {E_el}')
print(f'D1 = {j_border_energy - 0.94}')
print(f'D2 = {j_border_energy - E_el}')

plt.plot(drum_fine, calib_spline(drum_fine), 'g-', linewidth=2, label='Интерполяционный сплайн')
plt.scatter(neon_drum, w_to_E(neon_wl), color='orange', edgecolors='black', s=10, label='Реперы Неона (Ne)')
plt.scatter(mercury_drum, w_to_E(mercury_wl), color='blue', edgecolors='black', s=10, label='Реперы Ртути (Hg)')
plt.scatter(j_drum, j_energy, color='pink', edgecolors='black', s=100, label='Реперы йода')

plt.xlabel('Деления отсчетного барабана')
plt.ylabel('Энергия E, эВ')
plt.title('График №3. Поглощение Йода')
plt.minorticks_on()
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()

# plt.show()