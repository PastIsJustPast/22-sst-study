'''
python3    pypy3
32484kb    118956kb
472ms       252ms
'''

from collections import deque

n,m = map(int,input().split())
#graph = [list(map(int,input().split())) for _ in range(n)]
graph = []
for info in input().split("\n"):
    graph.append(list(map(int,info.split())))

home = []
bbq = []
for i in range(n):
    for j in range(n):
        if graph[i][j] == 1 :
            home.append((i,j))
        elif graph[i][j] == 2 :
            bbq.append((i,j))

'''
치킨 거리 구하기

input : 집 위치, temp(전체 치킨집중 활성화된 m개)
'''
def dist_bbq(home,temp) :
    total_dist = 0
    on_bbq = []
    for i in range(len(temp)) :
        if temp[i] == 1 :
            on_bbq.append(bbq[i])

    for hx,hy in home :
        dist  = 1e9
        for cx,cy in on_bbq :
            dist = min(abs(hx - cx) + abs(hy-cy) , dist)

        total_dist += dist

    return total_dist



'''
치킨집 중 m개 고르기
'''
min_dist = 1e9
temp = []
def choose(curr_num , cnt ) :
    global min_dist
    if curr_num == len(bbq) + 1 :
        if cnt == m :
            min_dist = min(min_dist ,  dist_bbq(home,temp) )
        return

    temp.append(1)
    choose(curr_num + 1 , cnt +1 )
    temp.pop()

    temp.append(0)
    choose(curr_num + 1, cnt)
    temp.pop()

    return


choose(1,0)
print(min_dist)