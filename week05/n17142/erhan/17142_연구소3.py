'''
pypy3
118884kb
380 ms
'''

from itertools import combinations
from copy import deepcopy
from collections import deque
'''
로직
- bfs + combinations
- 활성화바이러스 -> 상하좌우 복사 -> 비활성화 유무 체크 -> 이동한 칸이 비활성화를 활성화
- 1초마다 바이러스가 동시에 증식될 수 있도록 처리
 => 일반적인 BFS를 사용하지 않음  
- 정지조건 : 더 이상 증식은 없지만 빈칸이 남은경우 / 모든 빈칸을 차지한 경우


쟁점 
- 시간 줄이는 것 중요 
 ㄱ. 한번 탐색한 위치는 두번 볼필요 없음
 ㄴ. 이미 시간이 최소값 보다 클 경우 종료

정지조건
 ㄱ. 모든 칸을 활성화 바이러스로 채우는게 아님
 ㄴ. 모든 빈칸에 증식이 되면 종료
 ㄷ. 매 초 마다 모든 빈칸을 찾으면 시간 초과
 ㄹ. 바이러스가 빈칸을 채울 때 마다 카운트 하여 정지조건 입력  

틀린 이유
- 비활성화 바이러스까지 모두 활성화시키는 시간을 구했음
- 빈칸이 없는 경우를 고려하지 않음
- 연구실 상황을 탐색하기 위해 2차원 배열 대신 1차원 배열을 이용하는 것이 더 오래 걸림
 => list : 접근 빠름 / 데이터 추가 제거 느림
- 백트래킹을 쓰면 오히려 시간이 오래걸림

배운점
- 어떤 정보를 어떤 데이터 구조로 저장할 것인지가 매우 중요함

개선사항
- 코드를 더 간단하게 짤 수 있을 것 같음
'''

n,m = map(int,input().split())
graph = [list(map(int,input().split())) for _ in range(n)] #초기상태


'''바이러스 이동함수
참조 : combinations을 통해 활성화된 바이러스 _virus를 참조함
      연구실 상황인 _status를 참조함
output : 바이러스가 전염되는 최소시간

정지규칙 : 1.더 이상 전염이 일어나지 않지만 빈칸이 존재하는 경우 , 2. 전염이 끝난 경우
 => 바이러스가 빈칸을 감염시킬 때 마다 fleg를 증가시키고 fleg가 length와 같아지면 탐색 종료 
 => 더 이상 증식될 바이러가 없지만 fleg가 length보다 작다면 종료
'''
def  move_virus(_virus,_status):
    global min_value
    status = deepcopy(_status)
    virus = deque(_virus) # 더이상 복제가 안되는 바이러스를 또 탐색하는것 방지
    non_virus = list(set(_space) - set(_virus))
    # 상태 갱신
    for x, y in virus:
        status[x][y] = 0  # 활성화는 0초부터
    for x, y in non_virus:
        status[x][y] = -9  # 비활성화는 -9

    fleg = 0 #바이러스가 빈칸을 차지할 때마다 늘어남

    '''바이러스 전염
    이때, 매 초마다 모든 바이러스들이 동시에 증식함
    bfs를 사용할 경우에 인접한 바이러스부터 먼저 증식
    일반적인 bfs로는 초별 증식을 구현하기 어려움
    큐에 있는 바이러스를 모두 증식 -> 인접한 바이러스를 다시 큐에 삽입 -> 반복처리 
    '''

    '''바이러스 이동'''
    for t in range(1, 2000):
        if t > min_value : return -1  #최소시간을 초과하면 정지
        '''활성화 바이러스의 복제'''
        for idx in range(len(virus)) :
            vx,vy = virus.popleft()

            for i in range(4):
                nx, ny = vx + dx[i], vy + dy[i]
                if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
                if status[nx][ny] == -1:  # 빈칸이면
                    status[nx][ny] = t
                    virus.append((nx,ny))
                    fleg += 1 #빈칸을 감염시키면 카운트

                elif status[nx][ny] == -9:  # 비활성화 바이러스를 감염시키면 카운트하지 않음
                    status[nx][ny] = t
                    virus.append((nx, ny))

        #정지조건
        if fleg == length : return t #완전 정복

        if virus == deque() and fleg < length : return -1 #불완전 정복

    return -1

dx = [1,-1,0,0]
dy = [0,0,1,-1]

'''활성화 상태 나타내는 배열'''
_status = [[0] * n for _ in range(n)]
_space = []
length = 0
for i in range(n):
    for j in range(n) :
        if graph[i][j] == 0 :
            _status[i][j] = -1 #빈칸은 -1
            length += 1
        elif graph[i][j] == 1 : _status[i][j] = -2 #벽은 -2
        else : _space.append((i,j)) #바이러스만 따로 저장



'''활성화 바이러스 선택'''
min_value = 10000
for i in combinations(_space,m):
    _virus = list(i)  # 활성화 바이러스
    now_value = move_virus(_virus,_status)
    if now_value == -1 : continue
    min_value = min(min_value,now_value)

if length == 0 : print(0)
elif min_value == 10000 :
    print(-1)
else : print(min_value)





