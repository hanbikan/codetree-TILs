dx = [-1,-1,0,1,1,1,0,-1]
dy = [0,-1,-1,-1,0,1,1,1]

dpx = [-1,0,1,0] # 상좌하우
dpy = [0,-1,0,1]

def in_range(x,y):
    return 0 <= x < 4 and 0 <= y < 4

def move_monsters():
    global monsters
    new_monsters = [[[0]*8 for _ in range(4)] for _ in range(4)]
    for x in range(4):
        for y in range(4):
            for k in range(8):
                if monsters[x][y][k] == 0:
                    continue
                moved = False
                for add_k in range(8):
                    cur_k = (k + add_k) % 8
                    nx, ny = x + dx[cur_k], y + dy[cur_k]
                    if not in_range(nx,ny):
                        continue
                    if bodies[nx][ny] > 0:
                        continue
                    if nx == px and ny == py:
                        continue
                    new_monsters[nx][ny][cur_k] += monsters[x][y][k]
                    #print(x,y,k,nx,ny,cur_k)
                    moved = True
                    break
                if not moved:
                    new_monsters[x][y][k] += monsters[x][y][k]
    monsters = new_monsters

def set_max_ate(x,y,moved,ate,ate_count):
    global px, py, max_ate, max_ate_count
    for k in range(4):
        nx, ny = x + dpx[k], y + dpy[k]
        if not in_range(nx,ny):
            continue
        
        next_ate = ate.copy()
        next_ate_count = ate_count
        if not is_visited[nx][ny]:
            for k2 in range(8):
                if monsters[nx][ny][k2] == 0:
                    continue
                next_ate.append([nx,ny,k2,monsters[nx][ny][k2]])
                next_ate_count += monsters[nx][ny][k2]
        
        next_moved = moved + 1
        if next_moved == 3:
            if next_ate_count > max_ate_count:
                max_ate_count = next_ate_count
                max_ate = next_ate
                px = nx
                py = ny
        else:
            is_visited[nx][ny] = True
            set_max_ate(nx,ny,next_moved,next_ate,next_ate_count)
            is_visited[nx][ny] = False

def move_pacman():
    global px, py, is_visited, max_ate, max_ate_count, monsters

    is_visited = [[False]*4 for _ in range(4)]
    max_ate = [] # x,y,dir,cnt
    max_ate_count = -1
    set_max_ate(px,py,0,[],0)

    for x,y,_,_ in max_ate:
        bodies[x][y] = 3
        for k in range(8):
            monsters[x][y][k] = 0

def remove_bodies():
    global bodies

    for i in range(4):
        for j in range(4):
            bodies[i][j] = max(0, bodies[i][j] - 1)

M, T = map(int,input().split())
px, py = map(int,input().split())
px -= 1
py -= 1

monsters = [[[0]*8 for _ in range(4)] for _ in range(4)]
for i in range(M):
    x,y,d = map(int,input().split())
    x -= 1
    y -= 1
    d -= 1
    monsters[x][y][d] += 1

bodies = [[0]*4 for _ in range(4)] # x,y,life(0 to removed)
for _ in range(T):
    eggs = monsters.copy()
    move_monsters()
    #print("======================")
    #for i in range(4):
    #    for j in range(4):
    #        print(monsters[i][j], end=" ")
    #    print()
    
    move_pacman()
    #print("PAC", px, py)
    remove_bodies()
    #print("BODIES", bodies)

    for i in range(4):
        for j in range(4):
            for k in range(8):
                monsters[i][j][k] += eggs[i][j][k]
    #        print(monsters[i][j], end=" ")
    #    print()
    #print(px,py)

summ = 0
for i in range(4):
    for j in range(4):
        for k in range(8):
            summ += monsters[i][j][k]
print(summ)