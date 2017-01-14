# this is a simple Lisp interpreter
import math
import operator as op

Env = dict

def standard_environment():
	env = Env()
	env.update(vars(math))
	env.update({
		'+':op.add, '-':op.sub,
		'*':op.mul, '/':op.truediv,
		'>':op.gt, '<':op.lt,
		'>=':op.ge, '<=':op.le,
		'=':op.eq,
		'abs':abs,
		'append':op.add,
		'begin':lambda *x: x[-1],
		'car':lambda x: x[0], 'cdr':lambda x: x[1:], 'cons':lambda x,y: [x] + y,
		'eq?':op.is_, 'equal?':op.eq,
		'length':len,
		'list':lambda *x: list(x), 'list?':lambda x: isinstance(x, list),
		'map':map,
		'max':max, 'min':min,
		'not':op.not_,
		'null?':lambda x: x == [],
		'number?':lambda x: x == isinstance(x, Number),
		'procedure?':callable,
		'round':round,
		'symbol?':lambda x: x == isinstance(x, str),
		})
	return env

global_env = standard_environment()

def tokenize(input):
	return input.replace('(', ' ( ').replace(')', ' ) ').split()


def read_tokens(tokens):
	if (len(tokens)) == 0:
		raise SyntaxError('unexpected EOF while reading')
	token = tokens.pop(0)
	if ('(' == token):
		inside = []
		while tokens[0] != ')':
			inside.append(read_tokens(tokens))
		tokens.pop(0)
		return inside
	elif (')' == token):
		raise SyntaxError('unexpected closed parenthesis')
	else:
		return atomize(token)


def atomize(token):
	try: return int(token)
	except ValueError:
		try: return float(token)
		except ValueError:
			return str(token)


def parse(input):
	return read_tokens(tokenize(input))


def evaluate(x, env=global_env):
	if (isinstance(x, str)):
		return env[x]
	elif (not isinstance(x, list)):
		return x
	elif (x[0] == 'if'):
		(_, test, conseq, alt) = x
		expression = (conseq if evaluate(test, env) else alt)
		return evaluate(expression, env)
	elif (x[0] == 'define'):
		(_, var, expression) = x
		env[var] = evaluate(expression, env)
	else:
		proc = evaluate(x[0], env)
		args = [evaluate(arg, env) for arg in x[1:]]
		return proc(*args)

def testing():
	program = "(begin (define t 42) (* pi (* t t)))"
	p = parse(program)
	print(p)
	e = evaluate(p)
	print(e)


testing()