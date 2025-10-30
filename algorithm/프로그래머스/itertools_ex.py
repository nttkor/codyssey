from itertools import product
def transpose(matrix):
    z = zip(*matrix)
    #print(*z)
    lz = [list(t) for t in z]
    #print(lz)
    return lz
    
matrix3by3 = [ [i+j*3 for i in range(3)]  for j in range(3)]
print(matrix3by3)
mat_transpose = transpose(matrix3by3)
print(mat_transpose)
maxval,prod = 0,[]
for pd in product(*mat_transpose):
    s = sum(pd)
    if maxval < s:
        maxval = s
        prod = pd
print(s,pd)
        
    
    