import matplotlib.pyplot as plt

EPS = 1e-9


def cross(a, b, p):
    """Псевдоскалярний добуток векторів AB і AP."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def classify(a, b, c, p):
    """Повертає 'inside', 'edge' або 'outside'."""
    if abs(cross(a, b, c)) < EPS:
        raise ValueError("Вироджений трикутник: точки лежать на одній прямій")

    d = [cross(a, b, p), cross(b, c, p), cross(c, a, p)]
    has_neg = any(x < -EPS for x in d)
    has_pos = any(x > EPS for x in d)

    if has_neg and has_pos:
        return "outside"
    if any(abs(x) <= EPS for x in d):
        return "edge"
    return "inside"


def read_point(text):
    x, y = map(float, input(text).split())
    return (x, y)


def draw(a, b, c, p, result):
    xs = [a[0], b[0], c[0], a[0]]
    ys = [a[1], b[1], c[1], a[1]]
    plt.plot(xs, ys, "b-")
    plt.scatter([p[0]], [p[1]], color="red", zorder=3)
    for name, pt in zip("ABCP", (a, b, c, p)):
        plt.annotate(name, pt, textcoords="offset points", xytext=(5, 5))
    plt.title(f"Результат: {result}")
    plt.axis("equal")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    A = read_point("Вершина A (x y): ")
    B = read_point("Вершина B (x y): ")
    C = read_point("Вершина C (x y): ")
    P = read_point("Точка P (x y): ")

    names = {"inside": "всередині", "edge": "на ребрі", "outside": "зовні"}
    try:
        res = classify(A, B, C, P)
    except ValueError as e:
        print("Помилка:", e)
    else:
        print("Точка", names[res])
        draw(A, B, C, P, names[res])