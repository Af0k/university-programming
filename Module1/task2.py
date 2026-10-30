# Завдання 2, варіант 2. Виконано в режимі повного використання ШІ (п.18d).
#
# Інтерпретації (див. також відповіді викладача в teacher_qa.txt):
# - Послідовність починається з початкових A, B, C; кожен крок додає D, E, F, G, H.
# - E при колінеарних A, B, D: середнє в полярних координатах —
#   r = середнє геометричне, кут = циркулярне середнє atan2(mean sin, mean cos);
#   якщо хоча б одна точка має r = 0 — середнє арифметичне в декартових координатах.
# - D при A == C (пряма AC не визначена): центральна симетрія відносно A.
# - "кількість кроків більша за M": виконується не більше M кроків.
# - (c): трійки початкових точок — впорядковані, з повтореннями (як пари в завд. 1);
#   "нові точки" — ті, яких ще не було в послідовності.
#   Якщо на одному кроці спрацювало кілька критеріїв, зараховується перший за порядком:
#   "менше 2 нових точок", "площа > A", "кроки > M".

import heapq
import math
from itertools import combinations, product

W = (11, 13, 31, 43, 60)          # ваги для F
ANGLE = 5 * math.pi / 8           # кут повороту для G


# ---------- базова геометрія ----------

def sub(P, Q):
    return (P[0] - Q[0], P[1] - Q[1])


def dist(P, Q):
    return math.hypot(P[0] - Q[0], P[1] - Q[1])


def reflect(P, A, C):
    """Образ P при симетрії відносно прямої AC."""
    dx, dy = sub(C, A)
    L2 = dx * dx + dy * dy
    if L2 == 0:                                   # A == C: центральна симетрія
        return (2 * A[0] - P[0], 2 * A[1] - P[1])
    t = ((P[0] - A[0]) * dx + (P[1] - A[1]) * dy) / L2
    fx, fy = A[0] + t * dx, A[1] + t * dy         # проекція P на пряму
    return (2 * fx - P[0], 2 * fy - P[1])


def polar_mean(pts):
    """Середнє в полярних координатах (див. інтерпретації вгорі)."""
    rs = [math.hypot(x, y) for x, y in pts]
    if any(r == 0 for r in rs):
        n = len(pts)
        return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)
    r = math.exp(sum(math.log(r) for r in rs) / len(rs))
    s = sum(math.sin(math.atan2(y, x)) for x, y in pts) / len(pts)
    c = sum(math.cos(math.atan2(y, x)) for x, y in pts) / len(pts)
    th = math.atan2(s, c)
    return (r * math.cos(th), r * math.sin(th))


def orthocenter(A, B, D):
    """Ортоцентр трикутника ABD; для колінеарних точок — polar_mean."""
    ax, ay = A; bx, by = B; dx, dy = D
    d = 2 * (ax * (by - dy) + bx * (dy - ay) + dx * (ay - by))
    scale = max(dist(A, B), dist(A, D), dist(B, D)) ** 2
    if d == 0 or abs(d) <= 1e-12 * scale:
        return polar_mean([A, B, D])
    a2, b2, d2 = ax * ax + ay * ay, bx * bx + by * by, dx * dx + dy * dy
    ox = (a2 * (by - dy) + b2 * (dy - ay) + d2 * (ay - by)) / d
    oy = (a2 * (dx - bx) + b2 * (ax - dx) + d2 * (bx - ax)) / d
    # H = A + B + D - 2*O (пряма Ейлера)
    return (ax + bx + dx - 2 * ox, ay + by + dy - 2 * oy)


def mass_center(pts, ws):
    s = sum(ws)
    return (sum(w * p[0] for p, w in zip(pts, ws)) / s,
            sum(w * p[1] for p, w in zip(pts, ws)) / s)


def rotate(P, O, ang):
    x, y = sub(P, O)
    c, s = math.cos(ang), math.sin(ang)
    return (O[0] + x * c - y * s, O[1] + x * s + y * c)


# ---------- один крок ----------

def new_points(A, B, C):
    D = reflect(B, A, C)
    E = orthocenter(A, B, D)
    F = mass_center([A, B, C, D, E], W)
    G = rotate(C, E, ANGLE)
    EF, BG = sub(F, E), sub(G, B)
    H = (D[0] + 7 * EF[0] + 19 * BG[0], D[1] + 7 * EF[1] + 19 * BG[1])
    return [D, E, F, G, H]


def choose_next(pts):
    """Правило 7: при рівності — перша в лексикографічному порядку (x, y)."""
    A = min(pts, key=lambda p: (p[0], p[1]))
    B = min(pts, key=lambda p: (-math.hypot(p[0], p[1]), p[0], p[1]))
    C = min(pts, key=lambda p: (-p[1], p[0], p[1]))
    return A, B, C


def finite(pts):
    return all(math.isfinite(x) and math.isfinite(y) for x, y in pts)


# ---------- опукла оболонка ----------

def cross(O, A, B):
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])


