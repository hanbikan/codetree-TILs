dx = [0,-1,-1,-1,0,1,1,1]
dy = [1,1,0,-1,-1,-1,0,1]

dix = [-1,-1,1,1]
diy = [1,-1,-1,1]

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

N, M = map(int,input().split())
H = [list(map(int,input().split())) for _ in range(N)]

sups = [(N-2,0),(N-2,1),(N-1,0),(N-1,1)]
for _ in range(M):
    D, P = map(int,input().split())
    D -= 1
    cdx, cdy = (dx[D]*P + N*3) % N, (dy[D]*P + N*3) % N # make it positive
    
    # move
    for i in range(len(sups)):
        sups[i] = (sups[i][0] + cdx) % N, (sups[i][1] + cdy) % N
    # apply
    to_add = []
    for x, y in sups:
        H[x][y] += 1
    for x, y in sups:
        for k in range(4):
            nx, ny = x+dix[k], y+diy[k]
            if not in_range(nx, ny):
                continue
            if H[nx][ny] >= 1:
                H[x][y] += 1

    # add sups
    new_sups = []
    for i in range(N):
        for j in range(N):
            if (i,j) in sups:
                continue
            if H[i][j] >= 2:
                H[i][j] -= 2
                new_sups.append((i,j))
    sups = new_sups

result = 0
for i in range(N):
    for j in range(N):
        result += H[i][j]
print(result)