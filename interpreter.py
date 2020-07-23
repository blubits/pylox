"""
The Lox interpreter.

:Author:     Maded Batara III
"""

import sys

class Interpreter:
    """
    A wrapper class for the Lox interpreter.

    The Interpreter class serves as a front-end for the execution of Lox code.
    Code is passed into the function through the run() method and is executed
    on the fly. Errors in the code will cause an immediate stop in execution of
    the run() command, and the cause of the error will be printed to stderr
    (instead of raising an exception, since this is meant to be a front-end class).
    """

    def __init__(self):
        self.has_error = False

    def run(self, string):
        # Reset error state after every run
        self.has_error = False
        print(string)

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print("[line {0}] Error {1}: {2}".format(
            line, where, message), file=sys.stderr)
