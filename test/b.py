def cpu_heavy():
    s = 0
    for i in range(20_000_000):
        s += i
    return s


def many_calls_inner():
    return sum(range(100))


def many_calls():
    total = 0
    for _ in range(500_000):
        total += many_calls_inner()
    return total


def recursive(n):
    if n <= 1:
        return 1
    return recursive(n - 1) + recursive(n - 2)


def normal():
    return sum(range(1000))


if __name__ == "__main__":
    for i in range(20):
        cpu_heavy()
        many_calls()
        recursive(28)
        normal()