def convex_hull(points):
    """Алгоритм Ендрю (monotone chain), O(n log n)."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def area(hull):
    """Формула Гаусса (шнурування)."""
    n = len(hull)
    if n < 3:
        return 0.0
    s = sum(hull[i][0] * hull[(i + 1) % n][1] - hull[(i + 1) % n][0] * hull[i][1]
            for i in range(n))
    return abs(s) / 2


# ---------- (a) ----------

def solve_a(A, B, C, N):
    """Перші N точок послідовності (A, B, C, D1..H1, D2..H2, ...)."""
    seq = [A, B, C]
    while len(seq) < N:
        pts = new_points(A, B, C)
        if not finite(pts):
            print(f"  ! координати переповнились після {len(seq)} точок")
            break
        seq.extend(pts)
        A, B, C = choose_next([A, B, C] + pts)
    return seq[:N]


# ---------- (b) ----------

def solve_b(A, B, C, A_max, M):
    """Кроки, поки площа оболонки <= A_max і кроків < M.
    Оболонка оновлюється інкрементно: hull(всі) = hull(стара оболонка + нові точки)."""
    seq = [A, B, C]
    hull = convex_hull(seq)
    steps, reason = 0, None
    while True:
        pts = new_points(A, B, C)
        if not finite(pts):
            reason = "переповнення координат"
            break
        seq.extend(pts)
        steps += 1
        hull = convex_hull(hull + pts)
        S = area(hull)
        A, B, C = choose_next([A, B, C] + pts)
        if S > A_max:
            reason = "площа > A"
            break
        if steps >= M:
            reason = "кроки > M"
            break
    return seq, steps, area(hull), reason


def extreme_pairs(seq, k_far=37, k_near=25):
    """k_far найдальших і k_near найближчих пар (i, j, відстань)."""
    pairs = ((dist(seq[i], seq[j]), i, j) for i, j in combinations(range(len(seq)), 2))
    far = heapq.nlargest(k_far, pairs)
    pairs = ((dist(seq[i], seq[j]), i, j) for i, j in combinations(range(len(seq)), 2))
    near = heapq.nsmallest(k_near, pairs)
    return far, near


# ---------- (c) ----------

def snap(P, L):
    """Найближча точка з цілими координатами, |x|, |y| <= L - 1."""
    lim = L - 1
    return tuple(max(-lim, min(lim, math.floor(c + 0.5))) for c in P)


def run_c(A, B, C, A_max, M, L):
    seen = {A, B, C}
    hull = convex_hull(list(seen))
    steps = 0
    while True:
        pts = [snap(P, L) for P in new_points(A, B, C)]
        fresh = set(pts) - seen
        seen |= fresh
        steps += 1
        hull = convex_hull(hull + list(fresh))
        A, B, C = choose_next([A, B, C] + pts)
        if len(fresh) < 2:
            return "менше 2 нових точок"
        if area(hull) > A_max:
            return "площа > A"
        if steps >= M:
            return "кроки > M"


def solve_c(A_max, M, L):
    r = range(-(L - 1), L)
    grid = [(x, y) for x in r for y in r]
    counts = {"менше 2 нових точок": 0, "площа > A": 0, "кроки > M": 0}
    total = 0
    for A, B, C in product(grid, repeat=3):
        counts[run_c(A, B, C, A_max, M, L)] += 1
        total += 1
    return {k: 100 * v / total for k, v in counts.items()}, total


# ---------- тести ----------

def tests():
    assert reflect((0, 1), (0, 0), (1, 0)) == (0, -1)
    assert orthocenter((0, 0), (4, 0), (0, 3)) == (0, 0)        # прямий кут
    assert polar_mean([(1, 0), (0, 0), (2, 0)]) == (1, 0)       # є r = 0
    x, y = rotate((1, 0), (0, 0), math.pi / 2)
    assert abs(x) < 1e-12 and abs(y - 1) < 1e-12
    assert area(convex_hull([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)])) == 4
    assert snap((2.6, -9), 3) == (2, -2)
    print("All tests passed")


# ---------- ввід / вивід ----------

def read_point(name, conv=float):
    x, y = input(f"{name} (x y) = ").split()
    return (conv(x), conv(y))


def fmt(P):
    return f"({P[0]:.6g}, {P[1]:.6g})"


if __name__ == "__main__":
    tests()
    A = read_point("A")
    B = read_point("B")
    C = read_point("C")

    # (a)
    N = int(input("N = "))
    print(f"\n(a) перші {N} точок:")
    for i, P in enumerate(solve_a(A, B, C, N)):
        print(f"  {i}: {fmt(P)}")

    # (b)
    A_max = float(input("\nA (межа площі) = "))
    M = int(input("M (межа кроків) = "))
    seq, steps, S, reason = solve_b(A, B, C, A_max, M)
    print(f"\n(b) кроків: {steps}, точок: {len(seq)}, площа: {S:.6g}, зупинка: {reason}")
    far, near = extreme_pairs(seq)
    print("  37 найдальших пар (відстань, i, j):")
    for d, i, j in far:
        print(f"    {d:.6g}  {i} {fmt(seq[i])} — {j} {fmt(seq[j])}")
    print("  25 найближчих пар (відстань, i, j):")
    for d, i, j in near:
        print(f"    {d:.6g}  {i} {fmt(seq[i])} — {j} {fmt(seq[j])}")

    # (c)
    L = int(input("\nL = "))
    A_c = float(input("A для (c) = "))
    M_c = int(input("M для (c) = "))
    perc, total = solve_c(A_c, M_c, L)
    print(f"\n(c) трійок: {total}")
    for k, v in perc.items():
        print(f"  {k}: {v:.2f}%")