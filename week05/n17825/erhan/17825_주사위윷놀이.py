'''
pypy
123,164kb
1,368 ms
'''

'''<풀이 방법>
-계산시간보다는 예외처리에 중점을 맞춤 <-> 4^10 탐색이 반드시 필요하기 떄문에 어차피 오래걸림

-백트래킹 + 시뮬레이션

-말 네개를 (0~3번)을 10회에 걸쳐 뽑는 (중복순열) 모든 경우의 수에 대해 말 이동 + 점수를 계산

- 말 이동함수 , 점수계산 함수, 백트래킹 함수를 구현함

-점수를 계산하는 과정에서 말의 위치가 중복되는 조합을 제외

 => 백트래킹 과정에서 처음부터 말의 위치가 중복되는 조합을 제거할 수 있지만, 
     백트래킹 과정에서 말 이동 과정을 또 수행해야하므로 계산이 더 오래걸림
     
- 즉, 모든 경우의수 + 말 이동 + 점수계산 vs (말이동 + 말 위치가 중복 되지 않는 모든 경우의 수 ) + 말 이동 + 점수계산 
'''


'''<쟁점>
- 윷놀이판과 이동을 어떻게 정의하는지가 이 문제의 핵심
 => 딕셔너리로 윷놀이판 정의 
 
- 외각에서 40점과 25분기점에서 40점을 하나의 점으로 만들어서 말 위치가 겹치지 않도록 수행할 필요

- 이동 방식, 점수 계산에 대한 분기가 매우 다양함
'''

'''개선사항
- 최근에 백트래킹 공부를 했어서 일부러 백트래킹으로 품
- 더 빠른 접근법 존재할 것 같음
- 말 번호에 의미가 없어서 조합 경우의 수를 줄일 수 있을 것 같음
ex) 1,1,1,1,1,1,1,1,1,1와 2,2,2,2,2,2,2,2,2,2,2는 똑같음
ex) 1,1,1,2,2,2,3,3,3,0와 2,2,2,3,3,3,0,0,0,1은 똑같음
'''


'''윷놀이판
말의 위치를 [a][b]로 나타냄
a : 경로 및 분기점 / 외각과 10,20,30,25 분기점
b : 경로 및 분기점에서의 위치
말이 도착지점에 도착하기 위해서는 반드시 25분기점의 40을 지나야함
'''
orders = list(map(int,input().split()))
maps = {} #윷놀이 [a][b]로 표기
maps[0] = list(range(0,42,2))
maps[1] = [10,13,16,19]
maps[2] = [20,22,24]
maps[3] = [30,28,27,26]
maps[4] = [25,30,35,40]


'''주사위에 따라 말 이동
input = 현재 말 위치, 말번호(0~3), 주사위
참조 :말 위치(horses)
ouput = 이동 후 위치

-각 경로 및 분기점에서 위치(b)를 옮긴 후에 도착지점에 따라 경로 및 분기점(a)을 갱신
'''

def move_horse(horses,horse_num,order) :                    #출발위치가 외각 -> 도착위치가 외각                       출발위치가 10,20,30 분기점 -> 도착위치가 10,20,30 분기점
    h_a,h_b =horses[horse_num]                              #             -> 도착위치가 10,20,30 분기점                                     -> 도착위치가 25분기점
    #출발위치가 외곽                                           #             -> 도착위치가 25분기점(40점 짜리 윷놀이칸)                          -> 25분기점을 넘어 도착위치가 도착지점
    if h_a == 0 :                                           #             -> 도착위치가 도착지점
        #도착위치                                             #
        n_a ,n_b = h_a, h_b + order                         #출발위치가 25분기점 -> 도착위치가 25분기점
                                                            #                 -> 도착위치가 도착지점
        # 이동한 위치가 도착지점이라면
        if n_b >= len(maps[n_a]):
            n_a, n_b = -1, -1

        # 이동한 위치가 분기점이라면 좌표수정 필요
        elif maps[0][n_b] == 10  : n_a = 1 ; n_b = 0
        elif maps[0][n_b] == 20 : n_a = 2 ;n_b = 0
        elif maps[0][n_b] == 30 : n_a = 3 ;n_b = 0
        elif maps[0][n_b] == 40 : n_a = 4 ; n_b =  3

    #출발위치가 분기점이라면
    elif h_a in [1,2,3]:
        n_a,n_b = h_a,h_b + order

        #25분기점을 지난다면
        if n_b >= len(maps[n_a]) :
            spare= n_b - len(maps[n_a])
            n_a = 4 ; n_b = spare #25분기점으로 옮겨줌

            if n_b >= len(maps[n_a]) :  #25분기점을 넘어서 도착지점에 도착한다면
                n_a, n_b = -1,-1

    #출발위치기 25분기점이라면
    elif h_a == 4 :

        n_a,n_b = h_a, h_b + order
        if n_b >= len(maps[n_a]) :
            n_a, n_b = -1,-1 #도착 처리

    return (n_a,n_b)

'''점수 합산 함수
주사위 orders와 선택된 말 조합 temp를 활용해 10회 주사위를 모두 던졌을 때 점수를 계산하는 함수

참조 : 백트래킹함수에서 10회동안 4개의 말을 선택한 조합인 temp를 받음
output : 선택된 4개의 말을 10회 움직였을 때 총 점수 합산

- i번째 주사위 값과 말 선택 -> 도착유무 확인 -> 말의 다음위치 탐색 + 말 위치 중복 확인 -> 이동   
- 만약 말의 위치가 겹친다면 그 조합은 이용할 수 없으므로 점수 -1로 계산
- 선택된 말이 이미 도착했다면 최대 스코어를 낼 수 없으므로 점수 -1로 계산
'''

def move_score():
    horses = [(0, 0), (0, 0), (0, 0), (0, 0)]  # 말의 위치, 점수가 아닌 index로 표기함
    total = 0
    for i in range(10):
        horse_num = temp[i]  #i번째 주사위로 움직일 말 번호
        order = orders[i] # i번째 주사위 값

        if horses[horse_num] == (-1,-1) : #이미 통과한 말은 건드리지 않음
            continue

        #말의 다음 위치
        a,b  = move_horse(horses,horse_num, order)
        if (a,b) == (-1,-1) : #만약 이미 도착한 말이라면 점수 추가 없음
            horses[horse_num] = (a,b)
            continue
        elif (a,b) in horses : return - 1 # 만약 이동할 위치에 다른 말이 있다면 바로 종료 후 -1점

        #이동
        total += maps[a][b] #점수합산
        horses[horse_num] = (a,b) #위치 갱신
        #print((a, b), "말:",horse_num, "주사위:",order,"도착칸:", maps[a][b], total)
    return total

'''
4개의 말 중 1개를 선택하는 함수
input = 10회 중 curr_num번째
max_value를 갱신함 
'''

def choose(curr_num):
    global max_value

    '''정지조건'''
    if curr_num == 11 :
        now_value = move_score() #점수 합산
        #if now_value > max_value : print(temp,now_value)
        max_value = max(now_value,max_value)
        return

    '''이동할 말 결정'''
    for horse_num in range(4) : #말 번호 0 ~ 3
        temp.append(horse_num)
        choose(curr_num + 1 )
        temp.pop()
    return

temp = []
max_value = 0
choose(1)
print(max_value)

orders
