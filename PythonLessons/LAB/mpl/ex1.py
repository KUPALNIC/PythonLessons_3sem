import matplotlib.pyplot as plt
with open('005.dat', 'r') as file:
    n = int(file.readline())
    x=[]
    y=[]
    for i in range(n):
        cordinate = file.readline().split('\n')
        cordinate = cordinate[0].split(' ')
        x.append(float(cordinate[0]))
        y.append(float(cordinate[1]))

plt.scatter(x, y)
# print(*x, '\n', *y)
plt.xlim(min(x)-1, max(x)+1)
plt.ylim(min(y)-1, max(y)+1)
plt.title(f'Number of points: {len(x)}')
plt.gca().set_aspect('equal')
plt.show()

