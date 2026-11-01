calls = 0
depth = 0
calls_simple = 0
depth_simple = 0
max_depth = 0
memo = {}

def fib(n):
    global calls
    global depth
    global max_depth
    calls += 1
    depth += 1
    if depth > max_depth:
        max_depth = depth
    if n == 1 or n ==2:
        depth -= 1
        return 1
    res = fib(n - 1) + fib(n - 2)
    depth -= 1
    return res

def fib_memo(n):
    global calls
    global depth
    global max_depth
    calls += 1
    depth += 1
    if depth > max_depth:
        max_depth = depth
    if n in memo:
        depth -= 1
        return memo[n]
    if n == 1 or n ==2:
        depth -= 1
        return 1
    res = fib_memo(n - 1) + fib_memo(n - 2)
    memo[n] = res
    depth -= 1
    return res

print(f'{"n":>3} | {"fib(n)":>7} | {"викл. проста":>12} | {"викл. memo":>12} | {"глиб. проста":>12} | {"глиб. memo":>12}')
print("-" * 73)
for n in range(1, 31):
    result = fib(n)

    calls_simple = calls
    depth_simple = max_depth

    calls = 0
    depth = 0
    max_depth = 0
    memo = {}

    result_memo = fib_memo(n)
    assert result == result_memo

    print(f"{n:>3} | {result:>7} | {calls_simple:>12} | {calls:>12} | {depth_simple:>12} | {max_depth:>12}")

    calls = 0
    depth = 0
    max_depth = 0
    memo = {}