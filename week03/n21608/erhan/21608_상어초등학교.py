##로직
- 시뮬레이션 문제
-1단계 : 모든 빈칸 중 좋아하는 학생이 많은 자리)
-2단계 :2개 이상일 경우 주변에 빈칸이 많은 칸 찾기
-3단계 : 남은 것 중 행 열이 적은것 찾아서 넣기

##쟁점
- 제약 조건이 많기때문에 코드에 실수가 없도록 작성함


n = int(input())
students = []
for _ in range(n**2):
    students.append(list(map(int,input().split())))


#space : 남은 빈칸
#num : 자리를 정하는 학생
#반환 : 갈수있는 자리에 들어가기(graph) + 빈칸에서 제외하기(space)


##학생 자리 찾는 함수
def search_space(num,space):
    if len(space) == 1 :
        graph[space[0][0]][space[0][1]] = num
        return # 끝내기
    result = []
    #모든 빈칸 중 좋아하는 학생이 주변에 가장 많은 자리 찾기
    for x,y in space : # 빈칸 중
        count = 0
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= n or ny <0 or ny >= n : continue
            if graph[nx][ny] in dic[num] : # 선호학생이 있으면 그 빈칸
                count += 1
        if result == [] : #처음 뽑힌 빈칸은 무조건 포함
            max_count = count
            result.append([x,y])
        elif count > max_count : #더 큰게 나오면 다뺴고 그 빈칸만 추가
            max_count = count
            result =[[x,y]]
        elif count == max_count : # 똑같으면 그냥 추가만
            result.append([x,y])
    if len(result) == 1 : #조건 만족하는게 하나라면
        x,y= result[0]
        graph[x][y] = num  #그자리에 앉힘
        space.remove([x,y]) #빈칸에서 제거
        return

    #2개 이상일 경우 주변에 빈칸이 많은 칸 찾기
    temp = []
    max_count = 0
    for x,y in result :
        count = 0
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
            if graph[nx][ny] == 0  :
                count += 1
        if count == max_count :
            temp.append([x,y])
        elif count > max_count:
            max_count = count
            temp = [[x,y]]
    result = temp

    if len(result) == 1:  # 조건 만족하는게 하나라면
        x, y = result[0]
        graph[x][y] = num  # 그자리에 앉힘
        space.remove([x,y])  # 빈칸에서 제거
        return
    #남은 것 중 행 열이 적은것 찾아서 넣기
    result.sort()
    x,y = result[0]
    graph[x][y] = num
    space.remove([x,y])
    return

def score(x,y):
    count = 0
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if nx < 0 or nx >= n or ny < 0 or ny >= n: continue
        if graph[nx][ny] in dic[graph[x][y]] :
            count += 1
    if count == 0 : return 0
    if count == 1 : return 1
    if count == 2 : return 10
    if count == 3 : return 100
    if count == 4 : return 1000

#학생선호도
dic = {x[0]:[x[1],x[2],x[3],x[4]] for x in students}

#자리
graph = [[0]*n for _ in range(n)]

#빈칸
space =[]
for i in range(n):
    for j in range(n):
        space.append([i,j])

dx =[-1,1,0,0]
dy =[0,0,1,-1]

stu = [x[0] for x in students]
for num in stu:
    search_space(num,space)

value = 0
for x in range(n):
    for y in range(n):
        value += score(x,y)

print(value)

