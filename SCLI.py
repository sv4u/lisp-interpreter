# this is a simple Lisp interpreter
# there will be customization to it

# IMPORTS
import sys
import re
import math
import cmath
import operator as op


# SYMBOLS
# Lisp Symbols are equivalent to Python strings
class Symbol(str):
	pass


# Create a table to store and/or create new Symbols
def Sym(s, symbol_table={}):
	if s not in symbol_table:
		symbol_table[s] = Symbol(s)
	return symbol_table[s]


# Standard Symbols
(_quote, _if, _set, _define, _lambda, _begin, _definemacro) = map(Sym,
	'quote if set! define lambda begin define-macro'.split())


# More Standard Symbols
(_quasiquote, _unquote, _unquotesplicing) = map(Sym,'quasiquote unquote unquote-splicing'.split())


# More Standard Symbols
_append, _cons, _let = Sym("append"), Sym("cons"), Sym("let")


# Grouping all of the quote types together
quotes = {"'": _quote, '`': _quasiquote, ',': _unquote, ',@': _unquotesplicing}


# INPORT
# Create the Input Port object
class InPort(object):
	tokenizer = r'''\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)'''

	def __init__(self, file):
		self.file = file
		self.line = ''

	def next_token(self):
		while True:
			if self.line == '':
				self.line = self.file.readline()
			if self.line == '':
				return eof
			(token, self.line) = re.match(InPort.tokenizer, self.line).groups()
			if token != '' and not token.startswith(';'):
				return token


# LEXING
eof = Symbol('#<eof-object>')

# Read next character from the input port
def readchar(port):
	if port.line != '':
		(ch, port.line) = (port.line[0], port.line[1:])
		return ch
	else:
		return port.file.read(1) or eof


# Read the Lisp expression from an input port
def read(port):
	def read_ahead(token):
		if '(' == token:
			L = []
			while True:
				token = inport.next_token()
				if token == ')':
					return L
				else:
					L.append(read_ahead(token))
		elif ')' == token:
			raise SyntaxError('unexpected )')
		elif token in quotes:
			return [quotes[token], read(inport)]
		elif token is eof:
			raise SyntaxError('unexpected EOF in list')
		else:
			return atomize(token)
	token1 = port.next_token()
	return (eof if token1 is eof else read_ahead(token1))


# Numbers become numbers, Lisp booleans become Python booleans, '...' is a string
# Otherwise, the token becomes a Symbol
def atomize(token):
	if token == '#t':
		return True
	elif token == '#f':
		return False
	elif token[0] == '"':
		return token[1:-1].decode('string_escape')
	try:
		return int(token)
	except ValueError:
		try:
			return float(token)
		except ValueError:
			try:
				return complex(token.replace('i', 'j', 1))
			except ValueError:
				return Sym(token)


# Convert a Python object to a Lisp object
def py_to_lisp(x):
	if x is True:
		return '#t'
	elif x is False:
		return '#f'
	elif isinstance(x, Symbol):
		return x
	elif isinstance(x, str):
		return '"%s"' % x.encode('string_escape').replace('"', r'\"')
	elif isinstance(x, list):
		return '(' + ' '.join(map(py_to_lisp, x)) + ')'
	elif isinstance(x, complex):
		return str(x).replace('j', 'i')
	else:
		return str(x)


# Standard SCLI REPL
def repl(prompt='custom-lisp > ', inport=InPort(sys.stdin), out=sys.stdout):
	while True:
		try:
			if prompt:
				sys.stderr.write(prompt)
			x = parse(inport)
			if x is eof:
				return
			val = evaluate(x)
			if val is not None and out:
				print >> out, py_to_lisp(val)
		except Exception as e:
			print('%s: %s' % (type(e).__name__, e))


# Evaluate all lines from a Lisp file
def load(filename):
	repl(None, InPort(open(filename)), None)


