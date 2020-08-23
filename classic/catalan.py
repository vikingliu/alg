# coding=utf-8


def catalan_cnt(n):
    """
        令h(0)=1,h(1)=1，catalan数满足递推式：h(n)= h(0)*h(n-1)+h(1)*h(n-2) + ... +h(n-1)*h(0) (n>=2)

        另类递推式[2]：h(n)=h(n-1)*(4*n-2)/(n+1);

        递推关系的解为：h(n)=C(2n,n)/(n+1) (n=0,1,2,...)

        递推关系的另类解为：h(n)=c(2n,n)-c(2n,n-1)(n=0,1,2,...)

        C(2n, n) / (n+1) = 2n!/(n!*n!*(n+1))
    """
    if n == 1:
        return 1
    n_factorial = 1
    for i in xrange(1, n + 1):
        n_factorial *= i
    n2_factorial = n_factorial
    for i in xrange(n + 1, 2 * n + 1):
        n2_factorial *= i

    return n2_factorial / (n_factorial * n_factorial * (n + 1))


def bracket_dfs(n, left=0, right=0, path=''):
    if left == n and right == n:
        print path
        return

    if left < n:
        bracket_dfs(n, left + 1, right, path + '(')

    if left > right:
        bracket_dfs(n, left, right + 1, path + ')')


print bracket_dfs(3)
# bracket_dfs(3)
