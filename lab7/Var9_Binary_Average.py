import os
import random
from array import array

CHUNK = 65536


def generate(path, count, low=-1000.0, high=1000.0):
    with open(path, "wb") as f:
        left = count
        while left > 0:
            n = min(CHUNK, left)
            array("d", (random.uniform(low, high) for _ in range(n))).tofile(f)
            left -= n


def average_positive(path):
    total = 0.0
    count = 0
    with open(path, "rb") as f:
        while True:
            data = f.read(CHUNK * 8)
            if not data:
                break
            numbers = array("d")
            numbers.frombytes(data[:len(data) // 8 * 8])
            for x in numbers:
                if x > 0:
                    total += x
                    count += 1
    return (total / count if count else None), count


if __name__ == "__main__":
    path = input("Ім'я бінарного файлу (Enter = numbers.bin): ").strip() or "numbers.bin"
    if not os.path.exists(path):
        n = input("Файлу немає. Скільки чисел згенерувати (Enter = 1000000): ").strip()
        generate(path, int(n) if n else 1_000_000)
        print("Файл", path, "створено")
    avg, count = average_positive(path)
    print("Розмір файлу:", os.path.getsize(path), "байт")
    print("Кількість додатних елементів:", count)
    if avg is None:
        print("Додатних елементів немає")
    else:
        print("Середнє арифметичне додатних:", avg)
        