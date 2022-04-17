'''
pypy3
117348kb
232ms
'''

'''
로직 
- 구현 + bfs
- 원판 회전 함수 + 인접값 제거 및 평균 대체 함수

쟁점
- 원판간 이동은 경계 넘나들 수 없고, 원판 내 이동에서는 경계 넘나들 수 있음
 => 인접값 탐색시 벗어나는 값 조정
- 원판 값을 저장하는 데이터 구조가 중요 
 => 2차원 list로 [idx][value]형식으로 저장
- 평균 대체시 이미 원판에 모든값이 빈칸일 경우 예외처리 필요

배운점
- 시간초과가 걱정되는 상황이 아니라면 탐색을 늘려서 쉽게 풀어라

'''



from collections import deque
from copy import deepcopy
n,m,t = map(int,input().split())
#graph = [list(map(int,input().split())) for _ in range(n)]
#orders = [list(map(int,input().split())) for _ in range(t)]
graph = [] #index = 반지름 -1 // [idx][value]
orders = []

info =  input().split("\n")
for i in range(n):
    graph.append(list(map(int,info[i].split())))
for i in range(n,n+t):
    a,b,c  = map(int, info[i].split())
    orders.append([a,b,c])



'''회전
input : 회전 명령
참조 : 원판 상황
'''
def rotate_target(order):
    global target
    r,d,k = order

    for idx in range(r-1,n,r):
        if d == 0 : #시계방향 -> 뒤에 값이 앞으로
            target[idx] = target[idx][-k:] + target[idx][:-k]

        else: #반시계방향 -> 앞에 값이 뒤로
            target[idx] = target[idx][k:] + target[idx][:k]

'''인접 제거
참조 :원판 상황, 평균 계산
idx가 동일하면 경계 넘나들 수 있음
원판 간 경계는 넘을 수 없음
bfs
'''
didx = [1,-1,0,0]
dvalue = [0,0,1,-1]
def remove_target():
    global target
    fleg = 0  # 인접한 값이 있을 떄 마다 +1
    #값 선택
    for x in range(n): #원판
       for y in range(m): #값
            if target[x][y] > 0 : #값이 있다면
                q = deque()
                q.append((x,y))
                value = target[x][y]

                #인접값 탐색
                while q :
                    vx,vy = q.popleft()
                    for i in range(4):
                        nx,ny  = vx + didx[i], vy + dvalue[i]
                        ny = (ny + m )% m  #값은 인접값 넘을 수 있음
                        if nx < 0 or nx >= n  : continue
                        if target[nx][ny] == value :
                            target[vx][vy] = 0
                            target[nx][ny] =  0 #빈칸 삽입
                            fleg += 1  #인접한 값 있으면 카운트
                            q.append((nx,ny))

    if fleg == 0 : #인접한 값이 없을 경우
        total = 0
        count = 0
        for x in range(n):
            for y in range(m):
                if target[x][y] > 0 :  #빈칸 아니면 평균 계산
                    total += target[x][y]
                    count += 1

        if count != 0 : #모든칸이 이미 0이라면 변화없음
            mean = total / count
            for x in range(n):
                for y in range(m):
                    if target[x][y] == 0 : continue
                    if target[x][y] > mean : target[x][y] -= 1
                    elif target[x][y] < mean : target[x][y] += 1

target = deepcopy(graph)
for order in orders :
    rotate_target(order)
    remove_target()

print(sum(map(sum,target)))



