from itertools import combinations


def is_acute(a, b, c):
    return a + b > c and a * a + b * b > c * c


def acute_triples(arr):
    found = set()
    for a, b, c in combinations(sorted(arr), 3):
        if is_acute(a, b, c):
            found.add((a, b, c))
    return sorted(found)


if __name__ == "__main__":
    line = input("Введіть натуральні числа через пробіл: ").split()
    arr = [int(x) for x in line] if line else [2, 3, 4, 4, 5, 6, 10, 3, 3]
    triples = acute_triples(arr)
    print("Масив:", arr)
    if triples:
        for t in triples:
            print(*t)
    else:
        print("Таких трійок немає")