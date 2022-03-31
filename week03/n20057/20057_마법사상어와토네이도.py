##로직
- 토네이도 방향에 따라 모래양이 어디로 퍼지는지 사전에 정의하는 것이 편리함
- 각 방향으로 모래양이 퍼지는데 규칙이 존재/ 한 방향만 정의해도 나머지 방향 쉽게 정의가능
- 토네이도 방향과 좌표가 주어지면 모래를 뿌려주는 함수 정의 / output은 격자밖으로 나가는 모래양
- 토네이도의 방향과 좌표를 결정하는 for문 생성 필요
- 이때, 중심으로부터 얼마나 멀리 떨어져있는 가를 기준으로 토네이도 방향, 좌표 결정하면 됨

## 쟁점
- 모래가 퍼지는 분포를 사전에 손으로 정의해야함
- 격자밖으로 나가는 양을 세야함

##배운점
- 중심으로부터 떨어진 level을 활용하면 격자 안 회전 쉬움


#토네이도 방향에 따라 사전에 방향을 정의해주는 것이 필요하다.

from collections import deque
from math import floor
n = int(input())
#graph =[list(map(int,input().split())) for _ in range(n)]

graph = []
for i in input().split("\n"):
    graph.append(list(map(int,i.split())))

left = [[-2,0,0.02],[2,0,0.02],[1,0,0.07],[-1,0,0.07],[-1,1,0.01],[1,1,0.01],[-1,-1,0.1],[1,-1,0.1],[0,-2,0.05],[0,-1,"a"]]
down = [[-y,x,z] for x,y,z in left]
right = [[x,-y,z] for x,y,z in left]
up = [[-x,y,z] for x,y,z in down]
direc = {0 : left, 1 : down, 2 : right , 3 : up}

def move_tornado(x,y,d):
    global answer
    sand = graph[x][y]
    graph[x][y] = 0
    #모래 뿌리기
    total = 0
    for dx,dy,dz in direc[d] :
        nx,ny =x + dx,y+dy

        #알파 아닌경우
        if dz != "a" :
            nz = floor(sand * dz) #이동할 모래 양
        else : #알파인 경우
            nz = sand - total
        #격자밖이면
        if nx < 0 or nx >= n or ny <0 or ny >= n :
            answer += nz #나간 모래양에 추가
            total += nz
        else :
           graph[nx][ny] += nz #격자에 추가
           total += nz


##토네이도 방향
x,y = n//2,n//2
dx = [0,1,0,-1] #좌 하 우 상
dy = [-1,0,1,0]
graph
answer = 0
for idx in range(1,(n//2)+1): #중심에서 얼마나 벗어났는가
    #index가 시작될 때 무조건 왼쪽 한번
    x = x + dx[0]
    y = y + dy[0]
    move_tornado(x,y,0)
    #아래로 2 * idx -1 회
    for _ in range(2*idx -1) :
        x = x + dx[1]
        y = y + dy[1]
        move_tornado(x, y, 1)
    #우, 상, 좌 2 * idx회
    for d in [2,3,0]:
        for _ in range(2*idx) :
            x = x + dx[d]
            y = y + dy[d]
            move_tornado(x,y,d)

print(answer)



