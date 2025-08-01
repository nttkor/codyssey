def solution(rows, columns, queries):
    table = [[y+columns*x+1 for y in range(columns)] for x in range(rows)]

    def clockwise(x1,y1,x2,y2):
        arr1 = [(x1,y) for y in range(y1,y2)]
        arr2 = [(x,y2) for x in range(x1,x2)]
        arr3 = [(x2,y) for y in range(y2,y1,-1) ] 
        arr4 = [(x,y1) for x in range(x2,x1,-1) ]
        return arr1+arr2+arr3+arr4

    # for li in table:
    #     for v in li:
    #         print(f'{v:2} ',end='')
    #     print()
    # print()
    answer = []
    for li in queries:
        x1,y1,x2,y2 = li
        x1,y1,x2,y2 = x1-1,y1-1,x2-1,y2-1
        arr = clockwise(x1,y1,x2,y2)
        varr = [ table[x][y] for x,y in arr]
        answer.append(min(varr))
        rot = arr[1:]+[arr[0]]
        tem = table[arr[0][0]][arr[0][1]]
        for (x1,y1), (x2,y2) in zip(arr[::-1], rot[::-1]):
            table[x2][y2] = table[x1][y1]
        table[rot[0][0]][rot[0][1]] = tem
        # for li in table:
        #     for v in li:
        #         print(f'{v:2} ',end='')
        #     print()
        # print()  
    return answer
q=[[2,2,5,4],[3,3,6,6],[5,1,6,3]]
answer = solution(6,6,q)
print(answer)