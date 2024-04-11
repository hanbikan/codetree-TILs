import sys, copy, math
input = sys.stdin.readline

P, E = -1, float('inf')

def get_next_position(px, py, ex, ey):
    dx, dy = int((ex - px) / abs(ex - px)) if ex - px != 0 else 0, int((ey - py) / abs(ey - py)) if ey - py != 0 else 0 

    if dx != 0 and 1 <= mapp[px + dx][py] <= 9:
        dx = 0
    if dy != 0 and 1 <= mapp[px][py + dy] <= 9:
        dy = 0
    
    if dx != 0 and dy != 0:
        return [px + dx, py]
    elif dx != 0:
        return [px + dx, py]
    elif dy != 0:
        return [px, py + dy]
    else:
        return [px, py]

def find_square_positions(player_positions, ex, ey):
    min_square_length = float('inf')

    for p in range(len(player_positions)):
        px, py = player_positions[p]
        square_length = max(abs(ex - px) + 1, abs(ey - py) + 1)
        
        if square_length < min_square_length:
            min_square_length = square_length
    
    for i in range(min_square_length):
        sx = max(0, ex - (min_square_length - 1)) + i
        for j in range(min_square_length):
            sy = max(0, ey - (min_square_length - 1)) + j
            for i2 in range(min_square_length):
                x = min(sx + i2, N - 1)
                for j2 in range(min_square_length):
                    y = min(sy + j2, N - 1)
                    if mapp[x][y] < 0:
                        return sx, sy, sx + min_square_length - 1, sy + min_square_length - 1

def rotate_map(start_x, start_y, end_x, end_y):
    if not (start_x < end_x and start_y < end_y):
        return
    
    length = end_x - start_x + 1

    routes = []
    for j in range(start_y, end_y + 1):
        routes.append([start_x, j])
    for i in range(start_x + 1, end_x + 1):
        routes.append([i, end_y])
    for j in range(end_y - 1, start_y - 1, -1):
        routes.append([end_x, j])
    for i in range(end_x - 1, start_x, -1):
        routes.append([i, start_y])
    
    tmps = []
    for i in range(start_x + 1, end_x + 1):
        tmps.append(mapp[i][start_y])
    for r in range(len(routes) - 1, -1 + length - 1, -1):
        x, y = routes[r]
        nx, ny = routes[r - (length - 1)]
        mapp[x][y] = mapp[nx][ny]
    for i in range(len(tmps)):
        mapp[start_x][end_y - i - 1] = tmps[i]
    
    rotate_map(start_x + 1, start_y + 1, end_x - 1, end_y - 1)

def print_status():
    for i in range(N):
        for j in range(N):
            if (mapp[i][j] < 0): print("P", end = " ")
            elif (mapp[i][j] == E): print("E", end = " ")
            else: print(mapp[i][j], end = " ")
        print()
    print()

def play():
    global player_positions

    move_count = 0
    
    for T in range(K):
        player_positions = []
        ex, ey = -1, -1

        for i in range(N):
            for j in range(N):
                if mapp[i][j] < 0:
                    player_positions.append([i, j])
                elif mapp[i][j] == E:
                    ex, ey = i, j
        
        # move
        to_remove = []
        for p in range(len(player_positions)):
            px, py = player_positions[p]
            nx, ny = get_next_position(px, py, ex, ey)
            player_positions[p] = [nx, ny]
            if px != nx or py != ny:
                move_count += abs(mapp[px][py])
                if mapp[nx][ny] == E:
                    to_remove.append(p)
                elif mapp[nx][ny] == P:
                    mapp[nx][ny] = mapp[px][py] - 1
                else:
                    mapp[nx][ny] = mapp[px][py]
                mapp[px][py] = 0
        
        for i in range(len(to_remove) - 1, -1, -1):
            player_positions.pop(to_remove[i])
        if len(player_positions) == 0:
            break
        
        # rotate
        sx1, sy1, sx2, sy2 = find_square_positions(player_positions, ex, ey)
        rotate_map(sx1, sy1, sx2, sy2)
        
        # decrease walls
        for i in range(sx1, sx2 + 1):
            for j in range(sy1, sy2 + 1):
                if 1 <= mapp[i][j] <= 9:
                    mapp[i][j] -= 1
    
    print(move_count)
    for i in range(N):
        for j in range(N):
            if mapp[i][j] == E:
                print(i + 1, j + 1)

# N: 미로 크기, M: 참가자 수, K: 게임 시간
N, M, K = map(int,input().split())
mapp = [list(map(int,input().split())) for _ in range(N)]

player_positions = [list(map(int,input().split())) for _ in range(M)]
for i in range(M):
    player_positions[i][0] -= 1
    player_positions[i][1] -= 1

for px, py in player_positions:
    mapp[px][py] = P

ex, ey = map(int,input().split())
ex -= 1
ey -= 1

mapp[ex][ey] = E

play()