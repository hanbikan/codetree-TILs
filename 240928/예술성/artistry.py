dx = [0,1,0,-1]
dy = [1,0,-1,0]

def in_range(x,y):
    return 0 <= x < N and 0 <= y < N

def set_group_positions(x, y):
    positions.add((x,y))
    for k in range(4):
        nx,ny = x + dx[k], y + dy[k]
        if not in_range(nx,ny):
            continue
        if mapp[x][y] != mapp[nx][ny]:
            continue
        if visited[nx][ny]:
            continue
        visited[nx][ny] = True
        set_group_positions(nx,ny)

def dfs(x,y):
    for k in range(4):
        nx,ny = x + dx[k], y + dy[k]
        if not in_range(nx,ny):
            continue
        g1, g2 = group_map[x][y], group_map[nx][ny]
        if g1 != g2:
            if g1 < g2:
                adjs[g1][g2] += 1
            continue
        if visited[nx][ny]:
            continue
        visited[nx][ny] = True
        dfs(nx,ny)


def get_score():
    # find groups & save positions
    global visited, positions, group_map, score, adjs
    visited = [[False]*N for _ in range(N)]
    group_positions = []
    group_map = [[-1]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if visited[i][j]:
                continue
            visited[i][j] = True
            positions = set()
            set_group_positions(i,j)
            group_positions.append(positions)

            for x,y in positions:
                group_map[x][y] = len(group_positions) - 1
    
    visited = [[False]*N for _ in range(N)]
    g_len = len(group_positions)
    adjs = [[0]*g_len for _ in range(g_len)]
    for g in range(g_len):
        positions = group_positions[g]
        for x, y in positions:
            visited[x][y] = True
            dfs(x,y)
            break

    score = 0
    for i in range(g_len):
        for j in range(g_len):
            if adjs[i][j] != 0:
                for x,y in group_positions[i]:
                    i_sx, i_sy = x,y
                    break
                for x,y in group_positions[j]:
                    j_sx, j_sy = x,y
                    break
                score += (len(group_positions[i]) + len(group_positions[j])) * mapp[i_sx][i_sy] * mapp[j_sx][j_sy] * adjs[i][j]
    return score

def rotate_mapp_clockwise(sx, sy, length, rep):
    new_mapp = []
    for i in range(N):
        new_mapp.append(mapp[i].copy())

    to_rotate = []
    for i in range(length):
        lst = []
        for j in range(length):
            lst.append(new_mapp[sx + i][sy + j])
        to_rotate.append(lst)
    
    for _ in range(rep):
        to_rotate = [zp[::-1] for zp in zip(*to_rotate)]
        for i in range(length):
            for j in range(length):
                new_mapp[sx + i][sy + j] = to_rotate[i][j]

    return new_mapp

def rotate():
    mapp_for_cross = rotate_mapp_clockwise(0,0,len(mapp),3)
    for i in range(N):
        mapp[i][N//2] = mapp_for_cross[i][N//2]
    for j in range(N):
        mapp[N//2][j] = mapp_for_cross[N//2][j]
    for i in range(2):
        for j in range(2):
            sx = i * (N // 2 + 1)
            sy = j * (N // 2 + 1)
            mapp_for_square = rotate_mapp_clockwise(sx,sy,N//2,1)
            for k in range(N//2):
                for l in range(N//2):
                    x = sx + k
                    y = sy + l
                    mapp[x][y] = mapp_for_square[x][y]

N = int(input())
mapp = [list(map(int,input().split())) for _ in range(N)]

score_sum = 0
for _ in range(4):
    score_sum += get_score()
    rotate()
print(score_sum)