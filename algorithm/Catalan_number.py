def solve(n):
    if n== 1:
        return 1
    dp = [0]*(n+1)
    dp[0]=1
    for i in range(1,n+1):
        for j in range(i):
            dp[i] += dp[j]*dp[i-j-1]
    return dp[n]

print(solve(3))
print(solve(20))
memo={}
def dfs(n):
    global memo
    if n== 0 :
        return 1
    # if n in memo:
    #     return memo[n]
    result = 0
    for i in range(n):
        result += dfs(i)*dfs(n-i-1)
    # memo[n] = result
    return result
print(dfs)
print(3,dfs(3))
print(6, dfs(20))