# Завдання 3, варіант 2. Виконано в режимі повного використання ШІ (п.18d).
#
# Кінетична енергія стовпа атмосфери одиничної площі:
#     E(a, b) = ∫_a^b  ½ · rho(h) · v(h)^2  dh
# Функції v(h) і rho(h) вводяться як вирази Python від h (доступні функції з math).
# Точність eps: інтеграл рахується складеною формулою Сімпсона з подвоєнням
# кількості відрізків, поки |S_2n - S_n| / 15 >= eps (оцінка Рунге).

import math
import statistics
import time
from bisect import bisect_left


def make_func(expr):
    env = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    code = compile(expr, "<expr>", "eval")
    return lambda h: eval(code, {"__builtins__": {}}, {**env, "h": h})


def energy_density(v, rho):
    return lambda h: 0.5 * rho(h) * v(h) ** 2


def simpson(f, a, b, n):
    """Складена формула Сімпсона, n — парне."""
    hstep = (b - a) / n
    s = f(a) + f(b)
    s += 4 * sum(f(a + i * hstep) for i in range(1, n, 2))
    s += 2 * sum(f(a + i * hstep) for i in range(2, n, 2))
    return s * hstep / 3


def integrate(f, a, b, eps):
    """Повертає (інтеграл, n) з точністю eps за оцінкою Рунге."""
    n = 2
    prev = simpson(f, a, b, n)
    while True:
        n *= 2
        cur = simpson(f, a, b, n)
        if abs(cur - prev) / 15 < eps or n > 2 ** 22:
            return cur, n
        prev = cur


# ---------- (a) ----------

def solve_a(f, a, b, eps):
    return integrate(f, a, b, eps)[0]


# ---------- (b) ----------

def solve_b(f, a, b, w, eps):
    """Межі s_1..s_{k-1}, щоб енергії шарів відносились як w_1 : ... : w_k.

    Ефективність: замість окремого інтеграла для кожної межі (k бісекцій по
    повному інтегралу) будуємо один раз накопичувальну таблицю інтегралів на
    сітці з n відрізків (n — з integrate), бінарним пошуком знаходимо комірку,
    де лежить s_i, і лише всередині неї уточнюємо s_i бісекцією.
    Складність: O(n + k·log(1/eps)) обчислень f замість O(k·n·log(1/eps)).
    """
    if not (0 < len(w) <= 1000) or any(x <= 0 for x in w):
        raise ValueError("потрібно 1..1000 ваг w_i > 0")
    total, n = integrate(f, a, b, eps)
    hstep = (b - a) / n
    xs = [a + i * hstep for i in range(n + 1)]
    cum = [0.0]
    for i in range(n):                      # Сімпсон на кожній комірці
        x0, x1 = xs[i], xs[i + 1]
        cum.append(cum[-1] + (x1 - x0) / 6 * (f(x0) + 4 * f((x0 + x1) / 2) + f(x1)))

    W = sum(w)
    cuts, acc = [], 0.0
    for wi in w[:-1]:
        acc += wi
        target = total * acc / W
        j = min(max(bisect_left(cum, target) - 1, 0), n - 1)
        lo, hi = xs[j], xs[j + 1]
        base = cum[j]
        while hi - lo > eps * max(1.0, abs(b - a)):
            mid = (lo + hi) / 2
            part = (mid - xs[j]) / 6 * (f(xs[j]) + 4 * f((xs[j] + mid) / 2) + f(mid))
            if base + part < target:
                lo = mid
            else:
                hi = mid
        cuts.append((lo + hi) / 2)
    return cuts, total


# ---------- (c) ----------

def timing(f, a, b, w, eps_list, repeats=10):
    rows = []
    for eps in eps_list:
        ta, tb = [], []
        for _ in range(repeats):
            t0 = time.perf_counter()
            solve_a(f, a, b, eps)
            ta.append(time.perf_counter() - t0)
            t0 = time.perf_counter()
            solve_b(f, a, b, w, eps)
            tb.append(time.perf_counter() - t0)
        rows.append((eps, statistics.mean(ta), min(ta), statistics.mean(tb), min(tb)))
    return rows


# ---------- тести ----------

def tests():
    f = lambda h: 1.0                                   # ∫_0^10 1 dh = 10
    assert abs(solve_a(f, 0, 10, 1e-9) - 10) < 1e-9
    g = lambda h: h * h                                 # ∫_0^3 h^2 dh = 9
    assert abs(solve_a(g, 0, 3, 1e-9) - 9) < 1e-9
    cuts, _ = solve_b(f, 0, 10, [1, 1], 1e-9)           # стала густина — навпіл
    assert abs(cuts[0] - 5) < 1e-6
    cuts, _ = solve_b(f, 0, 10, [1, 2, 2], 1e-9)        # 2 : 4 : 4
    assert abs(cuts[0] - 2) < 1e-6 and abs(cuts[1] - 6) < 1e-6
    print("All tests passed")


# ---------- ввід / вивід ----------

def ask(prompt, default):
    s = input(f"{prompt} [{default}] = ").strip()
    return s if s else default


if __name__ == "__main__":
    tests()
    v = make_func(ask("v(h)", "10 + 0.002*h"))
    rho = make_func(ask("rho(h)", "1.225*exp(-h/8500)"))
    f = energy_density(v, rho)
    a = float(ask("a", "0"))
    b = float(ask("b", "10000"))
    eps = float(ask("eps", "1e-6"))

    # (a)
    E = solve_a(f, a, b, eps)
    print(f"\n(a) E = {E:.10g}")

    # (b)
    w = [float(x) for x in ask("w (через пробіл)", "1 2 3").split()]
    cuts, total = solve_b(f, a, b, w, eps)
    print(f"\n(b) межі s_i: {[round(s, 6) for s in cuts]}")
    bounds = [a] + cuts + [b]
    parts = [solve_a(f, bounds[i], bounds[i + 1], eps) for i in range(len(w))]
    print("  перевірка — частки енергії / частки ваг:")
    for p, wi in zip(parts, w):
        print(f"    {p / total:.6f} / {wi / sum(w):.6f}")

    # (c)
    eps_list = [10.0 ** -k for k in range(2, 11, 2)]
    print("\n(c) eps        (a) mean     (a) min      (b) mean     (b) min   [с]")
    for eps_i, ma, mia, mb, mib in timing(f, a, b, w, eps_list):
        print(f"    {eps_i:<9.0e}  {ma:.3e}    {mia:.3e}    {mb:.3e}    {mib:.3e}")