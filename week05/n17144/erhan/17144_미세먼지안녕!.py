'''
pypy3
119608 km
504ms
'''
'''
풀이 방법
- 시뮬레이션
- 미세먼지 이동 -> 공기청정 -> 반복
- 미세먼지 이동함수와 공기청정 함수를 만듦
- 미세먼지는 동시에 움직이기 때문에 임시공간에 미세먼지를 확산시킨 다음 return
- 공기청정 함수는 위 방향과 아래방향을 따로 구현했으며 바람이 부는 방향 반대로 큐 구조에 먼지를 쌓고 다시 뿌림  
'''



from collections import deque
from copy import deepcopy
r,c,t = map(int,input().split())
#graph = [list(map(int,input().split())) for _ in range(r)]
graph = []
for info in input().split("\n"):
    graph.append(list(map(int,info.split())))

robot = []
for i in range(r):
    for j in range(c):
        if graph[i][j] == -1:
            robot.append((i,j))


dust = deepcopy(graph) #미세먼지를 계속 바꾸기 때문

'''미세먼지 이동함수
input : 
참조 : 미세먼지의 현재위치, 로봇의 위치
output : 미세먼지 이동 후 위치
'''
dx = [-1,0,1,0] #상 우 하 좌
dy = [0,1,0,-1]

def move_dust():
    temp = [[0] * c for _ in range(r)] # 이동 후 위치 저장
    for x,y in robot :
        temp[x][y] = -1
    x,y = 0,7
    #미세먼지 선택(격자를 탐색하는게 1차원 리스트에서 찾고 제거하는 거보다 빠름)
    for x in range(r):
        for y in range(c):
            if dust[x][y] > 0 :
                #이동할 위치 탐색 후 이동
                total_dust = 0
                for i in range(4):
                    nx,ny = x +dx[i],y + dy[i]
                    if nx < 0 or nx >= r or ny < 0 or ny>=c or temp[nx][ny] == -1 : #격자밖이거나 로봇이면
                        continue
                    temp[nx][ny] += dust[x][y] // 5  #임시공간으로 이동
                    total_dust += dust[x][y] // 5   #확산된 양 체크
                temp[x][y]+= dust[x][y] - total_dust  #확산되고 남은 양
    return temp

'''미세먼지 기게
참조 : 로봇의 위치, 현 미세먼지 위치
output : 현 미세먼지 위치

-위와 아래를 따로 처리함
-위에서는 큐 자료구조를 사용해서 (a-2,0)으로 시계방향 수집후 다시 뿌림
-아래에서는 큐 자료구조 사용해서 (b-2,0)으로 반시계로 수집후 다시 뿌림
'''
def air_fresh():
    up,down = [x[0] for x in robot] #로봇의 위치

    '''up'''
    udx = [-1, 0, 1, 0]  # 상 우 하 좌
    udy = [0, 1, 0, -1]

    sx, sy = up - 1, 0 #로봇 위에서부터 시작
    d = 0 #상
    #미세먼지 흡수
    dust[sx][sy] = 0
    #미세먼지 수집
    q = deque()
    while True :
        nx,ny = sx + udx[d] , sy + udy[d]
        if nx < 0 or nx >= down or ny < 0 or ny >= c : #격자 밖으로 나가면 방향 전환
            d = (d + 1 ) % 4
            nx,ny= sx + udx[d] , sy + udy[d]
        elif dust[nx][ny] == -1 : break #로봇으로 돌아오면 끝
        q.append(dust[nx][ny]) #수집
        dust[nx][ny] = 0
        sx,sy = nx,ny
    #미세먼지 뿌리기
    sx, sy = up - 1, 0
    d = 0
    while q :
        dust[sx][sy] = q.popleft()
        nx, ny = sx + udx[d], sy + udy[d]
        if nx < 0 or nx >= down or ny < 0 or ny >= c:  # 격자 밖이나 아래로 내려가면
            d = (d + 1) % 4
            nx, ny = sx + udx[d], sy + udy[d]
        sx,sy = nx,ny

    '''down'''
    ddx = [1, 0, -1, 0]  # 하 우 상 좌
    ddy = [0, 1, 0, -1]

    sx,sy = down+1, 0
    d = 0  # 하
    # 미세먼지 흡수
    dust[sx][sy] = 0

    # 미세먼지 수집
    q = deque()
    while True :
        nx,ny = sx + ddx[d] , sy + ddy[d]
        if nx < down or nx >= r or ny < 0 or ny >= c : #격자 밖이나 위로 올라가면
            d = (d + 1 ) % 4
            nx,ny= sx + ddx[d] , sy + ddy[d]
        elif dust[nx][ny] == -1 : break #로봇으로 돌아오면 끝
        q.append(dust[nx][ny]) #수집
        dust[nx][ny] = 0
        sx,sy = nx,ny

    #미세먼지 뿌리기
    sx, sy = down + 1, 0
    d = 0
    while q :
        dust[sx][sy] = q.popleft()
        nx, ny = sx + ddx[d], sy + ddy[d]
        if nx < down or nx >= r or ny < 0 or ny >= c :  # 격자 밖으로 나가면 방향 전환
            d = (d + 1) % 4
            nx, ny = sx + ddx[d], sy + ddy[d]
        sx,sy = nx,ny


#작업시작
dust = deepcopy(graph)
for _ in range(t):
    dust = move_dust()
    air_fresh()

#미세먼지 계산
answer = 0
for i in range(r):
    for j in range(c):
        if dust[i][j] > 0 :
            answer += dust[i][j]

print(answer)






