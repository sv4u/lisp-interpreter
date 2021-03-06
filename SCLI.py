#!/usr/bin/python2
# -*- coding: utf-8 -*-
# this is a simple Lisp interpreter
# there will be customization to it
# use Python 2.7 not 3.x

import sys
import re
from sympy.solvers import solve
from sympy import N
import sympy
from libs.mathlib import *
from libs.solverlib import *
import math

isa = isinstance
VERSION = "0.4-alpha"
current_prompt = 'scli v:' + VERSION + ' > '


###############################################################################
###############################################################################
#                                   Symbols                                   #
###############################################################################
###############################################################################


class Symbol(str):

    pass


def Sym(s, symbol_table={}):
    '''Find or create unique Symbol entry for str s in symbol table.'''

    if s not in symbol_table:
        symbol_table[s] = Symbol(s)
    return symbol_table[s]


(_quote, _if, _set, _define, _lambda, _begin, _definemacro) = map(
    Sym, 'quote if set! define lambda begin define-macro'.split())

(_quasiquote, _unquote, _unquotesplicing) = map(
    Sym, 'quasiquote unquote unquote-splicing'.split())

(_append, _cons, _let) = (Sym('append'), Sym('cons'), Sym('let'))


###############################################################################
###############################################################################
#                                   InPorts                                   #
###############################################################################
###############################################################################


class InPort(object):
    '''An input port. Retains a line of chars.'''

    tokenizer = r'''\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)'''

    def __init__(self, file):
        self.file = file
        self.line = ''

    def next_token(self):
        '''Return the next token'''

        while True:
            if self.line == '':
                self.line = self.file.readline()
            if self.line == '':
                return eof_object
            (token, self.line) = re.match(InPort.tokenizer,
                                          self.line).groups()
            if token != '' and not token.startswith(';'):
                return token


eof_object = Symbol('#<eof-object>')


###############################################################################
###############################################################################
#                                   Reading                                   #
###############################################################################
###############################################################################


def readchar(inport):
    '''Read the next character from an input port.'''

    if inport.line != '':
        (ch, inport.line) = (inport.line[0], inport.line[1:])
        return ch
    else:
        return inport.file.read(1) or eof_object


def read(inport):
    '''Read a Lisp expression from an input port.'''

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
        elif token is eof_object:
            raise SyntaxError('unexpected EOF in list')
        elif '!quit' == token:
            sys.exit()
        else:
            return atomize(token)

    token1 = inport.next_token()
    return (eof_object if token1 is eof_object else read_ahead(token1))


quotes = {
    "'": _quote,
    '`': _quasiquote,
    ',': _unquote,
    ',@': _unquotesplicing,
}


def atomize(token):
    '''Convert tokens to atomic types'''

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


def to_string(x):
    '''Convert a Python object back into a Lisp-readable string.'''

    if x is True:
        return '#t'
    elif x is False:
        return '#f'
    elif isa(x, Symbol):
        return x
    elif isa(x, str):
        return '"%s"' % x.encode('string_escape').replace('"', r'\"')
    elif isa(x, list):
        return '(' + ' '.join(map(to_string, x)) + ')'
    elif isa(x, complex):
        return str(x).replace('j', 'i')
    else:
        return str(x)


###############################################################################
###############################################################################
#                                  Libraries                                  #
###############################################################################
###############################################################################


def add_libs(x, out=sys.stdout):
    if x == "math":
        global_env.update(add_math())
    elif x == "strings":
        global_env.update(add_strings())
    elif x == "stats":
        global_env.update(add_stats())
    elif x == "solver":
        global_env.update(add_solver())
    else:
        print >> out, "ERROR: Library not found!"


def add_math():
    '''Add math library functions'''

    func = {
        "modpow": lambda x, y, z: modpow(x, y, z),
        "sqrt": lambda x: math.sqrt(x),
        "nroot": lambda x, n: nroot(x, n),
        "abs": lambda x: abs(x),
        "ceil": lambda x: math.ceil(x),
        "floor": lambda x: math.floor(x),
        "ln": lambda x: math.log(x),
        "log": lambda x, n: math.log(x, n),
        "log": lambda x: math.log(x, 2)
    }

    return func


def add_strings():
    '''String library'''

    func = {
        "concat": lambda x, y: x + y,
        "substring": lambda x, y, z: x[y:z],
        "charat": lambda x, y: x[y],
        "length": lambda x: len(x),
        "split": lambda x, y: x.split(str(y))
    }

    return func


def add_stats():
    '''Stats library'''

    func = {}

    return func


