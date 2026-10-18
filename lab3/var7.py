import numpy as np

eps = 1e-8
def solve(A, b, x0, eps, max_iter=10000):
    n = len(b)
    if A.shape != (n, n):
        raise ValueError(f"A має бути {n}x{n}, а вона {A.shape}")
    if len(x0) != n:
        raise ValueError(f"x0 має мати {n} елементів, а має {len(x0)}")
    M = A + np.eye(n)
    x = x0.copy()
    for i in range(max_iter):
        x_new = M @ x - b
        if np.linalg.norm(x_new - x) < eps:
            return x_new, i + 1
        x = x_new
    return x, max_iter

A = np.array([[-1, 0.5], [0.5, -1]])
b = np.array([1, 1])
x0 = np.zeros(2)
x, steps = solve(A, b, x0, eps)
x_exact = np.linalg.solve(A, b)
x_diff = x_exact - x
print(x, steps)
print(np.linalg.norm(x_diff))


if np.linalg.norm(x_diff) < eps:
    print('Збіглось з точністю eps')
else:
    print('Не збіглось з точністю eps')
if np.allclose(x_exact, x, rtol=0, atol=eps):
    print('Збіглось з точністю eps')
else:
    print('Не збіглось з точністю eps')


