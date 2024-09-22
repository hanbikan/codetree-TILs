dx = [-1,-1,0,1,1,1,0,-1]
dy = [0,-1,-1,-1,0,1,1,1]

dpx = [-1,0,1,0] # 상좌하우
dpy = [0,-1,0,1]

def in_range(x,y):
    return 0 <= x < 4 and 0 <= y < 4

def is_there_any_body(x,y):
    for bx,by,_ in bodies:
        if x == bx and y == by:
            return True
    return False

def move_monster(mi):
    x, y, d = monsters[mi]
    for k in range(8):
        cur_d = (d + k) % 8
        nx, ny = x + dx[cur_d], y + dy[cur_d]
        if not in_range(nx,ny):
            continue
        if is_there_any_body(nx,ny):
            continue
        if nx == px and ny == py:
            continue
        monsters[mi] = [nx,ny,cur_d]
        break

def get_monsters_at(x,y):
    res = []
    for i in range(len(monsters)):
        if x == monsters[i][0] and y == monsters[i][1]:
            res.append(i)
    return res

def set_max_ate(x,y,moved,ate):
    global px, py, max_ate
    for k in range(4):
        nx, ny = x + dpx[k], y + dpy[k]
        if not in_range(nx,ny):
            continue
        
        next_ate = ate.copy()
        if not is_visited[nx][ny]:
            next_ate += get_monsters_at(nx,ny)
        
        next_moved = moved + 1
        if next_moved == 3:
            if len(next_ate) > len(max_ate):
                max_ate = next_ate
                px = nx
                py = ny
        else:
            is_visited[nx][ny] = True
            set_max_ate(nx,ny,next_moved,next_ate)
            is_visited[nx][ny] = False

def move_pacman():
    global px, py, is_visited, max_ate
    # get highest priority moves
    is_visited = [[False]*4 for _ in range(4)]
    
    max_ate = []
    set_max_ate(px,py,0,[])

    max_ate.sort(reverse=True)
    #print(max_ate)

    for mi in max_ate:
        bodies.append([monsters[mi][0], monsters[mi][1], 3])
        monsters.pop(mi)

def remove_bodies():
    to_remove = []
    for i in range(len(bodies)):
        bodies[i][2] -= 1
        if bodies[i][2] == 0:
            to_remove.append(i)
    to_remove.sort(reverse=True)
    for i in to_remove:
        bodies.pop(i)

M, T = map(int,input().split())
px, py = map(int,input().split())
px -= 1
py -= 1

monsters = [] # x,y,d
for _ in range(M):
    x,y,d = map(int,input().split())
    x -= 1
    y -= 1
    d -= 1
    monsters.append([x,y,d])

bodies = [] # x,y,life(0 to removed)
for _ in range(T):
    #print("================================")
    eggs = monsters.copy()

    for i in range(len(monsters)):
        move_monster(i)
    #print("monsters=", M, monsters)
    
    move_pacman()
    remove_bodies()

    #print("monsters=", M, monsters)
    #print("bodies=", bodies)
    for egg in eggs:
        monsters.append(egg)
    #print("=================")
    #print("pacman=",px, py)
    #print("monsters=", M, sorted(monsters))
    #print("bodies=",sorted(bodies))

print(len(monsters))