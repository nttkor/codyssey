
iterarr = []
def permut( plist, others ,n):
    if n== 0:
        iterarr.append(plist)
        return
    for i,v in enumerate(others):
        permut( plist + [v], others[:i]+others[i+1:],n-1)
    return
def main():
    nums = [ v for v in range(10)]
    permut( [],  nums,4)
    
    for v in iterarr:
        print(v)
    return
main()