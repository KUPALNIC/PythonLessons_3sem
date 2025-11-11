import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('students.csv', sep=';', names=['prep', 'group', 'grade'])
grades = list(range(3, 11))
by_prep = data.groupby(['prep', 'grade']).size().unstack(fill_value=0)
by_prep = by_prep[grades]

by_group = data.groupby(['group', 'grade']).size().unstack(fill_value=0)
by_group = by_group[grades]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

by_prep.plot(kind='bar', stacked=True, ax=ax1)
ax1.set_title('По преподавателям')
ax1.set_xlabel('Преподаватель')
ax1.set_ylabel('Кол-во студентов')
ax1.legend(title='Оценка',  bbox_to_anchor=(1.02, 1), loc='upper left')
ax1.tick_params(axis='x', rotation=45)

by_group.plot(kind='bar', stacked=True, ax=ax2)
ax2.set_title('По группам')
ax2.set_xlabel('Группа')
ax2.set_ylabel('Кол-во студентов')
ax2.legend(title='Оценка',  bbox_to_anchor=(1.02, 1), loc='upper left')
ax2.tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.show()