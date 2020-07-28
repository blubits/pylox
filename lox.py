"""The Lox interpreter.

:Author:     Maded Batara III
"""

import sys
import scanner

class Lox:
    """A wrapper class for the Lox interpreter.

    The Interpreter class serves as a front-end for the execution of Lox code.
    Code is passed into the function through the run() method and is executed
    on the fly. Errors in the code will cause an immediate stop in execution of
    the run() command, and the cause of the error will be printed to stderr
    (instead of raising an exception, since this is meant to be a front-end class).

    Attributes:
        has_error (bool): Flag for an error in the execution of code.
    """

    def __init__(self):
        self.has_error = False

    def run(self, string: str):
        # Reset error state after every run
        self.has_error = False
        sc = scanner.Scanner(string, self.error)
        print(' '.join(str(x) for x in sc.scan_tokens()))

    def error(self, line: str, message: str):
        self.report(line, "", message)

    def report(self, line: str, where: str, message: str):
        print("[line {0}] Error {1}: {2}".format(
            line, where, message), file=sys.stderr)
        self.has_error = True
