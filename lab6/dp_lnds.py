def longest_non_decreasing(arr):
    n = len(arr)
    if n == 0:
        return []
    dp = [1] * n
    prev = [-1] * n
    for i in range(n):
        for j in range(i):
            if arr[j] <= arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
    end = max(range(n), key=lambda k: dp[k])
    result = []
    while end != -1:
        result.append(arr[end])
        end = prev[end]
    return result[::-1]

if __name__ == "__main__":
    line = input("Введіть числа через пробіл: ").split()
    arr = [int(x) for x in line] if line else [5, 1, 3, 3, 2, 4, 1, 6, 5]
    res = longest_non_decreasing(arr)
    print("Масив:", arr)
    print("Найдовша неспадаюча підпослідовність:", res, "довжина", len(res))