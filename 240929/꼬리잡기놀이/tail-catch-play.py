EMPTY, HEAD, HUMAN, TAIL, LINE = 0,1,2,3,4
dx = [0,-1,0,1]
dy = [1,0,-1,0]

N,M,K = map(int,input().split())
mapp = [list(map(int,input().split())) for _ in range(N)]

sx = [0,N-1,N-1,0]
sy = [0,0,N-1,N-1]

def is_human(x,y):
    return 1 <= mapp[x][y] <= 3

def in_range(x,y):
    return 0 <= x < N and 0 <= y < N

def get_adjacent_line_pos(x,y):
    for k in range(4):
        nx, ny = x + dx[k], y + dy[k]
        if in_range(nx,ny) and mapp[nx][ny] == LINE:
            return (nx,ny)

# starting from head
def get_positions(x,y):
    if not is_human(x,y):
        return []
    
    res = [(x,y)]
    for k in range(4):
        nx, ny = x + dx[k], y + dy[k]
        if not in_range(nx,ny):
            continue
        if not is_human(nx,ny):
            continue
        if visited[nx][ny]:
            continue
        visited[nx][ny] = True
        res += get_positions(nx,ny)
        visited[nx][ny] = False
    return res

def get_first_hit_position(r):
    d = (r // N) % 4
    x, y = sx[d], sy[d]
    for _ in range(r % N):
        x += dx[(d + 3) % 4]
        y += dy[(d + 3) % 4]
    for offset in range(N):
        if is_human(x,y):
            return (x,y)
        x += dx[d]
        y += dy[d]
    return -1, -1

def get_head_pos(x,y):
    if mapp[x][y] == HEAD:
        return (x,y)
    for k in range(4):
        nx, ny = x + dx[k], y + dy[k]
        if not in_range(nx,ny):
            continue
        if not is_human(nx,ny):
            continue
        if visited[nx][ny]:
            continue
        visited[nx][ny] = True
        res = get_head_pos(nx,ny)
        visited[nx][ny] = False
        if res != False:
            return res
    return False

score = 0
visited = [[False]*N for _ in range(N)]
for r in range(K):
    # move
    head_positions = []
    for i in range(N):
        for j in range(N):
            if mapp[i][j] == HEAD:
                head_positions.append((i,j))
    for i, j in head_positions:
        visited[i][j] = True
        positions = get_positions(i,j)
        visited[i][j] = False
        next_head_pos = get_adjacent_line_pos(i,j)
        new_positions = [next_head_pos] + positions[:-1]
        
        for x, y in positions:
            mapp[x][y] = LINE
        for x, y in new_positions:
            mapp[x][y] = HUMAN
        mapp[new_positions[0][0]][new_positions[0][1]] = HEAD
        mapp[new_positions[-1][0]][new_positions[-1][1]] = TAIL

    # add score
    hx, hy = get_first_hit_position(r)
    if hx != -1:
        visited[hx][hy] = True
        head_x, head_y = get_head_pos(hx, hy)
        visited[hx][hy] = False

        visited[head_x][head_y] = True
        positions = get_positions(head_x, head_y)
        visited[head_x][head_y] = False
        score += (positions.index((hx, hy)) + 1) ** 2

        # turn around
        mapp[positions[0][0]][positions[0][1]] = TAIL
        mapp[positions[-1][0]][positions[-1][1]] = HEAD
print(score)