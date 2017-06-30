import math

func = {
"modpow": lambda x, y, z: modpow(x, y, z),
"sqrt": lambda x: sqrt(x),
"nroot": lambda x, n: nroot(x, n),
"abs": lambda x: abs(x),
"ceiling": lambda x: math.ceil(x),
"floor": lambda x: math.floor(x),
"factorial": lambda x: factorial(x),
"ln": lambda x: ln(x),
"log": lambda x, n: log(x, n),
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

def ceil(x):
	return math.ceil(x)

def floor(x):
	return math.floor(x)

def factorial(x):
	return math.factorial(x)

def ln(x):
	return math.log(x)

def log(x, n):
	return math.log(x, n)