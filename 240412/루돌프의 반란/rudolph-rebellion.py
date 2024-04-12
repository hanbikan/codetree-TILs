EMPTY, RUDOLF = 0, -1

d_pos = [
    [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]
]

def in_range(x, y):
    return 0 <= x <= N - 1 and 0 <= y <= N - 1

def get_nearest_santa():
    min_distance = float('inf')
    min_p = 0
    for p, (sx, sy) in s_pos.items():
        dist = pow(sx - rx, 2) + pow(sy - ry, 2)
        if dist < min_distance:
            min_distance = dist
            min_p = p
        elif dist == min_distance:
            if s_pos[min_p][0] < sx or (s_pos[min_p][0] == sx and s_pos[min_p][1] < sy):
                min_p = p

    return min_p

def move_rudolf(target_p):
    global rx, ry

    # 갈 방향 정하기
    tx, ty = s_pos[target_p]
    min_distance = float('inf')
    min_dx, min_dy = [0, 0]
    for dx, dy in d_pos:
        nrx, nry = rx + dx, ry + dy
        if not in_range(nrx, nry):
            continue
        distance = pow(tx - nrx, 2) + pow(ty - nry, 2)
        if distance < min_distance:
            min_distance = distance
            min_dx, min_dy = dx, dy

    # 이동
    nsx, nsy = tx + min_dx * C, ty + min_dy * C # 산타가 튕겨나간 위치

    # 루돌프 이동
    mapp[rx][ry] = EMPTY
    rx, ry = rx + min_dx, ry + min_dy
    has_collision = mapp[rx][ry] >= 1
    mapp[rx][ry] = RUDOLF

    # 산타 이동 + 상호작용
    if has_collision:
        offset = 0
        to_move = []
        while True:
            cur_x, cur_y = nsx + min_dx * offset, nsy + min_dy * offset
            if not in_range(cur_x, cur_y):
                break
            if mapp[cur_x][cur_y] >= 1: # 산타가 있음
                to_move.append(mapp[cur_x][cur_y])
                offset += 1
            else:
                break

        # 뒤에 있는 산타부터 이동
        for i in range(len(to_move) - 1, -1, -1):
            p_to_move = to_move[i]
            px, py = s_pos[p_to_move]
            pnx, pny = px + min_dx, py + min_dy
            if not in_range(pnx, pny):
                s_pos.pop(p_to_move)
            else:
                mapp[pnx][pny] = mapp[px][py]
                s_pos[p_to_move] = [pnx, pny]

        if not in_range(nsx, nsy):
            s_pos.pop(target_p)
        else:
            mapp[nsx][nsy] = target_p
            s_pos[target_p] = [nsx, nsy]

        status[target_p] = 2  # 기절
        scores[target_p] += C # 점수

def get_next_santa_pos(sx, sy):
    min_distance = pow(sx - rx, 2) + pow(sy - ry, 2)
    min_x, min_y = sx, sy
    for k in range(0, 8, 2):
        dx, dy = d_pos[k]
        nsx, nsy = sx + dx, sy + dy
        if not in_range(nsx, nsy):
            continue
        if mapp[nsx][nsy] >= 1:
            continue
        distance = pow(rx - nsx, 2) + pow(ry - nsy, 2)
        if distance < min_distance:
            min_distance = distance
            min_x, min_y = nsx, nsy

    return [min_x, min_y]

def move_santas():
    p_to_remove = []
    for p, (sx, sy) in s_pos.items():
        if status[p] != 0:
            continue
        nsx, nsy = get_next_santa_pos(sx, sy)
        if nsx == sx and nsy == sy:
            continue
        dx, dy = nsx - sx, nsy - sy
        rdx, rdy = -dx, -dy

        if mapp[nsx][nsy] == RUDOLF:
            # 산타 밀려남
            csx, csy = sx + rdx * (D - 1), sy + rdy * (D - 1)
            if not (csx == sx and csy == sy):
                offset = 0
                to_move = []
                while True:
                    cur_x, cur_y = csx + rdx * offset, csy + rdy * offset
                    if not in_range(cur_x, cur_y):
                        break
                    if mapp[cur_x][cur_y] >= 1:
                        to_move.append(mapp[cur_x][cur_y])
                        offset += 1
                    else:
                        break

                # 뒤에 있는 산타부터 이동
                for i in range(len(to_move) - 1, -1, -1):
                    p_to_move = to_move[i]
                    px, py = s_pos[p_to_move]
                    pnx, pny = px + rdx, py + rdy
                    if not in_range(pnx, pny):
                        p_to_remove.append(p_to_move)
                    else:
                        mapp[pnx][pny] = mapp[px][py]
                        s_pos[p_to_move] = [pnx, pny]

            if not in_range(csx, csy):
                mapp[sx][sy] = EMPTY
                p_to_remove.append(p)
            else:
                mapp[sx][sy] = EMPTY
                mapp[csx][csy] = p
                s_pos[p] = [csx, csy]

            status[p] = 2 # 기절
            scores[p] += D # 점수
        else:
            mapp[sx][sy] = EMPTY
            mapp[nsx][nsy] = p
            s_pos[p] = [nsx, nsy]

    for p in p_to_remove:
        s_pos.pop(p)


'''
5 7 4 2 2
3 2
1 1 3
2 3 5
3 5 1
4 4 4

5 7 3 1 1
3 2
1 3 3
2 3 4
3 3 5
'''

def print_status():
    print("RUDOLF: ", rx, ry)
    print("SANTAS: ", s_pos)
    print("STATUS: ", status)
    print("SCORES: ", scores)
    for i in range(N):
        for j in range(N):
            if mapp[i][j] == EMPTY:
                print('#', end=' ')
            elif mapp[i][j] == RUDOLF:
                print('R', end=' ')
            else:
                print(mapp[i][j], end=" ")
        print()
    print()

def play():
    for _ in range(M):
        # 루돌프 이동
        target_p = get_nearest_santa()
        move_rudolf(target_p)

        # 산타 이동
        move_santas()

        if len(s_pos) == 0:
            break

        for p in s_pos.keys():
            scores[p] += 1 # 살아있는 산타 점수 추가
            status[p] = max(0, status[p] - 1) # 상태 변경

    to_print = [0] * P
    for p, score in scores.items():
        to_print[p - 1] = score

    print(*to_print)

if __name__ == '__main__':
    # N: 게임판 크기, M: 턴 수, P: 산타 수, C: 루돌프 힘, D: 산타 힘
    N, M, P, C, D = map(int, input().split())
    mapp = [[EMPTY] * N for _ in range(N)]
    rx, ry = map(int, input().split())
    rx -= 1
    ry -= 1
    mapp[rx][ry] = RUDOLF
    s_pos = {}
    scores = {}
    status = {} # 2(기절한 턴) -> 1(기절 다음 턴) -> 0
    for i in range(P):
        p, x, y = map(int, input().split())
        x -= 1
        y -= 1
        s_pos[p] = [x, y]
        scores[p] = 0
        status[p] = 0
        mapp[x][y] = p

    play()