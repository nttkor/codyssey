def fill_2XN(n):
    dp = [0]*(n+1)
    dp[0] = 1
    dp[1] = 1
    _sum = 0
    for  i in range(2,n+1):
        dp[i] = dp[i-1] + 2*dp[i-2]
    return dp[n]
print(fill_2XN(8))
memo={}
def dfs(i):
    if i==0:
        return 1
    if i<0:
        return 0
    if i in memo:
        return memo[i]
    memo[i] = dfs(i-1)+2*dfs(i-2)
    return memo[i]
print(dfs(8))