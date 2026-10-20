import numpy as np
import matplotlib.pyplot as plt

# Настройка шрифтов для ГОСТ-дизайна
plt.rcParams.update({'font.size': 11, 'font.family': 'serif'})


def calc_array_factor(theta, N, d_over_lambda, theta_scan_deg=0.0):
    k = 2 * np.pi
    d = d_over_lambda
    theta_0 = np.radians(theta_scan_deg)
    delta_phi = k * d * np.sin(theta_0)
    Psi = k * d * np.sin(theta) - delta_phi

    eps = 1e-10
    numerator = np.sin(N * Psi / 2)
    denominator = np.sin(Psi / 2) + eps
    intensity = (numerator / denominator) ** 2 / (N ** 2)
    return intensity


def find_beamwidth(theta, intensity):
    max_idx = np.argmax(intensity)
    half_power = 0.5
    left_idx = max_idx
    while left_idx > 0 and intensity[left_idx] > half_power:
        left_idx -= 1
    right_idx = max_idx
    while right_idx < len(intensity) - 1 and intensity[right_idx] > half_power:
        right_idx += 1
    return np.degrees(theta[right_idx] - theta[left_idx])


# Сетка углов
theta_deg = np.linspace(-90, 90, 2000)
theta_rad = np.radians(theta_deg)

# ==============================================================================
# РИСУНОК 1а. Зависимость ДН от шага (Декартовы координаты, ЧБ)
# ==============================================================================
plt.figure(figsize=(7, 5))
D = 23.5

# Случай 1: N=12 (d = 2.14) - Сплошная тонкая серая линия
d_1 = D / (12 - 1)
I_1 = 10 * np.log10(calc_array_factor(theta_rad, 12, d_1, 0) + 1e-4)
plt.plot(theta_deg, I_1, color='gray', linestyle='-', linewidth=1.2, label='N=12 (d = 2.14$\\lambda$)')

# Случай 2: N=16 (d = 1.57) - Штриховая чёрная линия
d_2 = D / (16 - 1)
I_2 = 10 * np.log10(calc_array_factor(theta_rad, 16, d_2, 0) + 1e-4)
plt.plot(theta_deg, I_2, color='black', linestyle='--', linewidth=1.5, label='N=16 (d = 1.57$\\lambda$)')

# Случай 3: N=25 (d = 0.98) - Сплошная толстая чёрная линия
d_3 = D / (25 - 1)
I_3 = 10 * np.log10(calc_array_factor(theta_rad, 25, d_3, 0) + 1e-4)
plt.plot(theta_deg, I_3, color='black', linestyle='-', linewidth=2.0, label='N=25 (d = 0.98$\\lambda$)')

plt.axhline(-3, color='black', linestyle=':', alpha=0.7, label='Уровень -3 дБ')
plt.xlabel('Угол наблюдения $\\theta$, градусы')
plt.ylabel('Интенсивность, дБ')
plt.ylim(-40, 2)
plt.grid(True, linestyle=':')
plt.legend(loc='lower center')
plt.tight_layout()
plt.savefig('plot_1a_rect.png', dpi=300)  # Сохраняем в файл
plt.show()

# ==============================================================================
# РИСУНОК 1б. Зависимость ДН от шага (Полярные координаты, ЧБ)
# ==============================================================================
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
# Переводим в линейный масштаб (по полю, т.е. корень из интенсивности), так как в дБ полярный график не нагляден
ax.plot(theta_rad, np.sqrt(calc_array_factor(theta_rad, 12, d_1, 0)), color='gray', linestyle='-',
        label='N=12 (d = 2.14$\\lambda$)')
ax.plot(theta_rad, np.sqrt(calc_array_factor(theta_rad, 16, d_2, 0)), color='black', linestyle='--',
        label='N=16 (d = 1.57$\\lambda$)')
ax.plot(theta_rad, np.sqrt(calc_array_factor(theta_rad, 25, d_3, 0)), color='black', linestyle='-', linewidth=1.8,
        label='N=25 (d = 0.98$\\lambda$)')

ax.set_theta_zero_location('N')  # Нормаль к решётке смотрит вверх
ax.set_theta_direction(-1)  # Углы по часовой стрелке
ax.set_thetalim(-np.pi / 2, np.pi / 2)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15))
plt.tight_layout()
plt.savefig('plot_1b_polar.png', dpi=300)
plt.show()

# ==============================================================================
# РИСУНОК 2. Электронное сканирование (Идеальный шаг d = 0.5)
# ==============================================================================
plt.figure(figsize=(7, 5))
N_scan = 16
d_scan = 0.5
angles = [0, 30, 60]
styles = ['-', '--', ':']
widths = [2.0, 1.5, 1.2]
colors = ['black', 'black', 'gray']

for ang, style, w, col in zip(angles, styles, widths, colors):
    I = calc_array_factor(theta_rad, N_scan, d_scan, theta_scan_deg=ang)
    I_db = 10 * np.log10(I + 1e-4)
    w_deg = find_beamwidth(theta_rad, I)
    plt.plot(theta_deg, I_db, color=col, linestyle=style, linewidth=w,
             label=f'$\\theta_0 = {ang}^\\circ$ (Ширина: {w_deg:.1f}$^\\circ$)')


plt.xlabel('Угол наблюдения $\\theta$, градусы')
plt.ylabel('Интенсивность, дБ')
plt.ylim(-30, 2)
plt.grid(True, linestyle=':')
plt.legend()
plt.tight_layout()
plt.savefig('plot_2_scan.png', dpi=300)
plt.show()

# ==============================================================================
# РИСУНОК 3. Критическая ситуация: Возникновение паразита ПРИ сканировании
# ==============================================================================
plt.figure(figsize=(7, 5))
N_danger = 12
d_danger = 0.75

I_str = 10 * np.log10(calc_array_factor(theta_rad, N_danger, d_danger, 0) + 1e-4)
I_tilt = 10 * np.log10(calc_array_factor(theta_rad, N_danger, d_danger, 35) + 1e-4)

plt.plot(theta_deg, I_str, color='gray', linestyle='--', linewidth=1.5, label='Прямой луч ($\\theta_0 = 0^\\circ$)')
plt.plot(theta_deg, I_tilt, color='black', linestyle='-', linewidth=2.0,
         label='Сканирование на $\\theta_0 = 35^\\circ$')


plt.xlabel('Угол наблюдения $\\theta$, градусы')
plt.ylabel('Интенсивность, дБ')
plt.ylim(-30, 2)
plt.grid(True, linestyle=':')
plt.legend()
plt.tight_layout()
plt.savefig('plot_3_danger.png', dpi=300)
plt.show()
