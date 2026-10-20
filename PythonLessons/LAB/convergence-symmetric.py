import pandas as pd
import matplotlib.pyplot as plt

# 1. Читаем данные
# Путь к файлу: рядом с бенчмарком или в build/ — проверьте, где у вас сохраняется
try:
    df = pd.read_csv('//home//kupalnic//4th_sem//System_of_linear_equations//theory//simmetric//convergence.csv')
except FileNotFoundError:
    print("Файл convergence.csv не найден! Сначала запустите C++ бенчмарк.")
    exit()

# Создаем два графика в одном окне
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Цвета для методов (обновлено под новые имена)
colors = {
    'Jacobi': '#e41a1c',  # красный
    'GaussSeidel': '#377eb8',  # синий
    'SymmetricGS': '#4daf4a',  # зелёный
    'SymmetricGS_Chebyshev': '#984ea3'  # фиолетовый (ускорение)
}

# Стили линий для лучшего различия при Ч/Б печати
linestyles = {
    'Jacobi': '-',
    'GaussSeidel': '--',
    'SymmetricGS': '-.',
    'SymmetricGS_Chebyshev': ':'
}

methods = df['Method'].unique()

for method in methods:
    data = df[df['Method'] == method]
    color = colors.get(method, 'black')
    linestyle = linestyles.get(method, '-')

    # График 1: Ошибка от номера итерации
    ax1.semilogy(data['Iteration'], data['Residual'],
                 label=method, color=color, linestyle=linestyle,
                 linewidth=2, marker='o', markevery=25, markersize=3)

    # График 2: Ошибка от времени (мс)
    ax2.semilogy(data['Time_ms'], data['Residual'],
                 label=method, color=color, linestyle=linestyle,
                 linewidth=2, marker='o', markevery=25, markersize=3)

# ==================== Настройка левого графика (Итерации) ====================
ax1.set_xlabel('Номер итерации', fontsize=11)
ax1.set_ylabel('Норма невязки $||Ax - b||_2$', fontsize=11)
ax1.set_title('Сходимость по итерациям', fontsize=13, fontweight='bold')
ax1.grid(True, which="both", ls="-", alpha=0.3)
ax1.legend(fontsize=9, frameon=True, shadow=False)
ax1.set_xlim(left=1)

# ==================== Настройка правого графика (Время) ====================
ax2.set_xlabel('Время (мс)', fontsize=11)
ax2.set_ylabel('Норма невязки $||Ax - b||_2$', fontsize=11)
ax2.set_title('Сходимость по времени', fontsize=13, fontweight='bold')
ax2.grid(True, which="both", ls="-", alpha=0.3)
ax2.legend(fontsize=9, frameon=True, shadow=False)
ax2.set_xlim(left=0)

# Общий заголовок и оформление
plt.suptitle('Сравнение методов решения СЛАУ', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()

# Сохранение в нескольких форматах
plt.savefig('convergence_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('convergence_comparison.pdf', bbox_inches='tight')  # для LaTeX/отчёта
print("Графики сохранены: convergence_comparison.png, convergence_comparison.pdf")

# ==================== Бонус: таблица с финальными метриками ====================
print("\n" + "=" * 60)
print("ФИНАЛЬНЫЕ МЕТРИКИ (последняя итерация)")
print("=" * 60)
summary = []
for method in methods:
    data = df[df['Method'] == method].iloc[-1]
    summary.append({
        'Method': method,
        'Final Iter': int(data['Iteration']),
        'Time (ms)': f"{data['Time_ms']:.2f}",
        'Residual': f"{data['Residual']:.2e}"
    })
summary_df = pd.DataFrame(summary)
print(summary_df.to_string(index=False))

# ==================== Бонус 2: оценка фактора ускорения ====================
print("\n" + "=" * 60)
print("ФАКТОР УСКОРЕНИЯ (относительно обычного Якоби)")
print("=" * 60)

jacobi_data = df[df['Method'] == 'Jacobi']
if jacobi_data.empty:
    print("Нет данных для метода Якоби — пропускаем сравнение")
else:
    jacobi_final = jacobi_data.iloc[-1]['Residual']
    jacobi_max_iter = jacobi_data['Iteration'].max()

    for method in methods:
        if method == 'Jacobi':
            continue
        data = df[df['Method'] == method]
        if data.empty:
            continue

        # Находим итерацию, где метод достиг невязки <= финальной невязки Якоби
        faster = data[data['Residual'] <= jacobi_final].iloc[0:1]
        if not faster.empty:
            print(f"{method:25s}: достиг точности Якоби за {int(faster.iloc[0]['Iteration']):3d} итераций "
                  f"(Якоби: {jacobi_final:.2e} → {method}: {faster.iloc[0]['Residual']:.2e})")
        else:
            # Используем максимальную итерацию из данных этого метода
            max_iter_method = int(data['Iteration'].max())
            final_residual = data.iloc[-1]['Residual']
            print(f"{method:25s}: не достиг точности Якоби за {max_iter_method} итераций "
                  f"(финальная невязка: {final_residual:.2e})")