import matplotlib.pyplot as plt
import pandas as pd

df_students = pd.read_excel('students_info.xlsx', dtype=str)
res = pd.read_html('results_ejudge.html')
result = res[0]
result.rename(columns={'User': 'login'}, inplace=True)
merged = pd.merge(df_students, result, on='login', how='left')
fac_av = merged.groupby('group_faculty')['Solved'].mean()
fac_av.plot(kind='bar')
plt.xlabel('facultet group')
plt.ylabel('Average solved tasks')
plt.title('Solved task (facultet)')
plt.show()

group_mean = merged.groupby('group_out')['Solved'].mean()
group_mean.plot(kind='bar')
plt.xlabel('Computer science group')
plt.ylabel('Average solved tasks')
plt.title('Solved task')
plt.show()

G= merged['G']>=10
H = merged['H']>= 10
mask = (G | H)
sdali = merged[mask]
print("\n", "="*70, "\n",
      f"Всего студентов, прошедших тест G или H: {len(sdali)}",
      "\n", "="*70, "\n",
      f"По группам факультета: {sdali['group_faculty'].value_counts()}",
      "\n", "=" * 70, "\n",
      f"По группам информатики: {sdali['group_out'].value_counts()}")