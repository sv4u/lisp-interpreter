# A Simple (Custom) Lisp Interpreter

**SCLI** (*A Simple (Custom) Lisp Interpreter*) is a custom Lisp interpreter built in Python 2.7.x. It is meant to follow the language I developed that is an offshoot of Lisp.

## Motivation

I have been interested in creating a programming language for the past year. So, I decided to read a bunch of manuals and then one day I finally tried writing one. This is the outcome of that day.

## Usage

In the Python console, import the [interpreter](https://github.com/sv4u/lisp-interpreter/blob/master/SCLI.py).
Once the interpreter has been imported, run the *read-evaluate-prompt-loop* function like so:
```
python SCLI.py
```
The output of this should be
```python
scli >
```
To exit the prompt type
```python
scli > !quit
```
To use SCLI as a compiler instead of a repl, you can run it like so:
```
python SCLI.py file.scli
```
Now you're ready to program in SCLI!

## Releases

Currently, we have the alpha release here: [github.com/sv4u/scli-interpreter/releases/tag/alpha](https://github.com/sv4u/scli-interpreter/releases/tag/alpha)

## Install

To install, clone the repository into any directory you wish. Then, add that directory to your `PATH` so that you can execute `scli` from anywhere.

## Documentation

To import the math package, type
```python
scli > (import 'math)
```

To import a user package, type
```python
scli > (user-import '*user library*)
```
**Note:** The file name must have no spaces in it and must end in ".scli".

### Current Libraries

The current libraries that have been implemented fully are:
- Math
- Strings

Libraries that are under development are:
- Solver

Libraries that have not been developed yet are:
- Statistics

### Math Library

Some math functions that have been implemented in the ```math``` package are:
- Exponentiation
- Modular exponentiation
- `sqrt(x)`
- `nroot(x, n)`: the nth root of x
- `ceil(x)` and `floor(x)`
- `ln(x)`, `log10(x)`, and `log2(x)`

### Strings Library

Some string functions that have been implemented in the ```strings``` package are:
- Concatenation
- Substrings
- Character At
- Length
- Split on a regular expression

### Solver Library

Some solver functions that have been implemented in the ```solver``` package are:
- Linear Solving
	- Format:
```lisp
(linear-solve a b)
```
solves
```
ax = b
```
- Quadratic Solving
	- Format:
```lisp
(quadraticr-solve a b c)
```
solves
```
ax^2 + bx = c
```
- Cubic Solving
	- Format:
```lisp
(linear-solve a b)
```
solves
```
ax^3 + bx^2 + cx = d
```

Note: this packages uses the [SymPy](http://www.sympy.org/en/index.html) library.

## Contact
If you are interested in seeing this project grow or helping me, feel free to contact me at [svvishnu@andrew.cmu.edu](mailto:svvishnu@andrew.cmu.edu). I'm always looking for help.

## [License](https://github.com/sv4u/scli-interpreter/blob/master/LICENSE)

> MIT License

> Copyright (c) 2017 Sasank Venkata Vishnubhatla

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
* Give full credit to the author
* Properly cite this repository

> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