# ENVIRONMENT
# Create the standard environment for Lisp
class Environment(dict):
	# Bind parameters to their respective arguments, or a single parameter to a list of arguments
	def __init__(self, parms=(), args=(), outer=None):
		self.outer = outer
		if isinstance(parms, Symbol):
			self.update({parms: list(args)})
		else:
			if len(args) != len(parms):
				raise TypeError('expected %s, given %s, ' % (py_to_lisp(parms), py_to_lisp(args)))
				self.update(zip(parms, args))

	# Find the innermost Environment where 'var' appears
	def find(self, var):
		if var in self:
			return self
		elif self.outer is None:
			raise LookupError(var)
		else:
			return self.outer.find(var)


# Primitive function to determine if it is a Lisp pair
def is_pair(x):
	return x != [] and isinstance(x, list)


# Call proc with the current continuation; escape only
def callcc(proc):
	bail = RuntimeWarning("Sorry, can't continue this continuation any longer.")

	def throw(retval):
		bail.retval = retval
		raise bail

	try:
		return proc(throw)
	except RuntimeWarning as w:
		if w is bail:
			return bail.retval
		else:
			raise w

# Define 'let' macro
def let(*args):
	args = list(args)
	x = cons(_let, args)
	require(x, len(args) > 1)
	(bindings, body) = (args[0], args[1:])
	require(x, all(isinstance(b, list) and len(b) == 2 and isinstance(b[0], Symbol) for b in bindings), 'illegal binding list')
	(vars, vals) = zip(*bindings)
	return [[_lambda, list(vars)] + map(expand, body)] + map(expand, vals)


# Table of macros
# More macros can be added
macro_table = {_let:let}


# Add standard Lisp procedures
def add_globals(self):
	self.update(vars(math))
	self.update(vars(cmath))
	self.update({
		'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
		'not': op.not_,
		'>': op.gt,	'<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
		'equal?': op.eq, 'eq?': op.is_,
		'length': len,
		'cons': lambda x, y: [x] + list(y),
		'car': lambda x: x[0],
		'cdr': lambda x: x[1:],
		'append': op.add,
		'list': lambda *x: list(x),
		'list?': lambda x: isinstance(x, list),
		'null?': lambda x: x == [],
		'symbol?': lambda x: isinstance(x, Symbol),
		'boolean?': lambda x: isinstance(x, bool),
		'pair?': is_pair,
		'port?': lambda x: isinstance(x, file),
		'apply': lambda proc, l: proc(*l),
		'evaluate': lambda x: evaluate(expand(x)),
		'load': lambda fn: load(fn),
		'call/cc': callcc,
		'open-input-file': open,
		'close-input-port': lambda p: p.file.close(),
		'open-output-file': lambda f: open(f, 'w'),
		'close-output-port': lambda p: p.close(),
		'eof-object?': lambda x: x is eof,
		'read-char': readchar,
		'read': read,
		'write': lambda x, port=sys.stdout: port.write(py_to_lisp(x)),
		'display': lambda x, port=sys.stdout: port.write((x if isinstance(x, str) else py_to_lisp(x)))
		})
	return self


# Create standard environment
environment = add_globals(Environment())


# Evaluate an expression in the Lisp environment
def evaluate(x, Environment=environment):
	while True:
		if isinstance(x, Symbol):															# variable reference
			return Environment.find(x)[x]
		elif not isinstance(x, list):													# constant literal
			return x
		elif x[0] is _quote:																	# (quote exp)
			(_, exp) = x
			return exp
		elif x[0] is _if:																			# (if test conseq alt)
			(_, test, conseq, alt) = x
			x = (conseq if evaluate(test, Environment) else alt)
		elif x[0] is _set:																		# (set! var exp)
			(_, var, exp) = x
			Environment.find(var)[var] = evaluate(exp, Environment)
			return None
		elif x[0] is _define:																	# (define var exp)
			(_, var, exp) = x
			Environment[var] = evaluate(exp, Environment)
			return None
		elif x[0] is _lambda:																	# (lambda (var*) exp)
			(_, vars, exp) = x
			return Procedure(vars, exp, Environment)
		elif x[0] is _begin:																	# (begin exp+)
			for exp in x[1:-1]:
				evaluate(exp, Environment)
			x = x[-1]
		else:																									# (proc exp*)
			exps = [evaluate(exp, Environment) for exp in x]
			proc = exps.pop(0)
			if isinstance(proc, Procedure):
				x = proc.exp
				Environment = Environment(proc.parms, exps, proc.Environment)
			else:
					return proc(*exps)


