N, M = map(int, input().split())
field = []
for _ in range(M):
    field.append(list(map(int, input().split())))
K = int(input())
miners = []
for _ in range(K):
    x, y, d = map(int, input().split())
    miners.append((x, y, d))
otabotany = [[False for _ in range(N)] for _ in range(M)]
directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
              (1, 1), (1, -1), (-1, 1), (-1, -1)]
def in_bounds(x, y):
    return 0 <= x < N and 0 <= y < M
total = 0
for x, y, d in miners:
    for dx in range(-d, d+1):
        for dy in range(-d, d+1):
            if max(abs(dx), abs(dy)) <= d:
                nx, ny = x + dx, y + dy
                if in_bounds(nx, ny) and not otabotany[ny][nx]:
                    total += field[ny][nx]
                    otabotany[ny][nx] = True
print(total)