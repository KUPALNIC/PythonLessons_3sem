import matplotlib.pyplot as plt
import numpy as np
print("Задаем N")
N=int(input())
x=0

summ=[]
y=np.sign(x)
for x in np.arange(-np.pi, np.pi+0.01, 0.01):
    for k in range(1,N+1):
        sum1+=np.sin((2*k+1)*x)/(2*k+1)
    sum1=sum1*(4/np.pi)
    summ.append(sum1)
    sum1=0
x=np.arange(-np.pi, np.pi+0.01, 0.01)
print(summ)
plt.plot(x, sum)
plt.show()
