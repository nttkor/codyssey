def permu(line):
    answer = 0
    for i1, v1 in enumerate(line):
        line2 = [ t for t in line if t != v1 ]
        for i2, v2 in enumerate(line2):
            line3 = [ t for t in line2 if t != v2 ]
            for i3, v3 in enumerate(line3): 
                print(f'{i1}:{v2}, {i2}:{v2}, {i3}:{v3}')
    return answer
    
    
def main():
    line = [[2, -1, 4], [-2, -1, 4], [0, -1, 1], [5, -8, -12], [5, 8, 12]]
    permu(line)
main()