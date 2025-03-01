# shpy

Call Bash from Python with minimal effort.

## Motivation

I wanted to call command-line-oriented programs from Python as easy as I do it from my terminal. For what?

- It is easier to write a robust and maintainable script in Python, than in Bash.
- These programs are already installed and known, so why install duplicating Python wrappers and libraries as well? Why learn a new specific syntax and a calling convention for each?

## Usage

To make use of `sh.py` when writing a new script,

1. copy `sh.py` into `my-new-script.py`;
2. in `main()`, create an object `bash = Bash()` and then use it: `'find ~ -type d -name ".log"' >> bash`;
3. implement the logic;
4. done.

The following syntax is supported:

```python
bash = Bash(printStdout=False)          # capture stdout to only save it into variables

output = 'echo hello first' >> bash     # output=="hello first"
output = bash << 'echo hello second'    # output=="hello second"
output = bash('echo hello third')       # output=="hello third"

exception = 'echo a | grep b' >> bash   # Exception: the command returns non-zero

# Exception: complex constructions like semicolons and subcommands
# are explicitly prohibited, use Python control flow instead
prohibited = 'sleep 1 ; echo $(echo a)' >> bash
```