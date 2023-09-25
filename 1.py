counts = [[0, 14], [24, 0], [0, 0], [0, 0], [0, 8], [0, 2], [0, 21], [6, 0], [18, 0]]
s = [[37, 0]]
f = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def dfs(x):
    print(x)
    for i in s:
        print(i[0], i[1], sep=" ")
    if x == 10:
        for i in s:
            print(2)
            print(i[0], i[1])
            return
    for j in counts:
        print(s[x-1][1])
        if s[x - 1][1] == 0:
            if j[0] == 0 and f[counts.index(j)] == 0:
                s.append(j)
                f[counts.index(j)] = 1
                dfs(x + 1)
                f[counts.index(j)] = 0
        else:
            if j[0] != 0 and f[counts.index(j)] == 0 and 26 <= j[0] + s[x - 1][1] <= 28:
                s.append(j)
                f[counts.index(j)] = 1
                dfs(x + 1)
                f[counts.index(j)] = 0


dfs(1)

final = [4, 5, 10, 3, 6, 1, 8, 9, 2, 0, 7]
