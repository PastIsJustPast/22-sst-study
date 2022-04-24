'''
Python3  pypy3
32450kb 116908km
108ms  184ms
'''

'''로직
- bfs
- 상어의 다음 이동 위치 및 거리 함수 / 이동, 먹기, 크기증가 함수로 구성
- 또, 동일한 거리에 먹을 수 있는 물고기 중 행, 열 우선순위 
  => 상어로 부터 동일한 거리에 있는 위치를 동시에 탐색
  
시간복잡도
물고기 최대 수 N-1
상어 현재 위치에서 최대로 멀리 탐색할 때 N
O(N**2)
'''


from collections import deque
from copy import deepcopy
n = int(input())
graph = [list(map(int,input().split())) for _ in range(n)]



'''상어의 이동 위치 함수 
input :  물고기 위치 및 크기/ 상어 위치(sx,sy)
참조 : 물고기 크기 level 
output : 이동할 수 있는 위치

bfs는 시작 지점으로부터 길이가 같은 지점을 동시에 탐색함
'''
dx = [1,-1,0,0]
dy = [0,0,1,-1]

def search_loc(fish,sx,sy):
    q = deque()
    q.append((sx,sy))
    visited = [[False for _ in range(n)] for _ in range(n)]
    visited[sx][sy] = True
    d = 0 #거리
    while q :
        d += 1
        can_eat = []  # 먹을 수 있는 물고기 위치/ 거리가 같음
        for _ in range(len(q)) : #큐 길이만큼 탐색 수행, 같이 탐색되는 곳은 상어로부터 길이가 같음
            sx, sy = q.popleft()
            for i in range(4) :
                nx,ny = sx + dx[i], sy +dy[i]

                #예외처리
                if nx < 0 or nx >= n or ny < 0 or ny >= n or fish[nx][ny] > level : continue #상어보다 크다면 이동불가

                #이동가능한 곳
                if visited[nx][ny] == False :
                    visited[nx][ny] = True
                    q.append((nx,ny))


                    if 0 < fish[nx][ny] < level :
                        can_eat.append((nx,ny,d))


        #먹을 수 있는 물고기가 존재한다면
        if can_eat != [] :
            can_eat.sort()
            fx,fy,d = can_eat[0]
            return [fx,fy,d]

    return [-1]

'''이동 및 먹기
이동할 위치 탐색 -> 이동 및 먹기 -> 크기 변화
'''
def solution():
    global level,sx,sy
    t = 0
    count = 0
    while 1:
        #이동가능 위치 탐색
        now = search_loc(fish, sx, sy)
        if len(now) == 1:  # 더이상 없음
            print(t)
            return
        else : #먹을 물고기가 있음

            #이동 및 먹기
            nx,ny,d = now
            t += d
            fish[nx][ny] = 9
            fish[sx][sy] = 0
            sx,sy, = nx,ny


            #크기 변경
            count += 1
            if count == level :
                level += 1
                count = 0


fish = deepcopy(graph)
level= 2
for i in range(n):
    for j in range(n):
        if fish[i][j] == 9 :
            sx,sy = i,j


solution()




