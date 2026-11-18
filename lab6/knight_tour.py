MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]


def knight_tour(n=8, start=(0, 0)):
    board = [[0] * n for _ in range(n)]

    def free(r, c):
        return 0 <= r < n and 0 <= c < n and board[r][c] == 0

    def degree(r, c):
        return sum(free(r + dr, c + dc) for dr, dc in MOVES)

    def solve(r, c, step):
        board[r][c] = step
        if step == n * n:
            return True
        candidates = [(r + dr, c + dc) for dr, dc in MOVES if free(r + dr, c + dc)]
        candidates.sort(key=lambda p: degree(*p))
        for nr, nc in candidates:
            if solve(nr, nc, step + 1):
                return True
        board[r][c] = 0
        return False

    return board if solve(*start, 1) else None


if __name__ == "__main__":
    s = input("Розмір дошки (Enter = 8): ").strip()
    n = int(s) if s else 8
    result = knight_tour(n)
    if result is None:
        print("Маршруту не існує")
    else:
        for row in result:
            print(" ".join(f"{x:3}" for x in row))