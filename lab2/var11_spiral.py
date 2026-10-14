import math
import matplotlib.pyplot as plt


def spiral_points(a, b, theta, n):
    """Перші n точок спіралі r = a * exp(b * phi), phi = k * theta."""
    xs, ys = [], []
    for k in range(n):
        phi = k * theta
        r = a * math.exp(b * phi)
        xs.append(r * math.cos(phi))
        ys.append(r * math.sin(phi))
    return xs, ys


if __name__ == "__main__":
    a = float(input("a: "))
    b = float(input("b: "))
    theta = float(input("Крок по куту theta (радіани): "))
    n = int(input("Кількість точок N: "))

    xs, ys = spiral_points(a, b, theta, n)

    plt.plot(xs, ys, "-", color="gray", linewidth=0.8)
    plt.scatter(xs, ys, s=12, color="red", zorder=3)
    plt.title(f"Спіраль r = a*exp(b*phi), a={a}, b={b}, theta={theta}, N={n}")
    plt.axis("equal")
    plt.grid(True)
    plt.show()