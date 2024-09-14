'''
4^10 = 1048576
'''

def init_graph():
    graph = {} # 0: [[1], 2] ... 0(2점) -> 1
    for i in range(21):
        graph[i] = [[i+1], i*2]
    graph[21] = [[], 0] # 도착
    next_node = 22

    # A bridge 5 to node 20
    graph[5][NEXT_NODES].append(next_node)
    for i in range(3):
        graph[next_node] = [[next_node+1], graph[5][SCORE] + (i+1)*3]
        next_node += 1
    graph[next_node] = [[next_node+1], 25]
    next_node += 1
    graph[next_node] = [[next_node+1], 30]
    next_node += 1
    graph[next_node] = [[20], 35]
    next_node += 1

    # A bridge 10 to node 25
    graph[10][NEXT_NODES].append(next_node)
    graph[next_node] = [[next_node+1], 22]
    next_node += 1
    graph[next_node] = [[25], 24]
    next_node += 1

    # A bridge 15 to node 25
    graph[15][NEXT_NODES].append(next_node)
    graph[next_node] = [[next_node+1], 28]
    next_node += 1
    graph[next_node] = [[next_node+1], 27]
    next_node += 1
    graph[next_node] = [[25], 26]
    next_node += 1
    return graph

def try_move_and_get_node(start_node, rep):
    cur_node = start_node
    for i in range(rep):
        if i == 0 and len(graph[cur_node][NEXT_NODES]) == 2:
            cur_node = graph[cur_node][NEXT_NODES][1]
        elif len(graph[cur_node][NEXT_NODES]) == 0:
            break
        else:
            cur_node = graph[cur_node][NEXT_NODES][0]
    return cur_node
    

def dfs(move_index, score):
    if move_index >= 10:
        global max_score
        max_score = max(max_score, score)
        return
    for i in range(4):
        next_node = try_move_and_get_node(cur_nodes[i], moves[move_index])
        # next_node에 말이 있는지 체크
        if cur_nodes.count(next_node) >= 1:
            continue
        back = cur_nodes[i]
        cur_nodes[i] = next_node
        dfs(move_index + 1, score + graph[next_node][SCORE])
        cur_nodes[i] = back


NEXT_NODES, SCORE = 0, 1
moves = list(map(int,input().split()))
graph = init_graph()

cur_nodes = [0]*4
max_score = 0
dfs(0, 0)
print(max_score)