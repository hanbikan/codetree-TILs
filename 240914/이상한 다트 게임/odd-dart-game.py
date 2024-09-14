'''
1~n 원판에서 지워지는 수 없는 경우,
    원판에 남은 수가 하나라도 있는 경우,
        원판 전체 수 평균(소수점 floor)하여 정규화(평균보다 크면 -1 작으면 +1, 같으면 +0)
결과 = q번 회전 후 남아있는 수의 총합
'''

# [1,2,3,4] -> [4,1,2,3]
def rotate_clockwise(n, k):
    for _ in range(k):
        nums[n] = [nums[n][-1]] + nums[n][:-1]

def print_nums():
    for ns in nums:
        print(*ns)

CW, CCW = 0, 1 # d
REMOVED = float('inf')

# N=원판의 개수, M=원판 내 숫자 개수, Q=회전 횟수
N,M,Q = map(int,input().split())
nums = [[REMOVED]*M] + [list(map(int,input().split())) for _ in range(N)] + [[REMOVED]*M]
#print_nums()
for _ in range(Q):
    # x=원판 종류, d=방향(CW, CCW), k=회전 칸 수
    x,d,k = map(int,input().split())
    # 시계 방향 회전 기준으로 맞추기
    if d == CCW: # 반시계 기준 1 = 시계 3, 2 = 2, 3 = 1
        k = M - k
    # 회전
    for i in range(1, N + 1):
        if i % x == 0:
            rotate_clockwise(i, k)
    #print_nums()

    # 인접 찾기
    adj_pos = []
    for i in range(1, N+1):
        for j in range(M):
            cur = nums[i][j]
            if cur == REMOVED:
                continue
            if cur == nums[i-1][j] or cur == nums[i+1][j] or cur == nums[i][j-1] or cur == nums[i][(j+1)%M]:
                adj_pos.append((i,j))
    # 인접 지우기
    for i,j in adj_pos:
        nums[i][j] = REMOVED
    # (Optional) 정규화
    if len(adj_pos) == 0:
        survival_sum = 0
        survival_count = 0
        for i in range(1, N+1):
            for j in range(M):
                if nums[i][j] != REMOVED:
                    survival_sum += nums[i][j]
                    survival_count += 1
        if survival_count >= 1:
            survival_average = survival_sum // survival_count
            for i in range(1, N+1):
                for j in range(M):
                    cur = nums[i][j]
                    if cur == REMOVED:
                        continue
                    if cur > survival_average:
                        nums[i][j] -= 1
                    elif cur < survival_average:
                        nums[i][j] += 1
    #print(print_nums)

survival_sum = 0
for i in range(1, N+1):
    for j in range(M):
        if nums[i][j] != REMOVED:
            survival_sum += nums[i][j]
print(survival_sum)