'''
43퍼에서 시간초과
'''

'''
배운점 : 
- 작은 값을 추출할 때 힙큐를 반복적으로 사용하는 것 보다 sort후 순서대로 출력하는게 더 빠름
- 제한시간 짧고, 삭제 후 추가가 많은 문제에서는 정렬을 최소화 하는 것이 관건.
- pop과 슬라이싱 활용하면 더 빠름
'''



n,m,k = map(int,input().split())

food = [list(map(int,input().split())) for _ in range(n)]

trees = []
for _ in range(m):
    _x, _y, _z = map(int, input().split())
    _x, _y = _x - 1, _y - 1
    trees.append((_z,_x,_y))




'''봄 여름 가을 겨울
input :  
참조 : 나무, 현재 양분, 
output : 변경 후 나무 및 양분
'''
direc = [(0,1),(0,-1),(1,1),(1,-1),(1,0),(-1,0),(-1,1),(-1,-1)]
def ssfw():
    global maps, trees
    if trees == [] :
        return #나무가 모두 죽었다면 조기 종료
    '''봄'''
    #양분먹이고, 부족하면 제거
    temp=[]
    die = []
    growth = [] #증식할 나무
    for i in range(len(trees)) :
        z,x,y = trees[i]
        if maps[x][y] >= z : #양분을 먹을 수 있으면
            maps[x][y] -= z
            z += 1
            temp.append((z,x,y))
            if z % 5 == 0 :
                growth.append((z,x,y))
        else :
            die.append((z,x,y))

    trees = [x for x in temp]
    '''여름'''    #양분 및 나무 초기화
    if die != []:
        for z,x,y in die:
            if z >= 2:
                maps[x][y] += z//2

    '''가을'''
    if growth != []:
        new_trees = []
        for z, x, y in growth:
            for dx, dy in direc:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
                new_trees.append((1,nx,ny))
        trees = new_trees + trees

    '''겨울'''
    maps = [[maps[i][j] + food[i][j] for j in range(n)] for i in range(n)]

trees.sort()

maps = [[5 for _ in range(n)] for _ in range(n)] #잔여 양분
for _ in range(k):
    if trees == [] :
        break
    ssfw()
print(len(trees))