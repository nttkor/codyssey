import math
print(math.gcd(8,12))
print(math.lcm(8,12))
print(abs(8*12)//math.gcd(8,12))
def mygcd(a,b):
    while b:
        a,b = b, a%b