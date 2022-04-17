'''
pypy3
225028km
2876ms
'''

'''로직
- 낚시 -> 상어이동 -> 낚시왕 이동
- 전형적인 시뮬레이션 문제
- 상어가 움직인 자리를 temp에 입력하고 겹치는 상어들이 있다면 가장 큰 상어만 남김
- 상어가 움직일때는 상어가 움직일 자리 탐색 -> 격자 확인 -> 이동을 반복

'''

'''배운점
- 초기 데이터 배열을 반복적으로 수정할 때는 deepcopy를 통해 원본을 훼손하지 않고 분석하는 것이 적절함
- 알파벳 겹치는거 신경써야함
'''



from copy import deepcopy
r,c,m = map(int,input().split())

sharks = [[[] for _ in range(c)] for _ in range(r)]
if m != 0 :
    for info in input().split("\n"):
        x,y,s,d,z = map(int,info.split())
        sharks[x-1][y-1].append((s,d-1,z)) #속도, 방향 , 크기

#방향 정의
dx = [-1,1,0,0] #상 하 우 좌
dy = [0,0,1,-1]
change = [1,0,3,2]

'''상어 이동 함수'''

def move_sharks(sharks):
    temp =[[[] for _ in range(c)] for _ in range(r)]
    #상어 선택
    for x in range(r):
        for y in range(c):
            if sharks[x][y] != [] : #만약 상어가 있다면
                sx, sy = x, y  #x,y : 원래 위치 sx,sy : 다음위치, nx,ny : 탐색위치
                ss,sd,sz = sharks[sx][sy][0]
                #이동할 위치 탐색
                length = 1
                while length <= ss :
                    nx,ny = sx + dx[sd], sy + dy[sd]
                    if nx < 0 or nx >= r or ny < 0 or ny >=c  :#격자밖이라면
                        sd = change[sd]
                        nx,ny = sx + dx[sd], sy + dy[sd] #방향 바꿈
                    length += 1
                    sx,sy = nx,ny


                if temp[sx][sy] != [] : #이미 그 자리에 있다면 크기비교
                    if sz > temp[sx][sy][0][2] :

                        temp[sx][sy]= []
                        temp[sx][sy].append((ss,sd,sz))

                else :
                    temp[sx][sy].append((ss,sd,sz))

    return temp

'''낚시꾼의 이동 후 제거'''
score = 0
result = deepcopy(sharks)
for j in range(c):
    #탐색 후 제거
    for i in range(r):
        if result[i][j] != [] :
            score += result[i][j][0][2] # 점수추가
            result[i][j] = []  #제거
            break
    # 상어 이동
    result = move_sharks(result)



print(score)


