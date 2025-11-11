import matplotlib.pyplot as plt

with open('frames.dat', 'r') as file:
    lines = file.read().strip().split('\n')
x_data = []
y_data = []

for i in range(0, len(lines), 2):
    x_line = lines[i].strip()
    y_line = lines[i + 1].strip()
    if x_line and y_line:
        x_data.append([float(num) for num in x_line.split()])
        y_data.append([float(num) for num in y_line.split()])
all_x = [x for frame in x_data for x in frame]
all_y = [y for frame in y_data for y in frame]
x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y)-0.5, max(all_y)+0.5

fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 12))
axes = axes.flatten()

for idx in range(6):
    axes[idx].plot(x_data[idx], y_data[idx])
    axes[idx].set_title(f'Frame {idx}')
    axes[idx].grid(True)
    axes[idx].set_xlim(x_min, x_max)
    axes[idx].set_ylim(y_min, y_max)

plt.tight_layout()
plt.show()