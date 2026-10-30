import heapq
import math
from itertools import product

def det(P):
    a, b, c, d = P
    return a * d - b * c

def transpose(P):
    a, b, c, d = P
    return (a, c, b, d)

def mul(P, Q, N):
    a, b, c, d = P
    e, f, g, h = Q
    return ((a*e + b*g) % N, (a*f + b*h) % N,
            (c*e + d*g) % N, (c*f + d*h) % N)

def add(P, Q, N):
    a, b, c, d = P
    e, f, g, h = Q
    return ((a+e) % N, (b+f) % N,
            (c+g) % N, (d+h) % N)

def scale(k, P, N):
    a, b, c, d = P
    return ((a*k) % N, (b*k) % N,
            (c*k) % N, (d*k) % N)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

def step(A, B, N):
    AB = mul(A, B, N)
    BA = mul(B, A, N)
    X = add(scale(3, AB, N), scale(19, BA, N), N)
    dA = det(A)
    dB = det(B)
    left = scale(5 * dB, A, N)
    right = scale(-11 * dA, B, N)
    bracket = add(left, right, N)
    Y = mul(transpose(A), mul(B, bracket, N), N)
    if is_prime(abs(det(X))):
        X = add(mul(X, X, N), scale(7, Y, N), N)
    if any(is_prime(e) for e in Y):
        Y = add(mul(Y, mul(transpose(Y), Y, N), N), scale(23, mul(Y, X, N), N), N)
    return X, Y

# (a)

def solve_a(A, B, n, N):
    for i in range(n):
        A, B = step(A, B, N)
    return A, B

# (b)

def value(A, B):
    return (det(A) ** 2 + 1) * (det(B) ** 2 + 1)

def solve_b(A, B, N):
    values = []
    seen = {}
    best = value(A, B)
    best_pair = (A, B)
    k = 0
    while (A, B) not in seen:
        seen[(A, B)] = k
        values.append(value(A, B))
        A, B =  step(A, B, N)
        k += 1
        v = value(A, B)
        if v > best:
            best = v
            best_pair = (A, B)
    start = seen[(A, B)]
    length = k - start
    cyc = []
    C, D  = A, B
    for i in range(length):
        cyc.append((C, D))
        C, D = step(C, D, N)
    i = cyc.index(min(cyc))
    cyc = cyc[i:] + cyc[:i]
    return k, start, length, best, best_pair, values, tuple(cyc)

# (c)

def solve_c(M, N):
    all_values = []
    all_steps = []
    cycles = set()
    for A, B in product(M, repeat=2):
        k, start, length, best, best_pair, values, cyc = solve_b(A, B, N)
        all_values.extend(values)
        all_steps.append(k)
        cycles.add(cyc)
    top_values = heapq.nlargest(25, all_values)
    top_steps = heapq.nlargest(31, all_steps)
    return cycles, top_steps, top_values


def tests():
    assert det((1,2,3,4)) == -2
    assert transpose((1,2,3,4)) == (1, 3, 2, 4)
    assert mul((1,2,3,4), (5,6,7,8), 100) == (19, 22, 43, 50)
    assert add((1,2,3,4), (5,6,7,8), 10) == (6, 8, 0, 2)
    assert not is_prime(1) and is_prime(2) and not is_prime(9) and is_prime(97)
    assert value((1, 2, 3, 4), (5, 6, 7, 8)) == 25
    cycles, top_steps, top_values = solve_c([(0, 0, 0, 0)], 10)
    assert cycles == {(((0, 0, 0, 0), (0, 0, 0, 0)),)}

    print("All tests passed")

if __name__ == "__main__":
    tests()
    M = []
    N = int(input('N = '))
    A = tuple(int(x) % N for x in input("A = ").split())
    B = tuple(int(x) % N for x in input("B = ").split())
    n = int(input("n = "))
    m = int(input("кількість матриць у M = "))
    for i in range(m):
        M.append(tuple(int(x) % N for x in input(f"M[{i}] = ").split()))
    # (a)
    Xn, Yn = solve_a(A, B, n, N)
    print(f"\n(a) a_{n} = ({Xn}, {Yn})")

    # (b)
    k, start, length, best, best_pair, values, cyc = solve_b(A, B, N)
    print(f"\n(b) кроків до повтору: {k}")
    print(f"    цикл починається з кроку {start}, довжина циклу {length}")
    print(f"    цикл: {cyc}")
    print(f"    найбільший value = {best} на парі {best_pair}")

    # (c)
    cycles, top_steps, top_values = solve_c(M, N)
    print(f"\n(c) унікальних циклів: {len(cycles)}")
    for c in cycles:
        print(f"    {c}")
    print(f"    25 найбільших value: {top_values}")
    print(f"    31 найбільша кількість кроків: {top_steps}")