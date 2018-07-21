from sympy.solvers import solve
from sympy import N
import sympy

def linsolve(a, b):
    x = sympy.Symbol("x")
    return map(N, solve(a * x - b, x))


def quadsolve(a, b, c):
    x = sympy.Symbol("x")
    solution = solve(a * (x ** 2) + b * x - c, x)
    return map(N, solution)


def cubesolve(a, b, c, d):
    x = sympy.Symbol("x")
    solution = solve(a * (x ** 3) + b * (x ** 2) + c * x - d, x)
    return map(N, solution)
