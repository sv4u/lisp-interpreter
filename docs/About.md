# A Simple (Custom) Lisp Interpreter

**SCLI** (*A Simple (Custom) Lisp Interpreter*) is a custom Lisp interpreter built in Python 2.7.x. It is meant to follow the language I developed that is an offshoot of Lisp.

## Usage

In the Python console, import the [interpreter](https://github.com/sv4u/lisp-interpreter/blob/master/SCLI.py)
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

## TODO
- [x] Implement Lisp in Python
- [ ] Add more depth to the SCLI language
- [ ] Create a more user friendly interface for programming
- [ ] Fully finish language customization
- [ ] Add cryptographic functions
- [ ] Create full flegded documentation

## Language Specifications

Currently, this language is extremely basic. The main goal of this language is to be simple and pure. Here is a table of what has been and has not been implemented:

| Language Spec. | Date implemented |
| --- | ---: |
| Standard math | 01 - 13 - 2017 |
| Data types | 01 - 13 - 2017 |
| Proper exit from repl() | 03 - 28 - 2017 |
| Advanced math |	*currently in the works (short-term)* |
| For & While loops | *currently in the works (long-term)* |

More information will come when I have a bit more time to clearly layout a plan for this language!