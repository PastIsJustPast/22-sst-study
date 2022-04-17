'''
pypy3
118664kb
396ms
'''
'''
로직 
- 시뮬레이션
- 경계를 만들고 구역을 나눈 후 인구 수를 더하는 것 보다 구역안에 인구수를 바로 더하는게 편함

'''


n = int(input())
#graph = [list(map(int,input().split())) for _ in range(n)]
graph = []
for info in input().split("\n") :
    graph.append(list(map(int,info.split())))

total = sum(map(sum, graph)) #총인구수
min_people = 1e9
'''
인구차이의 최소값 찾는 함수
input : x0,y0 = 기준점, d1,d2
인구차이 최소를 갱신

기준점이 주어질 때 가능한 d1,d2를 찾는 check함수의 결과를 반영한다
경계선을 생각하고 나누기보다는 1,2,3,4 구역안에 들어오는 인구수를 계산하는 것이 빠름 
어느 칸이 어느 구역인지 찾고 인구수를 탐색해서 찾는 것은 비효율적
'''

def calcultate(x0,y0, d1,d2) :
    global total, min_people
    one,two,three,four = 0,0,0,0

    #구역 1
    y1  = y0 +1
    for x in range(x0 + d1):
        if x >= x0 :
            y1 -= 1
        one += sum(graph[x][:y1])

    #구역 2
    y2 = y0 + 1
    for x in range(x0 + d2 + 1) :
        if x > x0 :
            y2 += 1
        two += sum(graph[x][y2:])

    #구역 3
    y3 = y0 - d1
    for x in range(x0 + d1 , n ):
        three += sum(graph[x][:y3])
        if x < x0 +d1+d2 :
            y3 += 1

    #구역 4
    y4 = (y0 + d2) - n
    for x in range(x0 + d2 + 1 , n ):
        four += sum(graph[x][y4:])
        if x <= x0 + d1 + d2 :
            y4 -= 1

    #구역 5
    five = total - one - two - three - four

    min_people = min(min_people, (max(one,two,three,four,five) - min(one,two,three,four,five )))


'''d1,d2를 찾는 함수
기준점과 d1d2를 입력하면 계산가능한지 탐색하는 함수
'''
def search_d12(x0,y0,d1,d2):
    if 0 <= x0 + d1 -1 < n and 0 <= x0 + d2 -1 and 0 <= y0 - d1 + d2 -1 < n :
        if 0 <= y0 - d1 and y0 + d2 < n and x0 + d1+d2 < n :
            return True
    return False


for x0 in range(n-2):
    for y0 in range(1,n-1):
        for d1 in range(1,n-1):
            for d2 in range(1,n-1):
                if search_d12(x0,y0,d1,d2) == True :
                    calcultate(x0,y0,d1,d2)

print(min_people)