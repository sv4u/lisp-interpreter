# this is a simple Lisp interpreter

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
			return token


def parse(input):
	return read_tokens(tokenize(input))


def testing():
	program = "(begin (define t 42) (* pi (* t t)))"
	print(parse(program))


testing()