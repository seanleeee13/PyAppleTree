def a():
    for i in range(10000):
        a = 1 + i
    return a

def b():
    for i in range(12000):
        a = 1 + i
    return a

def c():
    for i in range(14000):
        a = 1 + i
    return a

def d():
    for i in range(16000):
        a = 1 + i
    return a

def e():
    for i in range(18000):
        a = 1 + i
    return a

def f(x):
    if x <= 0:
        return 0
    x = min(x, 25)
    a = 0
    for i in range(x):
        a += i + f(i)
    return a

for i in range(10000):
    a()
    b()
    c()
    d()
    e()
    f(i)