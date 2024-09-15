dx = [0,1,0,-1]
dy = [1,0,-1,0]

ddx = [0,1,0,-1]
ddy = [-1,0,1,0]

def get_route_in_line(x,y,d,p):
    result = []
    cx, cy = x, y
    for _ in range(p):
        cx += ddx[d]
        cy += ddy[d]
        result.append((cx,cy))
    return result

def pp():
    print()
    for mp in mapp:
        print(mp)

N, M = map(int,input().split())
mapp = [list(map(int,input().split())) for _ in range(N)]
px, py = N//2, N//2

# init route
route = []
cx, cy = px, py
cd = 0
for p in range(1, N):
    for _ in range(2):
        route_in_line = get_route_in_line(cx, cy, cd, p)
        route += route_in_line
        cx, cy = route_in_line[-1]
        cd = (cd + 1) % 4
route += get_route_in_line(cx, cy, cd, N-1)
#print(route)
score = 0
for _ in range(M):
    D, P = map(int,input().split())

    #print("------------1------------")
    # 1. 공격
    for i in range(1, P + 1):
        x, y = px + dx[D]*i, py + dy[D]*i
        score += mapp[x][y]
        mapp[x][y] = 0
    #pp()
    #print("------------2------------")
    # 2. 채우기 + 지우기 반복
    while True:
        # 채우기
        new_nums = []
        for x, y in route:
            if mapp[x][y] != 0:
                new_nums.append(mapp[x][y])
        new_nums += [0]*(len(route) - len(new_nums))
        i = 0
        should_break = True
        for x, y in route:
            if mapp[x][y] != new_nums[i]:
                should_break = False
            mapp[x][y] = new_nums[i]
            i += 1
            if i >= len(new_nums):
                break
        if should_break:
            break
        #pp()
        # 지우기
        i = 0
        while i < len(route):
            xi, yi = route[i]
            j = i + 1
            while j < len(route):
                xj, yj = route[j]
                if mapp[xi][yi] != mapp[xj][yj]:
                    break
                j += 1
            if j - i >= 4:
                origin = mapp[xi][yi]
                j = i
                while j < len(route):
                    xj, yj = route[j]
                    if origin != mapp[xj][yj]:
                        break
                    score += origin
                    mapp[xj][yj] = 0
                    j += 1
            i = j
        #pp()
    #print("------------3------------")
    # 3. 짝 지어주기
    nums = []
    for x, y in route:
        if mapp[x][y] != 0:
            nums.append(mapp[x][y])
    i = 0
    new_nums = []
    while i < len(nums):
        ni = nums[i]
        j = i
        while j < len(nums):
            nj = nums[j]
            if ni != nj:
                break
            j += 1
        new_nums.append(j - i)
        new_nums.append(ni)
        i = j
    for i in range(N):
        for j in range(N):
            mapp[i][j] = 0
    i = 0
    for x, y in route:
        mapp[x][y] = new_nums[i]
        i += 1
        if i >= len(new_nums):
            break
    #pp()
print(score)