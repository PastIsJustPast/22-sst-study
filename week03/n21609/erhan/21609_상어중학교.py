##풀이 로직
- bfs로 그륩을 찾는함수, 중력함수, 반시계회전 함수를 각각 생성한다
- 모든 행과 열에 대해 그륩을 찾고 가장 그륩 블록의 수가 큰 것을 탐색한다
- 이때, 첫행 첫열부터 시작하되 이전까지 최대 블록의 수 이상의 그륩이 나오면 최대 블록 수를 갱신해준다
- 또, 한번 색깔 블록을 탐색해서 최대 그륩 블록으로 갱신되지 않은 블록은 두번 탐색할 필요 없으니 방문처리 한다
- 이때, 무지개 색깔 블록은 다음 차례 탐색에 사용될 수 있도록 방문처리에서 뺀다

##쟁점
- 시뮬레이션 문제로 반복되는 작업을 함수화 하는 것이 중요함
- 검은 칸은 중력에 영향받지 않는다.
## 배운점
- 중력함수에서 큐를 활용한 수집 및 뿌리기 작업 때, 검은칸을 수집하고 검은칸에서 다시 뿌리면 검은 칸은 중력에 영향 받지 않음



from collections import deque
#상어중학교
n,m = map(int,input().split())
graph =[]
for info in input().split("\n"):
    graph.append(list(map(int,info.split())))

dx = [0,0,1,-1]
dy = [1,-1,0,0]


#그룹의 찾기
def search_group(x,y,col):
    if col <= 0  : return False  # 만약 일반블록 아니면 그냥 끝
    q=deque()
    q.append((x,y))
    visited =[]
    visited.append((x,y))

    while q :
        x,y = q.popleft()
        #4방향 탐색
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            #이동 위치의 예외 판단 (격자 벗어나기, 검은 블록, 빈칸)
            if nx < 0 or nx >=n or ny <0 or ny >= n or graph[nx][ny]  <0  : continue

            #방문 판단 후 이동
            if (nx,ny) not in visited : #방문한 적이 없고
                if graph[nx][ny] == col or graph[nx][ny] == 0 : # 같은 색이거나  무지개 색인경우
                    visited.append((nx,ny))
                    q.append((nx,ny))

    if len(visited) >=2 : #그륩안에 블록이 두개 이상이라면
        return visited
    return False

#중력 함수 만들기
def gravity(graph):
    for j in range(n):
        temp = deque()
        count = []
        #수집
        for i in range(n - 1, -1, -1):  # 가장 밑에서부터
            if graph[i][j] >= 0 :  # 빈칸과 검은칸 아니라면
                temp.append((graph[i][j]))  # 큐에 색 삽입 후 빈칸으로 대처
                graph[i][j] = -2
            if graph[i][j] == -1 : #검은칸도 수집하지만 그대로 검은칸으로 둠
                temp.append((graph[i][j]))
        #뿌리기
        i = n - 1
        while temp:  # 큐가 바닥날때까지 색 채우기
            if temp[0] >=0 :
                graph[i][j] = temp.popleft()
                i -= 1
            else :
                if graph[i][j] == -1 : #검은칸을 만나면 큐에서 제거
                    temp.popleft()
                    i -= 1
                else : #만날 때 까지 그냥 지나침
                    i -=1
    return graph

#회전
def rotated(graph):
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[n-1-j][i] = graph[i][j]
    return result


#가장 큰 그륩 찾기 + 제거 -> 제거하면 -2로 기록
score = 0
while True :
    ##가장 큰 볼록 그륩 찾기
    visited = []  # 한번 그륩으로 속한 위치는 또 탐색할 필요 없음/ 하지만 무지개 블록은 다시 빼줘야함
    max_block = []
    for i in range(n):
        for j in range(n):
            if graph[i][j] <= 0 : continue#색깔 블록아니면 우선 넘김
            if (i, j) in visited: continue #방문한 적 있으면 넘김
            temp = search_group(i, j, graph[i][j])  # 블록 찾고
            if temp != False:  # 블록의 기준을 만족한다면
                for x,y in temp:
                    if graph[x][y] > 0 :
                        visited.append((x,y))  # 색깔공은 방문처리
                if len(max_block) <= len(temp):  # 탐색한 그륩이 이전 그륩보다 크다면(행, 열 순으로 탐색하기 때문에 크기가 똑같으면 행, 열 우선으로 저장
                    max_block = temp

    ##만약 탐색했더니 볼록 그륩이 없다면
    if max_block == []: # 블록이 없는 것
        break

    ##제거
    for x,y in max_block :
        graph[x][y] = -2
    score += len(max_block) ** 2

    ##중력
    graph= gravity(graph)
    ##회전
    graph= rotated(graph)
    ##중력
    graph = gravity(graph)

print(score)






