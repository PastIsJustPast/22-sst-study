'''
python 3 pypy3
31156kb 116004kb
100ms   196ms
'''


'''
로직
-sort, transpose로 구성
- collections의 counter함수를 직접 구현해서 0을 제외하고 출력
- c배열 연산은 t -> r -> c

배운점
- collecntions의 counter함수는 배열 내 동일한 값 세서 출력
- list(dic.item())를 정렬하여 value에 따라 정렬할 수 있음


'''

from copy import deepcopy
r,c,k = map(int,input().split())
graph = [list(map(int,input().split())) for _ in range(3)]
'''
graph= []
for info in input().split("\n") :
    graph.append(list(map(int,info.split())))
'''
def sooort(lst):
    dic = {}
    for i in lst:
        if i == 0 : continue
        if i not in dic:
            dic[i] = 1
        else :
            dic[i] += 1
    return dic



def RorC(arr):
    row = len(arr)
    col = len(arr[0])
    if row >= col : return True #r연산
    else : return False

def R(arr):
    max_len = 0
    temp = []
    #모든 행에 대해 정렬
    for row in arr :
        nrow = []
        for i,j in sorted(list(sooort(row).items()), key = lambda x: (x[1],x[0])):
            nrow.append(i)
            nrow.append(j)
        if len(nrow) > max_len : max_len = len(nrow) #최대길이 갱신
        temp.append(nrow)

    #부족한 값 채우기
    arr = []
    if max_len < 3 : max_len = 3 #3보다 작으면 키움
    for row in temp :
        row = row + [0] * (max_len - len(row))
        if len(row) >= 101 : row = row[:100] #100보다 크면 자름
        arr.append(row)

    return arr


def C(arr):
    arr = list(map(list,zip(*arr)))
    arr = R(arr)
    arr = list(map(list,zip(*arr)))
    return arr

answer = -1
arr = deepcopy(graph)

#인덱스 밖에 있으면 그냥 넘겨야함
def in_box(arr):
    if r <= 0 or r > len(arr) or c <= 0 or c > len(arr[0]):  # 인덱스가 밖이면
        return False
    return True

if in_box(arr) and arr[r-1][c-1] == k : #찾으려는게 arr안이고 그 값이 맞다면
    answer = 0
else :
    for t in range(1, 101):
        if RorC(arr):
            arr = R(arr)
        else:
            arr = C(arr)

        if in_box(arr)  and arr[r - 1][c - 1] == k:
            answer = t
            break
print(answer)