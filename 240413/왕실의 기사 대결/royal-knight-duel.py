X, Y, H, W, HP = 0, 1, 2, 3, 4
EMPTY, TRAP, WALL = 0, 1, 2

d_pos = [
    [-1,0],[0,1],[1,0],[0,-1] # 상 우 하 좌
]

def in_range(x, y):
    return 0 <= x <= L - 1 and 0 <= y <= L - 1

def init_knight_map():
    global knight_map
    knight_map = [[EMPTY] * L for _ in range(L)]
    for k in range(1, N + 1):
        x, y, h, w, hp = knights[k]
        
        if hp == 0:
            continue

        for i in range(h):
            for j in range(w):
                knight_map[x + i][y + j] = k

def move(knight_index, dir_index, start_knight_index):
    to_move = set()
    x, y, h, w, hp = knights[knight_index]
    dx, dy = d_pos[dir_index]

    # 밀리는 기사 찾기
    for i in range(h):
        for j in range(w):
            nx, ny = x + i + dx, y + j + dy
            if not in_range(nx, ny) or mapp[nx][ny] == WALL:
                return False
            cur = knight_map[nx][ny]
            if cur != 0 and cur != knight_index: # 다른 기사가 있음
                to_move.add(cur)
    
    # 재귀: 한 번이라도 실패 시 아무것도 안 함
    for next_knight_index in to_move:
        res = move(next_knight_index, dir_index, start_knight_index)
        if res == False:
            return False
    
    # 업데이트
    knights[knight_index][X] = x + dx
    knights[knight_index][Y] = y + dy
    init_knight_map()
    if knight_index != start_knight_index:
        update_hp(knight_index, dir_index)

    return True

def update_hp(knight_index, dir_index):
    x, y, h, w, hp = knights[knight_index]
    if hp == 0:
        return
    if dir_index == 0: # 상
        for j in range(w):
            if mapp[x][y + j] == TRAP:
                knights[knight_index][HP] -= 1
                if knights[knight_index][HP] == 0:
                    init_knight_map()
                    return
    if dir_index == 1: # 우
        for i in range(h):
            if mapp[x + i][y + w - 1] == TRAP:
                knights[knight_index][HP] -= 1
                if knights[knight_index][HP] == 0:
                    init_knight_map()
                    return
    if dir_index == 2: # 하
        for j in range(w):
            if mapp[x + h - 1][y + j] == TRAP:
                knights[knight_index][HP] -= 1
                if knights[knight_index][HP] == 0:
                    init_knight_map()
                    return
    if dir_index == 3: # 좌
        for i in range(h):
            if mapp[x + i][y] == TRAP:
                knights[knight_index][HP] -= 1
                if knights[knight_index][HP] == 0:
                    init_knight_map()
                    return

def print_status():
    print("KNIGHT_MAP")
    for i in range(L):
        print(*knight_map[i])
    #print("HP")
    #for i in range(1, N + 1):
    #    print(i, "=", knights[i][HP], "(", knights[i][HP] - original_hp[i], ")")

# L: 체스판 크기, N: 기사 수, Q: 명령 수
L, N, Q = map(int,input().split())
mapp = [list(map(int,input().split())) for _ in range(L)]
knights = [[]]
knight_map = []
original_hp = [0]
for k in range(N):
    x, y, h, w, hp = map(int,input().split())
    knights.append([x - 1, y - 1, h, w, hp])
    original_hp.append(hp)
init_knight_map()

for t in range(Q):
    i, d = map(int,input().split())
    x, y, h, w, hp = knights[i]

    if hp == 0:
        continue

    move(i, d, i)

result = 0
for k in range(1, N + 1):
    if knights[k][HP] == 0:
        continue
    result += original_hp[k] - knights[k][HP]
print(result)