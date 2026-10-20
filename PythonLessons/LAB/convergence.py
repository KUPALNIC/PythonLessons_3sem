import pandas as pd
import matplotlib.pyplot as plt

# 1. Читаем данные
try:
    # Путь лучше оставить относительным для переносимости, либо проверь свой абсолютный
    df = pd.read_csv('//home//kupalnic//4th_sem//System_of_linear_equations//build//convergence.csv')
except FileNotFoundError:
    print("Файл convergence.csv не найден! Сначала запусти C++ бенчмарк.")
    exit()

# Создаем два графика в одном окне
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Обновленный список цветов с учетом Чебышёва
colors = {
    'GaussSeidel': 'blue',
    'Jacobi': 'red',
    'SimpleIteration': 'green',
    'Chebyshev': 'orange'  # Выделим ускорение ярким цветом
}

methods = df['Method'].unique()

for method in methods:
    data = df[df['Method'] == method]
    color = colors.get(method, 'black') # черный, если метод не в словаре

    # График 1: Ошибка от номера итерации
    ax1.plot(data['Iteration'], data['Residual'],
             label=method, color=color, linewidth=2)

    # График 2: Ошибка от времени (мс)
    ax2.plot(data['Time_ms'], data['Residual'],
             label=method, color=color, linewidth=2)

# Настройка левого графика (Итерации)
ax1.set_yscale('log')
ax1.set_xlabel('Номер итерации')
ax1.set_ylabel('Норма невязки ||Ax - b||')
ax1.set_title('Сходимость по итерациям')
ax1.grid(True, which="both", ls="-", alpha=0.3)
ax1.legend()

# Настройка правого графика (Время)
ax2.set_yscale('log')
ax2.set_xlabel('Время (мс)')
ax2.set_ylabel('Норма невязки ||Ax - b||')
ax2.set_title('Сходимость по времени')

# Ограничение по времени (убрал жесткое 55, чтобы видеть всю картину,
# либо адаптируй под свои замеры)
plt.xlim(0, 100)

ax2.grid(True, which="both", ls="-", alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('convergence_comparison.png', dpi=300)
plt.show()