def add_solver():
    '''Solver library'''

    func = {
        "linear-solve": lambda a, b: linsolve(a, b),
        "quadratic-solve": lambda a, b, c: quadsolve(a, b, c),
        "cubic-solve": lambda a, b, c, d: cubesolve(a, b, c, d)
    }

    return func


def add_user_libs(x):
    
    repl(None, inport=InPort(open(x)))


###############################################################################
###############################################################################
#                                  Load+REPL                                  #
###############################################################################
###############################################################################


def load(filename):
    '''Eval every expression from a file.'''

    repl(None, InPort(open(filename)), None)


def repl(prompt=current_prompt, inport=InPort(sys.stdin), out=sys.stdout):
    '''A standard SCLI read-eval-prompt loop.'''

    while True:
        try:
            if prompt:
                sys.stderr.write(prompt)
            x = parse(inport)
            if x is eof_object:
                return
            val = eval(x)
            if val is not None and out:
                print >> out, to_string(val)
        except Exception as e:
            print('%s: %s' % (type(e).__name__, e))


###############################################################################
###############################################################################
#                                     Let                                     #
###############################################################################
###############################################################################


def let(*args):
    '''Add the let macro'''

    args = list(args)
    x = cons(_let, args)
    require(x, len(args) > 1)
    (bindings, body) = (args[0], args[1:])
    require(x, all(isa(b, list) and len(b) == 2 and isa(b[0], Symbol)
                   for b in bindings), 'illegal binding list')
    (vars, vals) = zip(*bindings)
    return [[_lambda, list(vars)] + map(expand, body)] + map(expand,
                                                             vals)


macro_table = {_let: let}


###############################################################################
###############################################################################
#                                 Environment                                 #
###############################################################################
###############################################################################


class Env(dict):

    """An environment: a dict of {'var':val} pairs, with an outer Env."""

    def __init__(self, parms=(), args=(), outer=None):
        '''Bind parms to args, or parms to a list or args'''

        self.outer = outer
        if isa(parms, Symbol):
            self.update({parms: list(args)})
        else:
            if len(args) != len(parms):
                raise TypeError('expected %s, given %s, '
                                % (to_string(parms), to_string(args)))
            self.update(zip(parms, args))

    def find(self, var):
        '''Find the innermost Env where var appears.'''

        if var in self:
            return self
        elif self.outer is None:
            raise LookupError(var)
        else:
            return self.outer.find(var)


###############################################################################
###############################################################################
#                               Pair and CallCC                               #
###############################################################################
###############################################################################


def is_pair(x):
    '''Determine if x is a Lisp pair'''

    return x != [] and isa(x, list)


def callcc(proc):
    '''Call proc with current continuation; escape only'''

    bail = RuntimeWarning(
        "Sorry, can't continue this continuation any longer.")

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


###############################################################################
###############################################################################
#                                   Globals                                   #
###############################################################################
###############################################################################


def add_globals(self):
    '''Add some Lisp standard procedures.'''

    import math
    import cmath
    import operator as op
    self.update(vars(math))
    self.update(vars(cmath))
    self.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        'mod': op.mod,
        'not': op.not_,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'equal?': op.eq,
        '>>': op.rshift,
        '<<': op.lshift,
        '|': op.or_,
        '~': op.invert,
        '&': op.and_,
        'xor': op.xor,
        'abs': op.abs,
        'exp': op.pow,
        'eq?': op.is_,
        'length': len,
        'cons': lambda x, y: [x] + list(y),
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'append': op.add,
        'list': lambda *x: list(x),
        'list?': lambda x: isa(x, list),
        'null?': lambda x: x == [],
        'symbol?': lambda x: isa(x, Symbol),
        'boolean?': lambda x: isa(x, bool),
        'pair?': is_pair,
        'port?': lambda x: isa(x, file),
        'apply': lambda proc, l: proc(*l),
        'eval': lambda x: eval(expand(x)),
        'load': lambda fn: load(fn),
        'call/cc': callcc,
        'open-input-file': open,
        'close-input-port': lambda p: p.file.close(),
        'open-output-file': lambda f: open(f, 'w'),
        'close-output-port': lambda p: p.close(),
        'eof-object?': lambda x: x is eof_object,
        'read-char': readchar,
        'read': read,
        'write': lambda x, port=sys.stdout: port.write(to_string(x) + "\n"),
        'display': lambda x, port=sys.stdout: port.write((x if isa(x, str) else to_string(x))),
        'import': lambda x: add_libs(to_string(x)),
        'user-import': lambda x: add_user_libs(to_string(x))
    })
    return self


global_env = add_globals(Env())


