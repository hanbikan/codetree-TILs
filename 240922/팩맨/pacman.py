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

def get_max_eat_count(x,y,moved,eat_count):
    if moved == 3:
        return eat_count
    result = 0
    for k in range(4):
        nx, ny = x + dpx[k], y + dpy[k]
        if not in_range(nx,ny):
            continue
        next_eat_count = eat_count
        if not is_visited[nx][ny]:
            next_eat_count += len(get_monsters_at(nx,ny))
        is_visited[nx][ny] = True
        result = max(result, get_max_eat_count(nx,ny,moved+1,next_eat_count))
        is_visited[nx][ny] = False
    return result

def get_ate(x,y,moved,ate):
    global px, py
    for k in range(4):
        nx, ny = x + dpx[k], y + dpy[k]
        if not in_range(nx,ny):
            continue
        
        next_ate = ate.copy()
        if not is_visited[nx][ny]:
            next_ate += get_monsters_at(nx,ny)
        
        next_moved = moved + 1
        if next_moved == 3:
            if len(next_ate) == max_eat_count:
                px = nx
                py = ny
                return next_ate
        else:
            is_visited[nx][ny] = True
            res = get_ate(nx,ny,next_moved,next_ate)
            is_visited[nx][ny] = False
            if res != []:
                return res
    return []

def move_pacman():
    global px, py, max_eat_count, M, is_visited
    # get max eat count
    is_visited = [[False]*4 for _ in range(4)]
    max_eat_count = get_max_eat_count(px,py,0,0)

    # get highest priority moves
    is_visited = [[False]*4 for _ in range(4)]
    ate = get_ate(px,py,0,[])
    ate.sort(reverse=True)
    #print(max_eat_count, ate)

    for mi in ate:
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
    #print("pacman=",px, py)
    #print("monsters=", M, sorted(monsters))
    #print("bodies=",sorted(bodies))

print(len(monsters))