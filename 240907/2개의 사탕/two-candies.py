dx = [1,-1,0,0] # down up right left
dy = [0,0,1,-1]

DOWN,UP,RIGHT,LEFT=0,1,2,3
X,Y=0,1

def forward(d, p):
    x, y = p
    while mapp[x + dx[d]][y + dy[d]] != '#' and (x + dx[d],y + dy[d]) != b and (x + dx[d],y + dy[d]) != r:
        x += dx[d]
        y += dy[d]
    if (x,y) == o:
        return (-1,-1)
    return (x,y)

def tilt(d):
    global r, b
    if d == DOWN:
        if r[X] > b[X]:
            r = forward(d, r)
            b = forward(d, b)
        else:
            b = forward(d, b)
            r = forward(d, r)
    elif d == UP:
        if r[X] < b[X]:
            r = forward(d, r)
            b = forward(d, b)
        else:
            b = forward(d, b)
            r = forward(d, r)
    elif d == RIGHT:
        if r[Y] > b[Y]:
            r = forward(d, r)
            b = forward(d, b)
        else:
            b = forward(d, b)
            r = forward(d, r)
    else:
        if r[Y] < b[Y]:
            r = forward(d, r)
            b = forward(d, b)
        else:
            b = forward(d, b)
            r = forward(d, r)

    return r == (-1,-1) and b != (-1,-1)

def f(depth):
    if depth > 10:
        return float('inf')

    global b, r
    result = float('inf')
    for k in range(4):
        pb, pr = b, r
        #print(depth, k, r, b)
        if tilt(k):
            #print("!", depth, k, r, b)
            b, r = pb, pr
            return depth
        if pb == b and pr == r:
            continue
        result = min(result, f(depth + 1))
        b, r = pb, pr
    return result

N, M = map(int,input().split())
mapp = [str(input().rstrip()) for _ in range(N)]

for i in range(N):
    for j in range(M):
        if mapp[i][j] == 'B':
            b = (i,j)
        elif mapp[i][j] == 'R':
            r = (i,j)
        elif mapp[i][j] == 'O':
            o = (i,j)

result = f(1)
if result == float('inf'):
    print(-1)
else:
    print(result)