'''로직'''
#냄새 뿌리기 -> 상어이동 -> 겹치는것 제거 -> 냄새 제거의 반복
#겹치는 것 제거하기 위해 임시 공간에 상어의 위치를 저장한 후 다시 graph로 옮김

'''쟁점'''
#데이터 저장 배열이 가장 핵심인 문제 같음
#상어 위치, 냄새 위치, 상어 번호별 방향별 우선순위를 따로 저장
#상어 번호별 방향별 우선순위를 2차열 리스트에 리스트로 표현


#시간 초과남.

import heapq

n,m,k = map(int,input().split())
graph = [list(map(int,input().split())) for _ in range(n)]
direc= list(map(int,input().split()))
direc = list(map(lambda x : x-1 , direc))

prior = [[] for _ in range(m)]
for i in range(m) :
    for j in range(4) :
        a,b,c,d = map(int,input().split())
        a,b,c,d = a-1,b-1,c-1,d-1
        prior[i].append([a,b,c,d])



#냄새
smell = [[[] * n for _ in range(n)] for _ in range(n)]
dx = [-1,1,0,0]
dy = [0,0,-1,1]

'''상어 이동 함수'''
def move_shark(num,sx,sy): #숫자는 1씩 큼
    graph[sx][sy] = 0 #빈칸으로 바꿈
    sd = direc[num-1] #상어의 현재 방향

    #우선순위대로 탐색
    for i in prior[num-1][sd] : #상어의 현재 방향
        nx = sx + dx[i]
        ny = sy + dy[i]
        if nx <0 or nx >= n or ny<0 or ny >= n : continue
        #이동 - 빈칸이 있다면 우선적으로 이동
        if smell[nx][ny] == [] :
            temp.append((num,nx,ny)) # 임시공간에 우선 저장
            direc[num-1] = i #방향수정
            return

    #만약 모두 냄새가 있다면 자기 칸으로 이동
    for i in prior[num - 1][sd]:  # 상어의 현재 방향
        nx = sx + dx[i]
        ny = sy + dy[i]
        if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
        if smell[nx][ny] != [] and smell[nx][ny][0] == num :
            temp.append((num,nx,ny))
            direc[num - 1] = i
            return



count = 0
while True :
    shark =[]
    heapq.heapify(shark)
    '''상어 피뿌리기'''
    for i in range(n):
        for j in range(n):
            if graph[i][j] >0 :
                heapq.heappush(shark,(graph[i][j],i,j)) #num,sx,sy
                smell[i][j] = [graph[i][j],k] #본인 냄새인 칸에는 이동할 수 있음

    '''전체 상어 이동하기'''
    temp = [] # 임시공간 생성
    while shark :
        num,sx,sy = heapq.heappop(shark)
        move_shark(num,sx,sy)

    for num,sx,sy in temp :
        if graph[sx][sy] != 0 : continue # 이미 빠른 번호의 상어가 있으면 그 뒤 상어는 탈출
        graph[sx][sy] = num #이동

    count += 1 #전체 이동 후 횟수 증가

    if sum(map(sum,graph)) == 1 : break

    '''피 제거'''
    for i in range(n):
        for j in range(n):
            if smell[i][j] != [] :
                smell[i][j][1] -=1
                if smell[i][j][1] == 0 : smell[i][j] = []


print(count)
