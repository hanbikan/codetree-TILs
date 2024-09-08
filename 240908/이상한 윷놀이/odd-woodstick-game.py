dx = [0,0,-1,1] # R L T B
dy = [1,-1,0,0]
X,Y,D = 0,1,2
W,R,B = 0,1,2

def in_range(x,y):
    return 0 <= x < N and 0 <= y < N

def switch(d):
    if d % 2 == 0:
        return d + 1
    else:
        return d - 1

def move(index):
    x,y,d = xyd[index]
    nx,ny = x+dx[d], y+dy[d]
    
    # xyd
    ci = stack[x][y].index(index)
    for i in stack[x][y][ci:]:
        xyd[i][X] = nx
        xyd[i][Y] = ny

    # stack
    if color[nx][ny] == R:
        stack[nx][ny] = stack[nx][ny] + stack[x][y][ci:][::-1]
    else:
        stack[nx][ny] = stack[nx][ny] + stack[x][y][ci:]
    stack[x][y] = stack[x][y][:ci]

def get_game_turn():
    for turn in range(1, 1000 + 1):
        for i in range(K):
            x,y,d = xyd[i]
            # move
            nx, ny = x+dx[d], y+dy[d]
            if not in_range(nx,ny) or color[nx][ny] == B:
                xyd[i][D] = switch(d)
                d = xyd[i][D]
                nx, ny = x+dx[d], y+dy[d]
                if in_range(nx,ny) and color[nx][ny] != B:
                    move(i)
            else:
                move(i)
            # check 4 stacks
            for i in range(K):
                x,y,d = xyd[i]
                if len(stack[x][y]) >= 4:
                    return turn

    return -1

N, K = map(int,input().split())
color = [list(map(int,input().split())) for _ in range(N)]
stack = [[[] for _ in range(N)] for _ in range(N)]
xyd = []
for i in range(K):
    x,y,d = map(int,input().split())
    x -= 1
    y -= 1
    d -= 1
    xyd.append([x,y,d])
    stack[x][y].append(i)

print(get_game_turn())