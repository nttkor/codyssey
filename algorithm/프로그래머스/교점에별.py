def solution(line):
    answer = []
    gyojum = set()
    for i1,f1 in enumerate(line):
        other = line[:i1] + line[i1+1:]
        for i2,f2 in enumerate(other):
            A, B, E = f1
            C, D, F = f2
            mother = A*D - B*C # AD - BC
            if mother == 0:
                continue
            # 올바른 교점 공식 적용
            son1 = B*F - E*D  # BF - ED
            son2 = E*C - A*F  # EC - AF
            xp = son1 / mother
            yp = son2 / mother
            if float.is_integer(xp) and float.is_integer(yp):
                # print(f'integer:{xp},{yp}')
                gyojum.add((int(xp),int(yp)))
            # else:
            #     print(f'float:{xp},{yp}')
    minx = min(gyojum, key=lambda p:p[0])[0]
    maxx = max(gyojum, key=lambda p:p[0])[0]
    miny = min(gyojum, key=lambda p:p[1])[1]
    maxy = max(gyojum, key=lambda p:p[1])[1]
    # print(gyojum)
    for dy in range(maxy, miny-1,-1):
        row = ''
        for dx in range(minx, maxx + 1):
            if (dx,dy) in gyojum:
                row += '*'
            else:
                row += '.'
        answer.append(row)
    return answer

lines = [[2, -1, 4], [-2, -1, 4], [0, -1, 1], [5, -8, -12], [5, 8, 12]]
#lines = [[0, 1, -1], [1, 0, -1], [1, 0, 1]]
result = solution(lines)
print("\n최종 결과:")
for line in result:
    print(f'"{line}"')