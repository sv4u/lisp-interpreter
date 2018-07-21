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


def nroot(x, n):
    return x ** (1.0 / n)
