##로직
- 전형적인 시뮬레이션 문제
- 격자 나누기 -> 회전 - > 얼음 제거를 반복 후 bfs로 가장 큰 블럭을 탐색하면 됨

##쟁점
- 격자를 나눈 후 격자 내에서 회전 하는 것이 어려움
 => 격자의 시작점 호출을 반복한 후 격자 내부에서 회전시키면 됨

##배운점
- 대부분 경우에서 pypy3가 더 빠름


from collections import deque
n,q = map(int,input().split())
#graph = [list(map(int,input().split())) for _ in range(2**n)]
graph =[]
for i in input().split("\n"):
    graph.append(list(map(int,i.split())))
order = list(map(int,input().split()))

##파이어볼 마법 사용해 2^N을 2*l로 나누고 회전시키는 함수
def rotated(size):
    l = 2** size #격자 크기
    # 격자 나누기
    for i in range(0,length,l) :
        for j in range(0,length,l) :
            # 회전 시키기
            temp = [[0] * l for _ in range(l)]
            for a in range(l) :
                for b in range(l):
                    temp[b][l-1-a] = graph[i+a][j+b]

            for a in range(l):
                for b in range(l):
                    graph[i+a][j+b] = temp[a][b]


##녹을 수 있는 얼음 제거
def fire():
    temp =[]
    for x in range(length):
        for y in range(length):
            if graph[x][y] <= 0 : continue # 얼음이 있을때만
            count = 0
            for dx,dy in zip(dxs,dys):
                nx,ny = x + dx , y + dy
                if nx <0 or nx >= length or ny < 0 or ny >= length : continue
                if graph[nx][ny] > 0:
                   count += 1
            if count < 3 :
                temp.append((x,y))
    for x,y in temp:
        graph[x][y] -= 1


def bfs(graph,x,y,visited):
    global max_block
    if graph[x][y] == 0 : return 0
    queue = deque()
    queue.append((x,y))
    temp = [] #임시 저장. 블록의 크기 비교에 이용
    temp.append((x,y))
    visited[x][y] = True #방문처리

    while queue :
        x,y =queue.popleft()
        for dx,dy in zip(dxs,dys):
            nx,ny = x +dx , y + dy
            if nx < 0 or nx >= length or ny < 0 or ny>=length : continue
            if visited[nx][ny] == False and graph[nx][ny] > 0  : #방문한적없고 얼음이 있다면
                visited[nx][ny] = True
                temp.append((nx,ny))
                queue.append((nx,ny))
    return len(temp)


dxs = [0,0,1,-1]
dys = [1,-1,0,0]
length = len(graph)
#모든 명령 수행
for size in order :
    rotated(size)
    fire()

#블록 찾기

visited = [[False] * length for _ in range(length)]
max_block = 0
for x in range(length):
    for y in range(length):
        if visited[x][y] == False: #한번 방문한것은 또 방문하지 않음
            max_block = max(max_block,bfs(graph,x,y,visited))
if max_block ==1 : max_block = 0

print(sum(map(sum, graph)))
print(max_block)

