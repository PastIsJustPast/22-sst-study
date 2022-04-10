'''로직'''
#dfs+ 구현문제임
# 물고기 이동 -> 상어이동 (dfs)

'''쟁점'''
#dfs의 분기마다 이전 물고기 상태를 저장해줘야함
#=> deepcopy사용

'''배운점'''
#bfs문제는 최대로 점수를 내는 상황에서 사용됨
#특히 dfs함수 인자로 그 전까지의 점수를 기록해주면 됨



from copy import deepcopy
graph= [] # 공간
for info in input().split("\n"):
    fish = []
    data = list(map(int,info.split()))
    for i in range(4):
        fish.append([data[2*i] , data[2*i -1]])
    graph.append(fish)

#방향정의
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]


sx,sy,score = 0,0,0
max_score = 0
def dfs(sx,sy,score , graph ):
    global max_score
    score += graph[sx][sy][0]
    max_score = max(max_score,score)
    graph[sx][sy][0] = 0 #먹음

    '''물고기 움직임'''
    for f in range(1,17):
        f_x,f_y = -1,-1
        for x in range(4):
            for y in range(4):
                if graph[x][y][0] == f :
                    f_x,f_y = x,y
                    break
        if f_x == -1 and f_y == -1 : #이미 먹은 것
            continue
        f_d = graph[f_x][f_y][1] #방향 저장

        #물고기 이동
        for i in range(8):
            nd = (f_d + i) % 8
            nx,ny = f_x + dx[nd], f_y +dy[nd]

            if nx < 0 or ny >= 4 or ny <0 or ny >=4 or (nx==sx and ny == sy) : continue
            graph[f_x][f_y][1]=nd #방향 갱신
            graph[f_x][f_y] ,graph[nx][ny] =graph[nx][ny], graph[f_x][f_y]
            break

    '''상어가 물고기 먹고 움직임'''
    s_d = graph[sx][sy][1]
    for i in range(1,4):
        nx = sx + dx[s_d] * i
        ny = sy + dy[s_d] * i
        if nx < 0 or ny >=4 or ny <0 or ny >=4 and graph[nx][ny][0] >0 : #물고기가 있을 떄
            dfs(nx,ny,score,deepcopy(graph)) #딥카피로 원본 보존

dfs(0,0,0,graph)
print(max_score)