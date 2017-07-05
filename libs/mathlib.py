func = {
    "modpow": lambda x, y, z: modpow(x, y, z),
    "sqrt": lambda x: sqrt(x),
    "nroot": lambda x, n: nroot(x, n),
    "abs": lambda x: abs(x)
}


def modpow(x, e, n):
    y = 1
    while e > 0:
        if e % 2 == 0:
            x = (x * x) % n
            e = e/2
        else:
            y = (x * y) % n
            e = e - 1
    return y


def sqrt(x):
    return x ** (0.5)


def nroot(x, n):
    return x ** (1.0/n)