dx = [1,0,-1,0]
dy = [0,1,0,-1]

ddx = [-1,-1,1,1]
ddy = [-1,1,-1,1]

N,M,K,C = map(int,input().split()) # M년 / K 범위 대각선 / 제초제 C년 지속
mapp = [list(map(int,input().split())) for _ in range(N)]

def in_range(x,y):
    return 0 <= x < N and 0 <= y < N

def calc_kill_count(x,y):
    result = mapp[x][y]
    for k in range(4):
        for rep in range(1, K+1):
            nx, ny = x + ddx[k]*rep, y + ddy[k]*rep
            if not in_range(nx,ny):
                break
            if mapp[nx][ny] <= 0:
                break
            result += mapp[nx][ny]
    return result

def spray_herbicide(x,y):
    global killed
    killed += mapp[x][y]
    mapp[x][y] = 0
    herbicides[x][y] = C
    for k in range(4):
        for rep in range(1, K+1):
            nx, ny = x + ddx[k]*rep, y + ddy[k]*rep
            if not in_range(nx,ny):
                break
            herbicides[nx][ny] = C
            if mapp[nx][ny] <= 0:
                break
            killed += mapp[nx][ny]
            mapp[nx][ny] = 0

def print_all():
    print("TURN =", t)
    for i in range(N):
        print(*mapp[i])

killed = 0
EMPTY, WALL = 0, -1
herbicides = [[0]*N for _ in range(N)]
for t in range(M):
    # growth 1
    for i in range(N):
        for j in range(N):
            if mapp[i][j] >= 1:
                for k in range(4):
                    nx, ny = i+dx[k], j+dy[k]
                    if not in_range(nx,ny):
                        continue
                    if mapp[nx][ny] >= 1:
                        mapp[i][j] += 1

    # growth 2
    trees = []
    for i in range(N):
        for j in range(N):
            if mapp[i][j] >= 1:
                trees.append((i,j))
    
    to_add = [] # (x,y,add)
    for i, j in trees:
        count = 0
        for k in range(4):
            nx, ny = i+dx[k], j+dy[k]
            if not in_range(nx,ny):
                continue
            if mapp[nx][ny] == 0 and herbicides[nx][ny] == 0:
                count += 1
        for k in range(4):
            nx, ny = i+dx[k], j+dy[k]
            if not in_range(nx,ny):
                continue
            if mapp[nx][ny] == 0 and herbicides[nx][ny] == 0:
                to_add.append([nx, ny, mapp[i][j] // count])
    for x, y, add in to_add:
        mapp[x][y] += add

    # decrease herbicides
    for i in range(N):
        for j in range(N):
            herbicides[i][j] = max(0, herbicides[i][j] - 1)

    # kill trees
    max_kc = 0
    max_pos = (-1,-1)
    for i in range(N):
        for j in range(N):
            if mapp[i][j] >= 1:
                kc = calc_kill_count(i,j)
                if kc > max_kc:
                    max_kc = kc
                    max_pos = (i,j)
    if max_pos[0] != -1:
        spray_herbicide(max_pos[0], max_pos[1])
    #for h in herbicides:print(h)
    #print_all()

print(killed)