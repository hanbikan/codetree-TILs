d_pos = [
    [0,1],[1,0],[0,-1],[-1,0]
]

def select_to_move():
    # 현재까지의 총 점프 횟수가 적은 토끼
    candidates = []
    min_jump_count = float('inf')
    for pid, count in jump_count.items():
        if count < min_jump_count:
            min_jump_count = count
            candidates = [pid]
        elif count == min_jump_count:
            candidates.append(pid)
    if len(candidates) == 1:
        return candidates[0]
    
    # 현재 서있는 행 번호 + 열 번호가 작은 토끼
    next_candidates = []
    min_sum = float('inf')
    for pid in candidates:
        x, y = position[pid]
        if x + y < min_sum:
            min_sum = x + y
            next_candidates = [pid]
        elif x + y == min_sum:
            next_candidates.append(pid)
    candidates = next_candidates
    if len(candidates) == 1:
        return candidates[0]
    
    # 행 번호가 작은 토끼
    next_candidates = []
    min_x = float('inf')
    for pid in candidates:
        x, y = position[pid]
        if x < min_x:
            min_x = x
            next_candidates = [pid]
        elif x == min_x:
            next_candidates.append(pid)
    candidates = next_candidates
    if len(candidates) == 1:
        return candidates[0]
    
    # 열 번호가 작은 토끼
    next_candidates = []
    min_y = float('inf')
    for pid in candidates:
        x, y = position[pid]
        if y < min_y:
            min_y = y
            next_candidates = [pid]
        elif y == min_y:
            next_candidates.append(pid)
    candidates = next_candidates
    if len(candidates) == 1:
        return candidates[0]
    
    # 고유번호가 작은 토끼
    min_pid = float('inf')
    for pid in candidates:
        if pid < min_pid:
            min_pid = pid
    return min_pid

def in_range(x, y):
    return 0 <= x <= N - 1 and 0 <= y <= M - 1

# x, y 중 하나만 벗어났다고 가정
def get_out_position(x, y, d_index):
    if not (0 <= x <= N - 1):
        if x < 0:
            diff = -x
            if diff <= N - 1:
                return [diff % N, y]
            else:
                return [N - 1 - diff, y]
        else:
            diff = x - (N - 1)
            if diff <= N - 1:
                return [N - 1 - diff, y]
            else:
                return [diff % N, y]
    if not (0 <= y <= M - 1):
        if y < 0:
            diff = -y
            if diff <= M - 1:
                return [x, diff % M]
            else:
                return [x, M - 1 - diff]
        else:
            diff = y - (M - 1)
            if diff <= M - 1:
                return [x, M - 1 - diff]
            else:
                return [x, diff % M]

def get_next_positions(pid):
    result = []
    x, y = position[pid]
    d = dist[pid]
    for k in range(4):
        dx, dy = d_pos[k]
        nx, ny = x + (dx * d) % (N * 2 - 2), y + (dy * d) % (M * 2 - 2)
        if not in_range(nx, ny):
            nx, ny = get_out_position(nx, ny, k)
        result.append([nx, ny])
    return result

def select_position(positions):
    # 번호 + 열 번호가 큰 칸
    candidates = []
    max_sum = -1
    for x, y in positions:
        if x + y > max_sum:
            max_sum = x + y
            candidates = [[x,y]]
        elif x + y == max_sum:
            candidates.append([x,y])
    if len(candidates) == 1:
        return candidates[0]
    
    # 행 번호가 큰 칸
    next_candidates = []
    max_x = -1
    for x, y in candidates:
        if x > max_x:
            max_x = x
            next_candidates = [[x,y]]
        elif x == max_x:
            next_candidates.append([x,y])
    candidates = next_candidates
    if len(candidates) == 1:
        return candidates[0]

    # 열 번호가 큰 칸
    candidate = 0
    max_y = -1
    for x, y in candidates:
        if y > max_y:
            max_y = y
            candidate = [x,y]
    return candidate

def select_to_bonus(selected):
    # 현재 서있는 행 번호 + 열 번호가 큰 토끼
    candidates = []
    max_sum = -1
    for pid in selected:
        x, y = position[pid]
        if x + y > max_sum:
            max_sum = x + y
            candidates = [pid]
        elif x + y == max_sum:
            candidates.append(pid)
    if len(candidates) == 1:
        return candidates[0]
    
    # 행 번호가 큰 토끼
    next_candidates = []
    max_x = -1
    for pid in candidates:
        x, y = position[pid]
        if x > max_x:
            max_x = x
            candidates = [pid]
        elif x == max_x:
            candidates.append(pid)
    candidates = next_candidates
    if len(candidates) == 1:
        return candidates[0]
    
    # 열 번호가 큰 토끼
    next_candidates = []
    max_y = -1
    for pid in candidates:
        x, y = position[pid]
        if y > max_y:
            max_y = y
            candidates = [pid]
        elif x == max_y:
            candidates.append(pid)
    candidates = next_candidates
    if len(candidates) == 1:
        return candidates[0]
    
    # 고유번호가 큰 토끼
    max_pid = 0
    for pid in candidates:
        if pid > max_pid:
            max_pid = pid
    return max_pid

def play(): # K, S
    # K번 반복
    selected = set()
    for _ in range(K):
        # 이동
        pid_to_move = select_to_move()
        selected.add(pid_to_move)
        jump_count[pid_to_move] += 1
        next_positions = get_next_positions(pid_to_move)
        x, y = select_position(next_positions)
        position[pid_to_move] = [x,y]

        # 스코어 올리기
        to_add = x + y + 2
        for pid in score.keys():
            if pid == pid_to_move:
                continue
            score[pid] += to_add
        #print("position", position)
        #print("dist", dist)
        #print("score", score)
        #print("jump", jump_count)
        #print()
    # 우선순위 높은 토끼 +S(단, K번 반복하는 동안 1번이라도 뽑힌 적 있는 토끼여야 함)
    pid_for_bonus = select_to_bonus(selected)
    score[pid_for_bonus] += S


dist = {}
score = {}
jump_count = {}
position = {}

Q = int(input())
for t in range(1, Q + 1):
    order = list(map(int,input().split()))
    if order[0] == 100:
        # 경주 시작 준비
        N, M, P = order[1:4]
        for i in range(4, len(order), 2):
            pid, d = order[i:i+2]
            dist[pid] = d
            score[pid] = 0
            jump_count[pid] = 0
            position[pid] = [0,0]
    elif order[0] == 200:
        # 경주 진행
        K, S = order[1:3]
        play()
    elif order[0] == 300:
        # 이동거리 변경
        pid, L = order[1:3]
        dist[pid] *= L
    else:
        # 최고의 토끼 선정
        print(max(score.values()))