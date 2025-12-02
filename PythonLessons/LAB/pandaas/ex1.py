import pandas as pd

#=================task1==================
df=pd.read_csv('transactions.csv')
df=df[df['STATUS'] == 'OK'].sort_values('SUM')
print('='*70, '\n', 'Top 3 max finished contracts:', '\n', df.loc[:,  ['CONTRACTOR', 'SUM']][-3:])
print('='*70)
#=================task2==================
print(f'Sum of all contracrs: {df[df['CONTRACTOR'] == 'Umbrella, Inc']['SUM'].sum()}')
print('='*70)

