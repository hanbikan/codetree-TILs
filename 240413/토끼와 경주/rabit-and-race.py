import heapq

class Rabbit:
    def __init__(self, x, y, jump, pid):
        self.x = x
        self.y = y
        self.jump = jump
        self.pid = pid
    
    def __lt__(self, other):
        if self.jump != other.jump:
            return self.jump < other.jump
        if self.x + self.y != other.x + other.y: 
            return self.x + self.y < other.x + other.y
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        return self.pid < other.pid

d_pos = [
    [0,1],[1,0],[0,-1],[-1,0]
]

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

def get_next_positions(rabbit):
    result = []
    x, y = rabbit.x, rabbit.y
    d = dist[rabbit.pid]
    for k in range(4):
        dx, dy = d_pos[k]
        nx, ny = x + dx * d[0], y + dy * d[1]
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

def compare(r1, r2):
    if r1.x + r1.y != r2.x + r2.y:
        return r1.x + r1.y > r2.x + r2.y
    if r1.x != r2.x:
        return r1.x > r2.x
    if r1.y != r2.y:
        return r1.y > r2.y
    return r1.pid > r2.pid

def play(): # 2000
    global score_to_add
    # K번 반복
    selected = []
    for _ in range(K): # 100
        # 이동
        rabbit_to_move = heapq.heappop(rabbits)
        pid_to_move = rabbit_to_move.pid
        heapq.heappush(selected, rabbit_to_move)
        rabbit_to_move.jump += 1
    
        next_positions = get_next_positions(rabbit_to_move) # 4
        x, y = select_position(next_positions)
        rabbit_to_move.x = x
        rabbit_to_move.y = y
        heapq.heappush(rabbits, rabbit_to_move)

        # 스코어 올리기
        to_add = x + y + 2
        score_to_add += to_add
        score[pid_to_move] -= to_add
        #print("position", position)
        #print("dist", dist)
        #print("score", score)
        #print("jump", jump_count)
        #print()
    # 우선순위 높은 토끼 +S(단, K번 반복하는 동안 1번이라도 뽑힌 적 있는 토끼여야 함)
    bonus_rabbit = Rabbit(0, 0, 0, 0)
    while selected:
        cur = heapq.heappop(selected)
        if compare(cur, bonus_rabbit):
            bonus_rabbit = cur
    score[bonus_rabbit.pid] += S


dist = {}
score = {}
rabbits = []
score_to_add = 0

Q = int(input())
for t in range(1, Q + 1):
    order = list(map(int,input().split()))
    if order[0] == 100:
        # 경주 시작 준비
        N, M, P = order[1], order[2], order[3]
        for i in range(4, len(order), 2):
            pid, d = order[i], order[i + 1]
            dist[pid] = [d % (N * 2 - 2), d % (M * 2 - 2)]
            score[pid] = 0
            heapq.heappush(rabbits, Rabbit(0, 0, 0, pid))
    elif order[0] == 200:
        # 경주 진행
        K, S = order[1], order[2]
        play()
    elif order[0] == 300:
        # 이동거리 변경
        pid, L = order[1], order[2]
        dist[pid][0] = (dist[pid][0] * L) % (N * 2 - 2)
        dist[pid][1] = (dist[pid][1] * L) % (M * 2 - 2)
    else:
        # 최고의 토끼 선정
        print(max(score.values()) + score_to_add)