###############################################################################
###############################################################################
#                                 Evaluations                                 #
###############################################################################
###############################################################################


def eval(x, env=global_env):
    '''Evaluate an expression in an environment.'''

    while True:
        if isa(x, Symbol):
            return env.find(x)[x]
        elif not isa(x, list):
            return x
        elif x[0] is _quote:
            (_, exp) = x
            return exp
        elif x[0] is _if:
            (_, test, conseq, alt) = x
            x = (conseq if eval(test, env) else alt)
        elif x[0] is _set:
            (_, var, exp) = x
            env.find(var)[var] = eval(exp, env)
            return None
        elif x[0] is _define:
            (_, var, exp) = x
            env[var] = eval(exp, env)
            return None
        elif x[0] is _lambda:
            (_, vars, exp) = x
            return Procedure(vars, exp, env)
        elif x[0] is _begin:
            for exp in x[1:-1]:
                eval(exp, env)
            x = x[-1]
        else:
            exps = [eval(exp, env) for exp in x]
            proc = exps.pop(0)
            if isa(proc, Procedure):
                x = proc.exp
                env = Env(proc.parms, exps, proc.env)
            else:
                return proc(*exps)


###############################################################################
###############################################################################
#                                  Procedure                                  #
###############################################################################
###############################################################################


class Procedure(object):

    '''A user-defined Lisp procedure.'''

    def __init__(self, parms, exp, env):
        (self.parms, self.exp, self.env) = (parms, exp, env)

    def __call__(self, *args):
        return eval(self.exp, Env(self.parms, args, self.env))


###############################################################################
###############################################################################
#                                   Parsing                                   #
###############################################################################
###############################################################################


def parse(inport):
    '''Parse a program: read and expand/error-check it.'''

    if isinstance(inport, str):
        inport = InPort(StringIO.StringIO(inport))
    return expand(read(inport), toplevel=True)


def expand(x, toplevel=False):
    '''Walk tree of x, making optimizations, and signaling SyntaxError'''

    require(x, x != [])
    if not isa(x, list):
        return x
    elif x[0] is _quote:
        require(x, len(x) == 2)
        return x
    elif x[0] is _if:
        if len(x) == 3:
            x = x + [None]
        require(x, len(x) == 4)
        return map(expand, x)
    elif x[0] is _set:
        require(x, len(x) == 3)
        var = x[1]
        require(x, isa(var, Symbol), 'can set! only a symbol')
        return [_set, var, expand(x[2])]
    elif x[0] is _define or x[0] is _definemacro:
        require(x, len(x) >= 3)
        (_def, v, body) = (x[0], x[1], x[2:])
        if isa(v, list) and v:
            (f, args) = (v[0], v[1:])
            return expand([_def, f, [_lambda, args] + body])
        else:
            require(x, len(x) == 3)
            require(x, isa(v, Symbol), 'can define only a symbol')
            exp = expand(x[2])
            if _def is _definemacro:
                require(x, toplevel,
                        'define-macro only allowed at top level')
                proc = eval(exp)
                require(x, callable(proc), 'macro must be a procedure')
                macro_table[v] = proc
                return None
            return [_define, v, exp]
    elif x[0] is _begin:
        if len(x) == 1:
            return None
        else:
            return [expand(xi, toplevel) for xi in x]
    elif x[0] is _lambda:
        require(x, len(x) >= 3)
        (vars, body) = (x[1], x[2:])
        require(x, isa(vars, list) and all(isa(v, Symbol) for v in
                                           vars) or isa(vars, Symbol),
                'illegal lambda argument list')
        exp = (body[0] if len(body) == 1 else [_begin] + body)
        return [_lambda, vars, expand(exp)]
    elif x[0] is _quasiquote:
        require(x, len(x) == 2)
        return expand_quasiquote(x[1])
    elif isa(x[0], Symbol) and x[0] in macro_table:
        return expand(macro_table[x[0]](*x[1:]), toplevel)
    else:
        return map(expand, x)


def require(x, predicate, msg='wrong length'):
    '''Signal a syntax error if predicate is false.'''

    if not predicate:
        raise SyntaxError(to_string(x) + ': ' + msg)


def expand_quasiquote(x):
    """Expand `x => 'x; `,x => x; `(,@x y) => (append x y) """

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
        return [_cons, expand_quasiquote(x[0]),
                expand_quasiquote(x[1:])]


###############################################################################
###############################################################################
#                                    Main                                     #
###############################################################################
###############################################################################


if (len(sys.argv) == 2):
    load(sys.argv[1])
else:
    print "Welcome to SCLI " + VERSION
    print "To quit: !quit"
    print ""

    repl()
