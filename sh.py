#!/usr/bin/env python3


from typing import Optional


class BashFormatted:
    """
    Call Bash commands easily
    This class wraps subprocess.run()

    Syntax: stdout = Bash()("echo hello")
    or      "echo hello" >> Bash()
    or      "ssh user@host" >> Bash(interactive=True)
    """

    def __init__(self, interactive: bool = False) -> None:
        self.__i = interactive

    def __call__(self, command: str) -> Optional[str]:
        if self.__i:
            return self.interactive(command)
        else:
            return self.execute(command)

    def __rrshift__(self, command: str) -> Optional[str]:
        return self.__call__(command)

    @staticmethod
    def interactive(command: str) -> None:
        from subprocess import run

        run(["bash", "-c", command], check=True)

    @staticmethod
    def execute(command: str) -> str:
        from subprocess import run

        p = run(["bash", "-c", command], capture_output=True, text=True)
        if p.returncode != 0:
            raise Exception((p.stderr or p.stdout or f"Errno {p.returncode}").strip())
        return p.stdout.strip()


class Bash:
    def __init__(self, interactive=False):
        self.__i = interactive
    def __call__(self, command):
        if self.__i: return Bash.interactive(command)
        else:        return Bash.execute(command)
    def __rrshift__(self, command):
        return self.__call__(command)
    def interactive(command):
        from subprocess import run
        run(["bash", "-c", command], check=True)
    def execute(command):
        from subprocess import run
        p = run(["bash", "-c", command], capture_output=True, text=True)
        if p.returncode != 0: raise Exception((p.stderr or p.stdout or f"Errno {p.returncode}").strip())
        return p.stdout.strip()


def main():
    out = "echo Hello world" >> Bash()
    print(out)


if __name__ == "__main__":
    main()