# PROCEDURE
# A user defined Lisp procedure
class Procedure(object):
	# Store the parameters, expression, and environment
	def __init__(self, parms, exp, Environment):
		(self.parms, self.exp, self.Environment) = (parms, exp, Environment)

	# Recall the user defined procedure and evaluate
	def __call__(self, *args):
		return evaluate(self.exp, Environment(self.parms, args, self.Environment))


# PARSING
# Read and expand (error-check) a Lisp program
def parse(inport):
	if isinstance(inport, str):
		inport = InPort(StringIO.StringIO(inport))
	return expand(read(inport), toplevel=True)


# Walk the AST, make fixes in syntax (optimization), and raise SyntaxError
def expand(x, toplevel=False):
	require(x, x != [])																			# () => Error
	if not isinstance(x, list):															# constant => unchanged
		return x
	elif x[0] is _quote:																		# (quote ...)
		require(x, len(x) == 2)
		return x
	elif x[0] is _if:
		if len(x) == 3:																				# (if t c) => (if t c None)
			x = x + [None]
			require(x, len(x) == 4)
		return map(expand, x)
	elif x[0] is _set:
		require(x, len(x) == 3)
		var = x[1]  																					# (set! non-var exp) => Error
		require(x, isinstance(var, Symbol), 'can set! only a symbol')
		return [_set, var, expand(x[2])]
	elif x[0] is _define or x[0] is _definemacro:
		require(x, len(x) >= 3)
		(_def, v, body) = (x[0], x[1], x[2:])
		if isinstance(v, list) and v:													# (define (f args) body) => (define f (lambda (args) body))
				(f, args) = (v[0], v[1:])
				return expand([_def, f, [_lambda, args] + body])
		else:
			require(x, len(x) == 3)															# (define non-var/list exp) => Error
			require(x, isinstance(v, Symbol), 'can define only a symbol')
			exp = expand(x[2])
			if _def is _definemacro:
				require(x, toplevel, 'define-macro only allowed at top level')
				proc = evaluate(exp)
				require(x, callable(proc), 'macro must be a procedure')
				macro_table[v] = proc															# (define-macro v proc) => None; add v:proc to macro_table
				return None
			return [_define, v, exp]
	elif x[0] is _begin:
		if len(x) == 1:  																			# (begin) => None
			return None
		else:
				return [expand(xi, toplevel) for xi in x]
	elif x[0] is _lambda:																		# (lambda (x) e1 e2) => (lambda (x) (begin e1 e2))
		require(x, len(x) >= 3)
		(vars, body) = (x[1], x[2:])
		require(x, isinstance(vars, list) and all(isinstance(v, Symbol) for v in vars)
			or isinstance(vars, Symbol), 'illegal lambda argument list')
		exp = (body[0] if len(body) == 1 else [_begin] + body)
		return [_lambda, vars, expand(exp)]
	elif x[0] is _quasiquote:																# `x => expand_quasiquote(x)
		require(x, len(x) == 2)
		return expand_quasiquote(x[1])
	elif isinstance(x[0], Symbol) and x[0] in macro_table:
		return expand(macro_table[x[0]](*x[1:]), toplevel)		# (m arg...) => macroexpand if m isinstance macro
	else:
		return map(expand, x) 																# (f arg...) => expand each


# Raise a SyntaxError if the predicate is false
def require(x, predicate, msg='wrong length'):
	if not predicate:
		raise SyntaxError(py_to_lisp(x) + ': ' + msg)

# Expand all the types of quotes
def expand_quasiquote(x):
	if not is_pair(x):
		return [_quote, x]
	require(x, x[0] is not _unquotesplicing, "can't splice here")
	if x[0] is _unquote:
		require(x, len(x) == 2)
		return x[1]
	elif is_pair(x[0]) and x[0][0] is _unquotesplicing:
		require(x[0], len(x[0]) == 2)
		return [_append, x[0][1], expand_quasiquote(x[1:])]
	else:
		return [_cons, expand_quasiquote(x[0]), expand_quasiquote(x[1:])]