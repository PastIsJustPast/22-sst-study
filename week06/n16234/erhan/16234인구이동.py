'''
 python3    pypy3
            144712kb
            728ms
'''


'''
로직
- bfs 및 완전탐색
- 매 초 마다 모든 나라에 대해 bfs를 수행해야함
- 시간 초과 고려할 필요 있음

쟁점
- bfs안에서 방문처리와 글로벌 방문처리를 따로 하는 것이 어려움
 => 글로벌 방문처리할때는 solution 함수 사용하지 말것
- 정지조건
 => bfs함수의 return에 인구이동시 1 아니면 0을 출력해 fleg를 사용
    모든 나라에 대해 bfs로 연합을 찾고 fleg가 0이면 인구이동 없었던 것

배운점 
- list의 접근이 추가제거보다 훨씬 빠르다.
- 웬만한 상황에서는 list의 접근을 이용하자
- united를 2차원 격자로 할때는 시간 통과
- 1차원 배열로 두면 실패

- bfs를 반복적으로 수행할 때 bfs를 수행할지 말지 사전에 검증함으로써 시간을 비약적으로 단축시킬 수 있음

개선점
- k * n^2 번 bfs가 호출됨
'''


from copy import deepcopy
from collections import deque
n,l,r = map(int,input().split())
#graph = [list(map(int,input().split())) for _ in range(n)]
graph = []
for info in input().split("\n"):
    graph.append(list(map(int,info.split())))



'''
연합찾고 인구 이동 함수
input  :  시작위치
참조 : 인구수, 연합 포함 유무
output : 변화 후 인구수

탐색과 연합포함은 별개로 처리
'''
dx = [1,0,-1,0]
dy = [0,1,0,-1]


def union(x,y) :
    global worlds, united
    visited = [(x,y)] #연합인 나라를 다시 찾아야하므로 1차원 리스트
    q = deque()
    q.append((x,y))

    #연합 상황
    total = worlds[x][y]
    count = 1
    united[x][y] = True

    #연합 탐색
    while q :
        x,y = q.popleft()
        for i in range(4):
            nx,ny = x + dx[i], y + dy[i]
            #예외처리 : 격자밖 / bfs내 방문 / 연합에 포함
            if nx < 0 or nx >= n or ny < 0 or ny >= n or (nx,ny) in visited or united[nx][ny] == True :continue
            now = worlds[nx][ny]
            if l <= abs(now - worlds[x][y]) <= r:  # 연합이면
                visited.append((nx, ny))
                q.append((nx,ny))
                total += now
                count += 1
                united[nx][ny] = True
    #연합 확인
    if count == 1 :
        return 0 #국경이동 없음

    #연합 평균
    means= total//count
    for x,y in visited :
        worlds[x][y] = means

    return 1 #국경이동 있음


'''인구이동'''
worlds = deepcopy(graph)


for t in range(0, 2001):
    fleg = 0
    united = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if united[i][j] == False:

                need_bfs = False

                for idx in range(4):
                    ni,nj = i +dx[idx], j +dy[idx]
                    if ni < 0 or ni >= n or nj < 0 or nj >= n : continue
                    elif united[ni][nj] == False and (l <= abs(worlds[i][j] - worlds[ni][nj]) <= r ) :
                        need_bfs = True
                        break

                if need_bfs :
                    fleg += union(i, j)

    if fleg == 0:  # 어떠한 인구변화도 없다면
        print(t)
        break

