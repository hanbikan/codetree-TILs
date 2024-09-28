'''
> 술래
n*n 격자 정중앙(n은 홀수)

> 도망자 = m명
상하: 하
좌우: 우

> 나무 = h개
최초에 도망자와 중첩 가능

> k턴
move runners
    술래와 거리 3 이하일 때만 움직임(|x1-x2| + |y1-y2|)
    if next position not in range?
        방향 바꿈
    next position에 술래 없는 경우에 이동(나무 노상관)
move catcher
    move
    다음에 방향을 틀어야 하는 경우((0,0), 정중앙도 포함)
        방향 전환
    3칸 체크
        나무와 함께 있는 도망자는 못 잡음
        도망자 사라짐
        점수 획득(t번째 턴, t * 잡은 도망자 수)

> 주요 포인트
- runners iteration: runners = [(1,2), ...]
- catcher route: 좌표 기준
- catcher direction: dx, dy를 다음 위치 - 현재 위치로 구하기
- check trees: trees set -> runner가 빠르게 체크
'''

def init_catcher_route(N):
    dx = [-1,0,1,0]
    dy = [0,1,0,-1]

    x,y = N // 2, N // 2
    d = 0
    route = [(x,y)]
    for move in range(1, N):
        for _ in range(2):
            for _ in range(move):
                x += dx[d]
                y += dy[d]
                route.append((x,y))
            d = (d + 1) % 4
    for _ in range(move):
        x += dx[d]
        y += dy[d]
        route.append((x,y))
    route = route + route[::-1][1:-1]
    return route

def in_range(x,y):
    return 0 <= x < N and 0 <= y < N

rdx = [0,1,0,-1]
rdy = [1,0,-1,0]

N,M,H,K = map(int,input().split())
catcher_route = init_catcher_route(N)
catcher_ri = 0 # catcher's route index
runners = []
for _ in range(M):
    X,Y,D = map(int,input().split())
    X -= 1
    Y -= 1
    D -= 1
    runners.append([X,Y,D])
trees = set()
for _ in range(H):
    X,Y = map(int,input().split())
    X -= 1
    Y -= 1
    trees.add((X,Y))

def calc_dist_to_catcher(x,y):
    cx, cy = catcher_route[catcher_ri]
    return abs(cx-x) + abs(cy-y)

def get_catcher_pos():
    return catcher_route[catcher_ri]

def get_catcher_d():
    cx, cy = catcher_route[catcher_ri]
    ncx, ncy = catcher_route[(catcher_ri + 1) % len(catcher_route)]
    return (ncx - cx, ncy - cy)

def print_all():
    cx, cy = get_catcher_pos()
    print("TURN=", t, "SCORE=", score)
    print("catcher=", cx, cy, "dir=", get_catcher_d())
    print("trees=", trees)
    print("runners=")
    rds = [">", "v", "<", "ㅅ"]
    for i in range(len(runners)):
        rx,ry,rd = runners[i]
        print("runner=", rx, ry, rds[rd])
    print("===========================")

score = 0
for t in range(1, K+1):
    cx, cy = get_catcher_pos()
    # move runners
    for i in range(len(runners)):
        rx, ry, rd = runners[i]
        dist_to_catcher = calc_dist_to_catcher(rx,ry)
        if dist_to_catcher > 3:
            continue
        nrx, nry = rx + rdx[rd], ry + rdy[rd]
        if not in_range(nrx, nry):
            runners[i][2] = (rd + 2) % 4
            rd = runners[i][2]
            nrx, nry = rx + rdx[rd], ry + rdy[rd]
        if nrx == cx and nry == cy:
            continue
        runners[i][0] = nrx
        runners[i][1] = nry

    # move catcher
    catcher_ri = (catcher_ri + 1) % len(catcher_route)
    cx, cy = get_catcher_pos()
    #print_all()

    # catch
    cdx, cdy = get_catcher_d()
    cur_cx, cur_cy = cx, cy
    for _ in range(3):
        removal_runner_indexes = set()
        for i in range(len(runners)):
            rx, ry, _ = runners[i]
            if (runners[i][0], runners[i][1]) in trees:
                continue
            if rx == cur_cx and ry == cur_cy:
                removal_runner_indexes.add(i)
                score += t
        
        new_runners = []
        for i in range(len(runners)):
            if not i in removal_runner_indexes:
                new_runners.append(runners[i])
        runners = new_runners

        cur_cx += cdx
        cur_cy += cdy
        if not in_range(cur_cx, cur_cy):
            break
    #print_all()

print(score)