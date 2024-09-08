dx = [-1,1,1,-1]
dy = [1,1,-1,-1]

X,Y = 0,1

def in_range(x,y):
    return 0 <= x < N and 0 <= y < N

def get_diagonal_sum(x,y,k,points):
    result = 0
    left,top,right,bottom = points
    cx, cy = x, y
    while in_range(cx, cy):
        result += mapp[cx][cy]
        cx += dx[k]
        cy += dy[k]
        if k == 0 and cy > top[Y]:
            break
        elif k == 1 and cx > right[X]:
            break
        elif k == 2 and cy < bottom[Y]:
            break
        elif k == 3 and cx < left[X]:
            break

    return result

def get_diff(top_x,top_y,l,r):
    sums = []
    #print("get_diff", top_x,top_y,l,r)
    
    top = top_x,top_y
    left = top_x+l,top_y-l
    bottom = top_x+l+r,top_y-l+r
    right = top_x+r,top_y+r

    points = [left,top,right,bottom]
    #print(points)
    pdx = [0,-1,0,1] # l t r b
    pdy = [-1,0,1,0]
    for k in range(4):
        cur_sum = 0
        x, y = points[k]
        x += pdx[(k+1)%4]
        y += pdy[(k+1)%4]
        # left 기준 왼쪽 이동(한 칸 남김)
        #print("start", x, y, k)
        while in_range(x + pdx[k], y + pdy[k]):
            cur_sum += get_diagonal_sum(x,y,k,points)
            #print("[1]", x,y, get_diagonal_sum(x,y,k,points))
            x += pdx[k]
            y += pdy[k]
        # left 기준 위로 이동
        while in_range(x, y):
            cur_sum += get_diagonal_sum(x,y,k,points)
            #print("[2]", x,y, get_diagonal_sum(x,y,k,points))
            x += pdx[(k+1)%4]
            y += pdy[(k+1)%4]
        #print("end", cur_sum)
        sums.append(cur_sum)
    
    sums.append(total_sum - sum(sums))
    return max(sums) - min(sums)

N = int(input())
mapp = [list(map(int,input().split())) for _ in range(N)]

total_sum = 0
for i in range(N):
    total_sum += sum(mapp[i])

#get_diff(0,2,2,1)

min_diff = float('inf')
for i in range(N-2):
    for j in range(1, N-1):
        l = 1
        while j - l >= 0:
            r = 1
            while j + r <= N - 1 and i + l + r <= N - 1:
                min_diff = min(min_diff, get_diff(i,j,l,r))
                r += 1
            l += 1
print(min_diff)