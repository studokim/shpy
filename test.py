#!/usr/bin/env python3

from sh import Bash

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
                raise Exception(f"Failed: expected={expected}, result={result}!")
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

def tests():
    bash = 'Bash(printStdout=False, printDebug=True)'
    test = Test()

    test + (f'{bash}("echo $HOME")', "/home/kim")
    test + (f'{bash} << "echo foo"', "foo")
    test + (f'"echo $bar" >> {bash}', '')

    test + (f'"alias" >> {bash}', FileNotFoundError(2, "No such file or directory"))
    test + (f'"echo `rm ~/*`" >> {bash}', Exception('Subcommands are prohibited!'))
    test + f'"ls -l" >> {bash}'
    test + f'"ls -l ~/*" >> {bash}'
    test + f'"/usr/bin/grep alias /home/kim/.zshrc" >> {bash}'
    test + f'"/usr/bin/grep alias ~/.zshrc" >> {bash}'
    test + f'"/usr/bin/grep alias $HOME/.zshrc" >> {bash}'
    
    test + (f'{bash} << "echo foo | grep foo"', Exception('Piping is not implemented: echo foo | grep foo!'))
    test + (f'"dmesg | grep hda" >> {bash}', Exception('Piping is not implemented: dmesg | grep hda!'))
    test + (f'"    " >> {bash}', Exception('Empty command: !'))
    
    test.verdict()

if __name__ == "__main__":
    tests()