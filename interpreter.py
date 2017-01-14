# this is a simple Lisp interpreter

def tokenize(input):
	return input.replace('(', ' ( ').replace(')', ' ) ').split()