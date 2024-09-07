import math

N = int(input())
A = list(map(int,input().split()))
B = list(map(int,input().split()))

result = 0
for a in A:
    cur = max(0, a - B[0])
    result += 1 + math.ceil(cur / B[1])

print(result)