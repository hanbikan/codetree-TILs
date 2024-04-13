X, Y, H, W, HP = 0, 1, 2, 3, 4
EMPTY, TRAP, WALL = 0, 1, 2

d_pos = [
    [-1,0],[0,1],[1,0],[0,-1]
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

def move(knight_index, dir_index):
    to_move = set()
    x, y, h, w, hp = knights[knight_index]
    dx, dy = d_pos[dir_index]

    # 밀리는 기사 찾기
    for i in range(h):
        for j in range(w):
            nx, ny = x + i + dx, y + j + dy
            cur = knight_map[nx][ny]
            if not in_range(nx, ny) or mapp[nx][ny] == WALL:
                return False
            if cur != 0 and cur != knight_index:
                to_move.add(knight_map[nx][ny])
    
    for next_knight_index in to_move:
        if move(next_knight_index, dir_index) == False:
            return False
    
    # 업데이트
    knights[knight_index][X] = x + dx
    knights[knight_index][Y] = y + dy
    init_knight_map()

    return to_move

def update_hp(knight_index):
    x, y, h, w, hp = knights[knight_index]
    for i in range(h):
        for j in range(w):
            if mapp[x + i][y + j] == TRAP:
                knights[knight_index][HP] -= 1
                if knights[knight_index][HP] == 0:
                    init_knight_map()

def print_status():
    print("KNIGHT_MAP")
    for i in range(L):
        print(*knight_map[i])
    print("HP")
    for i in range(1, N + 1):
        print(i, " = ", knights[i][HP])

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

    res = move(i, d)
    if res != False:
        for knight_index in res:
            update_hp(knight_index)

result = 0
for k in range(1, N + 1):
    if knights[k][HP] == 0:
        continue
    result += original_hp[k] - knights[k][HP]
print(result)