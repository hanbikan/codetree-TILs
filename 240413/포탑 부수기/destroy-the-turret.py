import heapq

d_pos_4 = [
    [0,1],[1,0],[0,-1],[-1,0]
]

d_pos_8 = [
    [0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]
]

def in_range(x, y):
    return 0 <= x <= N - 1 and 0 <= y <= M - 1

def select_attacker():
    # 공격력이 가장 낮은 포탑
    candidates = []
    min_attack = float('inf')
    for i in range(N):
        for j in range(M):
            if mapp[i][j] == 0: continue

            if mapp[i][j] < min_attack:
                min_attack = mapp[i][j]
                candidates = [[i,j]]
            elif mapp[i][j] == min_attack:
                candidates.append([i,j])

    if len(candidates) == 1:
        return candidates[0]

    # 가장 최근에 공격한 포탑
    next_candidates = []
    recent = -1
    for x, y in candidates:
        if attacked_at[x][y] > recent:
            recent = attacked_at[x][y]
            next_candidates = [[x,y]]
        elif attacked_at[x][y] == recent:
            next_candidates.append([x,y])
    candidates = next_candidates

    if len(candidates) == 1:
        return candidates[0]
    
    # 행과 열의 합이 가장 큰 포탑
    next_candidates = []
    summ = -1
    for x, y in candidates:
        if x + y > summ:
            summ = x + y
            next_candidates = [[x,y]]
        elif x + y == summ:
            next_candidates.append([x,y])
    candidates = next_candidates

    if len(candidates) == 1:
        return candidates[0]

    # 열 값이 가장 큰 포탑
    candidate = None
    max_y = -1
    for x, y in candidates:
        if y > max_y:
            max_y = y
            candidate = [x,y]
    
    return candidate

def select_target(attacker):
    # 공격력이 가장 높은 포탑
    candidates = []
    max_attack = -1
    for i in range(N):
        for j in range(M):
            if mapp[i][j] == 0: continue
            if i == attacker[0] and j == attacker[1]: continue

            if mapp[i][j] > max_attack:
                max_attack = mapp[i][j]
                candidates = [[i,j]]
            elif mapp[i][j] == max_attack:
                candidates.append([i,j])

    if len(candidates) == 1:
        return candidates[0]

    # 공격한 지 가장 오래된 포탑
    next_candidates = []
    oldest = float('inf')
    for x, y in candidates:
        if attacked_at[x][y] < oldest:
            oldest = attacked_at[x][y]
            next_candidates = [[x,y]]
        elif attacked_at[x][y] == oldest:
            next_candidates.append([x,y])
    candidates = next_candidates

    if len(candidates) == 1:
        return candidates[0]
    
    # 행과 열의 합이 가장 작은 포탑
    next_candidates = []
    summ = float('inf')
    for x, y in candidates:
        if x + y < summ:
            summ = x + y
            next_candidates = [[x,y]]
        elif x + y == summ:
            next_candidates.append([x,y])
    candidates = next_candidates

    if len(candidates) == 1:
        return candidates[0]

    # 열 값이 가장 작은 포탑
    candidate = None
    min_y = float('inf')
    for x, y in candidates:
        if y < min_y:
            min_y = y
            candidate = [x,y]
    
    return candidate

def attack(target, damage):
    mapp[target[0]][target[1]] = max(0, mapp[target[0]][target[1]] - damage)
    not_attacked.discard(target[0]*M + target[1])

def attack_raiser(attacker, target):
    # dijkstra
    distances = [[float('inf')]*M for _ in range(N)]
    distances[attacker[0]][attacker[1]] = 0

    q = [[0, attacker, []]] # dist, node, route
    heapq.heapify(q)

    while len(q) > 0:
        cur_dist, cur_pos, cur_route = heapq.heappop(q)
        for dx, dy in d_pos_4:
            nx, ny = cur_pos[0] + dx, cur_pos[1] + dy
            if not in_range(nx, ny):
                nx, ny = (nx + N) % N, (ny + M) % M
            if mapp[nx][ny] == 0:
                continue
            if [nx, ny] == target:
                # 포탑 공격
                damage = mapp[attacker[0]][attacker[1]]
                attack(target, damage)
                for p in cur_route:
                    attack(p, damage // 2)
                return True
        
            if cur_dist + 1 < distances[nx][ny]:
                heapq.heappush(q, [cur_dist + 1, [nx, ny], cur_route + [[nx,ny]]])
                distances[nx][ny] = cur_dist + 1
    
    return False

def attack_fire(attacker, target):
    damage = mapp[attacker[0]][attacker[1]]
    attack(target, damage)
    # 주위 공격
    for dx, dy in d_pos_8:
        nx, ny = target[0] + dx, target[1] + dy
        if not in_range(nx, ny):
            nx, ny = (nx + N) % N, (ny + M) % M
        if mapp[nx][ny] == 0:
            continue
        attack([nx, ny], damage // 2)

def print_status():
    print(attacker, target)
    for i in range(N):
        print(*mapp[i])
    print()

N, M, K = map(int,input().split())
mapp = [list(map(int,input().split())) for _ in range(N)]
attacked_at = [[0] * M for _ in range(N)]

for t in range(1, K + 1):
    # 공격자 선정
    attacker = select_attacker()
    mapp[attacker[0]][attacker[1]] += N + M
    attacked_at[attacker[0]][attacker[1]] = t

    # 타겟 선정
    target = select_target(attacker)

    # 공격
    not_attacked = set()
    for i in range(N):
        for j in range(M):
            if mapp[i][j] == 0: continue
            not_attacked.add(i*M + j)
    
    # 레이저 공격
    if not attack_raiser(attacker, target):
        # 포탄 공격
        attack_fire(attacker, target)
    
    # 부서지지 않은 포탑 1개가 되면 종료
    zero_count = 0
    for i in range(N):
        for j in range(M):
            if mapp[i][j] == 0:
                zero_count += 1
    if zero_count == N * M - 1:
        break

    # 정비(공격과 부관한 포탑 +1)
    for p in not_attacked:
        if p == attacker[0]*N + attacker[1]:
            continue
        x, y = p // M, p % M
        mapp[x][y] += 1

    #print_status()

# 가장 강한 포탑 공격력 출력
maxx = -1
for i in range(N):
    for j in range(M):
        maxx = max(maxx, mapp[i][j])
print(maxx)