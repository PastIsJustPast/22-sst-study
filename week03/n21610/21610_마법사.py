## 로직
- 구름 이동 -> 물 증가 -> 물 복사 -> 구름 생성을 반복함
- 구름 이동 후 구름을 갱신하고, 구름 생성후 구름을 갱신
- 구름은 경계를 넘을 수 있지만 물복사 탐색은 경계를 넘을 수 없음


n,m = map(int,input().split())
#graph = [list(map(int,input().split())) for _ in range(n)]
graph = []
for info in input().split("\n"):
    graph.append(list(map(int,info.split())))
magic = [list(map(int,input().split())) for _ in range(m)]



## 구름이동 함수
#input : 명령
#output : 구름 위치
#구름은 경계를 넘나들수 있음
direc = {1:[0,-1],2:[-1,-1],3:[-1,0],4:[-1,1],5:[0,1],6:[1,1],7:[1,0],8:[1,-1]} #좌 좌상 상 우상 우 우하 하 좌하
def move_cloud(d,s):
    temp = []
    #구름 이동
    for x,y in cloud :
        nx = (x + s * direc[d][0] + n ) % n #구름은 경계를 넘나들 수 있음
        ny = (y + s * direc[d][1] + n ) % n
        temp.append((nx,ny))
    return temp


##물 증가 및 복사함수/ 구름 재생성
#input : 구름 우치
#output : cloud
def water(cloud):
    #물증가
    for x,y in cloud :
        graph[x][y] +=1

    dx = [1,1,-1,-1]
    dy = [1,-1,-1,1]
    #물 복사
    for x,y in cloud :
        #대각방향 탐색
        for i in range(4):
            nx,ny = x + dx[i], y + dy[i]
            if nx <0 or nx >= n or ny <0 or ny >= n : continue #물복사 탐색은 경계를 넘지 않음
            if graph[nx][ny] >= 1 : graph[x][y] += 1 #물 복사됨

    #구름 생성
    temp = []
    for x in range(n):
        for y in range(n):
            if graph[x][y] >=2 and (x,y) not in cloud:
                temp.append((x,y))
                graph[x][y] -= 2
    return temp


#초기 구름 위치
cloud = [(n-2,0),(n-1,1),(n-1,0),(n-2,1)]

for d,s in magic :
    cloud = move_cloud(d,s)
    cloud = water(cloud)

print(sum(map(sum,graph)))