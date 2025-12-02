import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('flights.csv')
summary = df.groupby('CARGO').agg(
    flights_count=('CARGO', 'count'),
    total_price=('PRICE', 'sum'),
    total_weight=('WEIGHT', 'sum')
).reset_index()
print("Статистика по авиакомпаниям:")
print(summary)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
ax1.bar(summary['CARGO'], summary['flights_count'])
ax1.set_title('Количество рейсов по авиакомпаниям')
ax1.set_ylabel('Количество рейсов')
ax2.bar(summary['CARGO'], summary['total_price'])
ax2.set_title('Общая стоимость перевозок')
ax2.set_ylabel('Стоимость')
ax3.bar(summary['CARGO'], summary['total_weight'])
ax3.set_title('Общий вес перевезенных грузов')
ax3.set_ylabel('Вес')
plt.tight_layout()
plt.show()
