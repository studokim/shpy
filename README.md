# shpy

Call Bash from Python with minimal effort.

## Motivation

I wanted to call command-line-oriented programs from Python as easy as I do it from my terminal. For what?

- It is easier to write a robust and maintainable script in Python, than in Bash.
- These programs are already installed and known, so why install duplicating Python wrappers and libraries as well? Why learn a new specific syntax and a calling convention for each?

## Usage

To make use of `sh.py` when writing a new script,

1. copy `sh.py` into `my-new-script.py`;
2. in `main()`, create an object `bash = Bash()` and then use it: `"find ~ -type d -name '.log'" >> bash`;
3. implement the logic;
4. done.

Or you can just copy-and-paste the `Bash` class into any existing file. The goal was to make it as succinct as possible, so without docstring it's only 16 LOC.

The following syntax is supported:

```python
bash  = Bash()
bashi = Bash(interactive=True)

output = 'echo hello first' >> bash    # output=="hello first"
output = bash('echo hello second')     # output=="hello second"

exception = 'echo a | grep b' >> bash  # Exception: Errno 1 (means "not found" in grep)

"ssh user@host" >> bashi               #  for interactive applications like ssh, stdout/stderr is not captured
```

## These projects are nice too

- [xonsh/xonsh](https://github.com/xonsh/xonsh)
- [Apakottur/shpyx](https://github.com/Apakottur/shpyx)
- [toastdriven/shell](https://github.com/toastdriven/shell)
