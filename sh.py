#!/usr/bin/env python3

import subprocess

class Bash:
    def __init__(self, printStdout = True, printDebug = False):
        self._printStdoutEnabled = printStdout
        self._printDebugEnabled = printDebug
    def __call__(self, command: str) -> str:
        self._printDebug("[[call]]")
        return self.execute(command)
    def __rrshift__(self, command: str) -> str:
        self._printDebug("[[rrshift]]")
        return self.execute(command)
    def __lshift__(self, command: str) -> str:
        self._printDebug("[[lshift]]")
        return self.execute(command)
    def _printDebug(self, string: str) -> None:
        if self._printDebugEnabled:
            print(string)
    def _expand(self, command: str) -> str:
        command = command.replace("~", "$HOME")
        result = ""
        for i, cmd in enumerate(command.split('|')):
            if (i > 0):
                result += ' | '
            result += subprocess.check_output(["bash", "-c", f"echo {cmd}"], text=True).strip()
        self._printDebug(f"command: {command}, expanded: {result}")
        return result
    def execute(self, command: str) -> str:
        if (type(command) != str): raise Exception(f"Expected a str, got: {type(command)}!")
        if '$(' in command or '`' in command: raise Exception(f"Subcommands are prohibited!")
        if ';' in command: raise Exception(f"Semicolons are prohibited: {command}!")
        if command.strip().endswith('&'): raise Exception(f"Background execution is prohibited: {command}!")
        if '[' in command or ']' in command or '!' in command: raise Exception(f"Conditional execution is prohibited: {command}!")
        if any(c in command for c in ['$', '=', '\\', '"', "'", '#', '(', ')', '{', '}', '?', '*']): 
            print(f"Warning: special characters may introduce unexpected behaviour!")
        
        command = self._expand(command)
        if '|' in command: raise Exception(f"Piping is not implemented: {command}!")
        if '<' in command or '>' in command: raise Exception(f"IO redirection is not implemented: {command}!")
        cmds = command.split()
        if not cmds: raise Exception(f"Empty command: {command}!")
        self._printDebug(f"cmds: {cmds}")

        process = subprocess.run(cmds, shell=False, capture_output=True, text=True)
        stdout = str.strip(process.stdout)
        self._printDebug(f"stdout: {stdout}")
        self._printDebug(f"stderr: {str.strip(process.stderr)}")
        if process.returncode != 0:
            raise Exception(f"Errno {process.returncode}: {command}!")
        if self._printStdoutEnabled:
            print(stdout)
        return stdout


def main():
    bash = Bash()
    'echo Hello world' >> bash


if __name__ == "__main__":
    main()