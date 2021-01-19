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
    for i in range(1, n + 1):
        n_factorial *= i
    n2_factorial = n_factorial
    for i in range(n + 1, 2 * n + 1):
        n2_factorial *= i

    return n2_factorial / (n_factorial * n_factorial * (n + 1))


def bracket_dfs(n, left=0, right=0, path=''):
    if left == n and right == n:
        return [path]
    res = []
    if left < n:
        res += bracket_dfs(n, left + 1, right, path + '(')

    if left > right:
        res += bracket_dfs(n, left, right + 1, path + ')')
    return res


def bracket_dfs_1(n, used=0, left=0, path=''):
    if left == 0 and n == used:
        return [path]
    res = []
    if left > 0:
        res += bracket_dfs_1(n, used, left - 1, path + ')')
    if n > used:
        res += bracket_dfs_1(n, used + 1, left + 1, path + '(')
    return res


def bracket_dfs_2(n):
    brackets = [('', 0, 0)]
    for i in range(n * 2):
        for j, bracket in enumerate(brackets):
            s, left, right = bracket
            modify = False
            if left < n:
                modify = True
                brackets[j] = (s + '(', left + 1, right)
            if right < left:
                new_bracket = (s + ')', left, right + 1)
                if modify:
                    brackets.append(new_bracket)
                else:
                    brackets[j] = new_bracket
    return [b[0] for b in brackets]


def bracket_dfs_3(n, stack=0, res=''):
    if n == 0:
        x = stack
        res += '(' * x + ')' * x
        print(res)
        return

    if n > 0:
        # 入栈
        bracket_dfs_3(n - 1, stack + 1, res)

    out = ''
    while stack > 0:
        # 出栈
        stack -= 1
        out = '(' + out + ')'
        bracket_dfs_3(n - 1, stack + 1, res + out)


def bracket_dfs_4(left_remain, left_stack=0, res=''):
    if left_remain == 0:
        print(res + ')' * left_stack)
        return
    # ( 入栈
    bracket_dfs_4(left_remain - 1, left_stack + 1, res + '(')
    if left_stack > 0:
        # ( 出栈 + ）
        bracket_dfs_4(left_remain, left_stack - 1, res + ')')


def stack_out(arr, start=0, stack=[], path=[]):
    if start == len(arr):
        path = path + stack[::-1]
        return [path]
    else:
        res = []
        # 入栈
        res += stack_out(arr, start + 1, stack + [arr[start]], path)
        pop = []
        # 出栈在入栈
        while stack:
            pop.append(stack.pop())
            res += stack_out(arr, start + 1, stack + [arr[start]], path + pop)
        return res


def stack_out_1(arr):
    results = [([], [])]
    for i in range(len(arr)):
        new_results = []
        for stack, path in results:
            new_results.append((stack + [arr[i]], path))
            pop = []
            while stack:
                pop.append(stack.pop())
                new_results.append((stack + [arr[i]], path + pop))
        results = new_results
    res = [path + stack[::-1] for stack, path in results]
    return res


cache = {}


def print_n_pair(n):
    if n == 0:
        return ['']
    if n == 1:
        return ['()']
    if n in cache:
        return cache[n]
    res = []
    for i in range(1, n + 1):
        left = print_n_pair(i - 1)
        right = print_n_pair(n - i)
        for l in left:
            for r in right:
                res.append('(' + l + ')' + r)
    if n not in cache:
        cache[n] = res
    return res


print(print_n_pair(4))

# print(bracket_dfs(3))
# print('------')
# print(bracket_dfs_1(3))
# print('------')
# print(bracket_dfs_2(3))
# print('------')
# print(stack_out([1, 2, 3]))
# print('------')
# print(stack_out_1([1, 2, 3]))

# bracket_dfs_3(3)
bracket_dfs_4(4)
