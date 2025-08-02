def solution(n):
    if n == 1:
        return [1]
    answer = []
    table = [[0] * (i+1)  for i in range(n)]
    cx = 0
    cy = 0
    offset = 1
    li = list()
    while n > 1:
        li.extend([(cx, cy+i) for i in range(n-1)])
        cy += n-1
        li.extend([(cx+i, cy) for i in range(n-1)]) 
        cx += n-1
        li.extend([(cx-i, cy-i) for i in range(n-1)])
        # cx = li[-1][0]; cy = li[-1][1]+1
        cx -= n-2; cy -= n-3
        n -= 3
        if n == 1:
            li.append((cx,cy))
            n -= 1
    cnt = 1
    for x,y in li:
        table[y][x] = cnt
        cnt += 1
    for li in table:
        answer += li
    return answer


ans = solution(1)
print(ans)