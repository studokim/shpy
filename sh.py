#!/usr/bin/env python3

import subprocess

class Bash:
    _verboseEnabled = False
    _printStdout = True
    def __call__(self, command: str) -> str:
        Bash._verbose("[[call]]")
        return Bash.execute(command)
    def __rrshift__(self, command: str) -> str:
        Bash._verbose("[[rrshift]]")
        return Bash.execute(command)
    def __lshift__(self, command: str) -> str:
        Bash._verbose("[[lshift]]")
        return Bash.execute(command)
    def _verbose(string: str) -> None:
        if Bash._verboseEnabled:
            Bash._verbose(string)
    def _expand(command: str) -> str:
        command = command.replace("~", "$HOME")
        return subprocess.check_output(["bash", "-c", f'echo {command}'], text=True).strip()
    def execute(command: str) -> str:
        if (type(command) != str): raise Exception(f"Expected a str, got: {type(command)}!")
        if '$(' in command or '`' in command: raise Exception(f"Subcommands are not implemented!")
        if ';' in command: raise Exception(f"Command separation is not implemented: {command}!")
        if '|' in command: raise Exception(f"Piping is not implemented: {command}!")
        if '&' in command: raise Exception(f"Background execution is not implemented: {command}!")
        if '=' in command: raise Exception(f"Variables are not implemented: {command}!")
        if '!' in command: raise Exception(f"Negation is not implemented: {command}!")
        if '[' in command or ']' in command: raise Exception(f"Conditional execution is not implemented: {command}!")
        if '<' in command or '>' in command: raise Exception(f"IO redirection is not implemented: {command}!")
        if any(c in command for c in ['$', '\\', '"', "'", '#', '(', ')', '{', '}', '?', '*']): 
            print(f"Warning: special characters may introduce unexpected behaviour!")
        command = Bash._expand(command)
        cmds = command.split()
        if not cmds: raise Exception(f"Empty command: {command}!")
        Bash._verbose(f"cmds: {cmds}")

        process = subprocess.run(cmds, shell=False, capture_output=True, text=True)
        stdout = str.strip(process.stdout)
        Bash._verbose(f"stdout: {stdout}")
        Bash._verbose(f"stderr: {str.strip(process.stderr)}")
        if process.returncode != 0:
            raise Exception(f"Errno {process.returncode}: {command}!")
        if Bash._printStdout:
            print(stdout)
        return stdout

def tests():
    class Test:
        def __init__(self):
            self._failed = []
            self._total = 0
            self._divider = '-' * 40
            self._printFailedInVerdict = False
        def __add__(self, expr):
            print(self._divider)
            print(f"Test #{self._total}:\t{str(expr)}")
            expected = None
            if type(expr) is tuple:
                expr, expected = expr
            if type(expr) is not str:
                raise Exception(f"Test is a string expression and, optionally, the expected result. Got: {type(expr)}!")
            try:
                result = eval(expr)
                if expected is not None and result != expected:
                    raise Exception(f"Failed: expected={expected}, result={result}")
            except Exception as exception:
                if not isinstance(expected, Exception) or expected.args != exception.args:
                    self._failed.append((self._total, expr, exception))
                    if not self._printFailedInVerdict:
                        from traceback import format_exc
                        print(format_exc())
            self._total += 1
        def verdict(self):
            print(self._divider)
            passed = self._total - len(self._failed)
            print(f"Tests passed: {passed}/{self._total}")
            if self._failed and self._printFailedInVerdict:
                print("Failed:")
                for num, expr, exception in self._failed:
                    print(f"\t#{num}: {str(expr):<50}\t{exception}")

    test = Test()

    test + ('Bash()("echo $HOME")', "/home/kim")
    test + ('Bash() << "echo foo"', "foo")
    test + ('"echo $bar" >> Bash()', '')

    test + ('"alias" >> Bash()', FileNotFoundError(2, "No such file or directory"))
    test + ('"echo `rm ~/*`" >> Bash()', Exception('Subcommands are not implemented!'))
    test + '"ls -l" >> Bash()'
    test + '"ls -l ~/*" >> Bash()'
    test + '"/usr/bin/grep alias /home/kim/.zshrc" >> Bash()'
    test + '"/usr/bin/grep alias ~/.zshrc" >> Bash()'
    test + '"/usr/bin/grep alias $HOME/.zshrc" >> Bash()'
    
    test + ('Bash() << "echo foo | grep foo"', Exception('Piping is not implemented: echo foo | grep foo!'))
    test + ('"dmesg | grep hda" >> Bash()', Exception('Piping is not implemented: dmesg | grep hda!'))
    test + ('"    " >> Bash()', Exception('Empty command: !'))
    
    test.verdict()

if __name__ == "__main__":
    tests()
