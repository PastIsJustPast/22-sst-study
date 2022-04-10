from collections import deque
n,k = map(int,input().split())
#graph = [list(map(int,input().split())) for _ in range(n)]
#chess = [list(map(int,input().split())) for _ in range(k)]
graph = []
chess = []
data = input().split("\n")
for i in range(n):
    graph.append(list(map(int,data[i].split())))
for j in range(n,n+ k):
    x,y,d = map(int,data[j].split())
    x,y,d = x-1,y-1,d-1
    chess.append([x,y,d])

#방향
dx = [0,0,-1,1] # 우 좌 상 하
dy = [1,-1,0,0]

#체스 말의 관계, 2차원리스트 위에 순서대로 쌓임(앞에 있는 번호가 아래에 있음
r = [[[] for _ in range(n)] for _ in range(n)]
i = 0
for x,y,d in chess :
    r[x][y] += [i]
    i +=1


def move():
    for i in range(k):
        x,y,d = chess[i] # 말 위치 및 방향
        #이동할 칸 탐색
        nx,ny = x + dx[d] , y+ dy[d]

        #이동하게 될 말 탐색
        temp = r[x][y][r[x][y].index(i):] #i번째 체스말 포함 그 위에 말들을 모두 temp에 담음
        del r[x][y][r[x][y].index(i):] #원래 칸에서 제거

        #이동(관계 갱신) #파란색+격자밖 -> 흰색 -> 빨간색 순으로 탐색
        if nx < 0 or nx >= n or ny <0 or ny >= n or graph[nx][ny] == 2 :  #격자 밖이나 파란칸
            #방향 바꿔서 재 탐색
            nd = (5 - d)% 4  # 0<->1, 2<->3
            nx,ny = x + dx[nd] , y + dy[nd]
            if nx < 0 or nx >= n or ny <0 or ny >= n or graph[nx][ny] == 2 : #또다시 격자 밖이나 파란칸이라면
                r[x][y] += temp  # 그자리에 관계 다시 두기
                for j in temp:
                    chess[j][2] = (5- chess[j][2]) % 4   #방향 모두 바꾸기
            else :  #격자나 파란칸이 아니라면
                r[nx][ny] += temp
                for j in temp :
                    chess[j][0:2] = [nx,ny] #방향 위치 다 바꾸기
                    chess[j][2] = (5 - chess[j][2]) % 4

        elif graph[nx][ny] == 0 : #흰색으로 이동한다면/관계는 안바뀜
            r[nx][ny] += temp #그대로 얹음

            #이동(위치 갱신)
            for j in temp:
                chess[j][0:2] = [nx,ny] # 위치 갱신

        elif graph[nx][ny] == 1 : #빨간색으로 이동한다면/관계는 다 바뀜
            temp = temp[::-1] #관계 바꿈
            r[nx][ny] += temp #그대로 얹음

            # 이동(위치 갱신)
            for j in temp:
                chess[j][0:2] = [nx, ny]  # 위치 갱신


def solution():
    count = 0
    while count < 999 :
        count +=1
        move()
        for x in range(n):
            for y in range(n):
               if len(r[x][y]) == k :
                    print(count)
                    return
    print(-1)
#max([max(list(map(len, r[i]))) for i in range(k)]) == k:

#solution()


