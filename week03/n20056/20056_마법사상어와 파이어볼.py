##로직
-아주복잡한 구현문제
-불의 위치와 불 이동은 별개로 고려
-불은 이동하더라도 방향과 속도는 그대로 가지고 있음
-이동을 새롭게 명령한다는 것은 쪼개지거나 한번 이동한 불꽃을 방향과 속도대로 이동시키는 것을 의미
-즉, 불 이동 -> 겹치는 것 체크 후 쪼개기 -> 불 위치 갱신

##쟁점
- 불 이동시 질량, 방향,속도 정보 필요
=> 2차원 배열에 리스트 형식으로 정리(3차원 배열)

##배운점
- 격자 밖의 위치를 격자 안으로 옮기는 방법
 => x = (x + n) %



n,m,k = map(int,input().split())
fire = [list(map(int,input().split())) for _ in range(m)]


#방향 함수
dx = [-1,-1,0,1,1,1,0,-1]#0,1,2,3,4,5,6,7,8
dy = [0,1,1,1,0,-1,-1,-1]


##불꽃 이동함수
##겹치는 불꽃을 네 방향으로 나누는 함수

graph = [[[] for _ in range(n)] for _ in range(n)]  #불꽃의 위치

#불꽃 위치
for r,c,m,s,d in fire:
    graph[r-1][c-1].append((m,s,d))


def fire_move(graph):
    move = [[[] for _ in range(n)] for _ in range(n)] #불꽃 이동 후 위치/ 주기적으로 갱신
    for i in range(n):
        for j in range(n):
            if graph[i][j] != [] : #격자 중 불꽃이 있는 위치만
                for a in range(len(graph[i][j])): #한 위치에 불꽃이 여러개 있을 수 있음
                    m,s,d = graph[i][j][a]
                    ni,nj = i + s * dx[d], j + s * dy[d]
                    ni,nj = (ni+n)%n , (nj + n)%n #위치를 격자 안으로 이동
                    move[ni][nj].append((m,s,d))
    return move

def check_fire(move):
    for i in range(n):
        for j in range(n):
            if len(move[i][j]) >=2 : #2개 이상이라면
                count = len(move[i][j])
                new_m,new_s,new_d = 0,0,[]
                for b in range(count) :
                    new_m += move[i][j][b][0]
                    new_s += move[i][j][b][1]
                    new_d.append(move[i][j][b][2])

                new_m = new_m//5
                new_s = new_s// count

                move[i][j] = [] #비워주기

                if new_m > 0 :
                #네방향 나누기(0248)
                    if list(map(lambda x : x%2==0,new_d)) ==[True] * count or list(map(lambda x : x%2!=0,new_d)) ==[True] * count :
                        for d in [0,2,4,8] :
                            move[i][j].append((new_m,new_s,d)) #불꽃의 이동과 나누기를 각각 함수로 구성했으므로 불꽃 이동 전 위치로 갱신

                    else :
                        for d in [1,3,5,7]:
                            move[i][j].append((new_m, new_s, d))
    return move #이 함수의 결과를 graph에 갱신


for _ in range(k):
    move = fire_move(graph)
    graph = check_fire(move)

total = 0
for i in range(n):
    for j in range(n):
        if graph[i][j] != []:
            for a in range(len(graph[i][j])) :
                total += graph[i][j][a][0]

print(total)