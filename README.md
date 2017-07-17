# A Simple (Custom) Lisp Interpreter

**SCLI** (*A Simple (Custom) Lisp Interpreter*) is a custom Lisp interpreter built in Python 2.7.x. It is meant to follow the language I developed that is an offshoot of Lisp. For more information you can head over to [sv4u.github.io/scli-interpreter](https://sv4u.github.io/scli-interpreter/)

## Motivation

I have been interested in creating a programming language for the past year. So, I decided to read a bunch of manuals and then one day I finally tried writing one. This is the outcome of that day.

## Releases

Currently, we have the alpha release here: [github.com/sv4u/scli-interpreter/releases/tag/alpha](https://github.com/sv4u/scli-interpreter/releases/tag/alpha)

## TODO
- [ ] Create an executable version of [SCLI.py](https://github.com/sv4u/lisp-interpreter/blob/master/SCLI.py)
- [x] Add more default mathematical functions to the SCLI language
	- This was completed by adding the mathematics library
- [ ] Create a more user friendly interface for programming (a portable GUI)
- [x] Create full flegded documentation
	- This documentation is only going to grow as features are added
- [ ] Add a Strings, Equation Solving, and Statistics Library	

### Mathematical Functions Library - **DONE**

This language is meant to be mathematics heavy. Since I am quite interested in computer science research, SCLI is primarily a research language. Currently the list of mathematical functions to implement are:

| Function | Description | Status |
| :------- | :---------- | -----: |
| Modular exponentiation | A simple `x^y mod z` operator | Done |
| Square Root | A simple square root operator | Done (with added `nroot` operator) |
| Ceiling and Floor | `ceil(x)` and `floor(x)` | Done |
| Absolute Value | `abs(x)` | Done |
| Logarithms | `log(x)` of multiple bases | Done (three types of logs: base e, 2, and n) |

### String Functions Library - **DONE**

The functions to add to this library are:

| Function | Description | Status |
| :------- | :---------- | -----: |
| String Concatenation | Concatenate two strings | Done |
| Substring | Substring between two values | Done |
| Character At | Finds the specific character at an index | Done |
| Length | Get the length of a specific string | Done |
| Split | Split a string on a regular expression | Done |

### Equation Solving Library - **NOT STARTED**

The functions to be added to this library are:

| Function | Description | Status |
| :------- | :---------- | -----: |
| Linear Solver | Solves a linear equation | Not started |
| Quadratic Solver | Solves a quadratic equation | Not started |
| Cubic Solver | Solves a cubic equation | Not started |
| Exponential Solver | Solves an exponential equation | Not started |
| Logarithmic Solver | Solves a logarithmic equation | Not started |
| Polynomial Solver | Solves a polynomial equation | Not started |
| Derivative Calculator | Calculates derivative | Not started |
| Integral Calculator | Calculate integral | Not started |
| Polynomial Factoring | Factors a polynomial expression | Not started |

### Statistic Analysis Library - **NOT STARTED**

Some basic statistic analysis functions to be added are:

| Function | Description | Status |
| :------- | :---------- | -----: |
| Standard T-test | Computes a standard T-test | Not started |
| Z-score Calculator | Computes a Z-score | Not started |
| ANNOVA Calculator | Computes an ANNOVA | Not started |
| Multiple Distribution Calculator | Calculates multiple discributions | Not started |

### SCLI Editor

Similarly to how Python is bundled with IDLE, I would like to create a IDE for SCLI. This is currently the most long term goal as it will take the longest about of time.

### Documentation

Adding a documentation to SCLI for learning how to use it and how it is extremely similar to Lisp would not only help me but also new users.

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
