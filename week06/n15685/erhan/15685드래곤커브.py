'''
python3    pypy3
31004kb     92ms
115252kb    144ms
'''



'''
로직
- 구현
- 방향을 이용한 세대별 패턴 파악 가능
 - 현재 세대는 이전 세대의 역순 + 1

배운점 
- 너무 구현하기 어려운 시뮬레이션 문제는 보통 패턴이 숨어있음
- 방향별 반복동작이 있다면 방향에 따라 패턴 파악 쉬움
- 1 인덱스 사용시 탐색범위 신경쓰기

'''




from copy import deepcopy
n = int(input())
orders = [list(map(int,input().split())) for _ in range(n)]
'''
orders = []
for info in input().split("\n"):
    orders.append(list(map(int,info.split())))
'''


'''드래곤 커브 찾아서 그래프에 입력하는 함수 
input = order(x,y,d,g)
output = 위치

방향 0 일
0세대 : 0 1 
1세대 : 0 1 2 1
2세대 : 0 1 2 1 2 3 2 1
3세대 : 0 1 2 1 2 3 2 1 2 3 0 3 2 3 2 1
이전세대의 역순에 +1 을 추가하면 됨
방향별 공통점이 있으며, 다음 세대는 이전 세대의 끝점과 연결된다는 점에서 쉽게 유추할 수 있음
'''
dx = [1,0,-1,0] #우 상 좌 하
dy = [0,-1,0,1]
row,col = 0,0
def dragon(order):
    global graph,row,col
    x,y,d,g = order
    #이동 방향 설정
    direc = [d]
    for _ in range(g) :
        direc = direc + [x+1 for x in direc[::-1]]
        for i in range(len(direc)) :
            if direc[i] == 4 : direc[i] = 0

    #이동 위치
    graph[y][x] = 1
    for i in direc :
        y,x = y + dy[i], x + dx[i]
        graph[y][x] = 1
        if y > row : row = y
        if x > col : col = x


graph = [[0 for _ in range(101)] for _ in range(101)]
for order in orders:
    dragon(order)

count = 0
for i in range(row):
    for j in range(col):
        if graph[i][j] == 1 and graph[i+1][j] == 1 and graph[i][j+1]== 1 and graph[i+1][j+1] == 1 :
            count +=1

print(count)

