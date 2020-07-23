"""Main executable for the pylox interpreter.

:Author:     Maded Batara III
"""

import interpreter
import argparse
import sys

def run_file(filename, iptr, parser):
    """Executes code from a file.

    Args:
        filename (str): Filename of code to execute.
        iptr (Interpreter): Interpreter to pass code into.
        parser (ArgumentParser): ArgumentParser of the executable, used to output
            exec-level errors (e.g. file not found).
    """
    try:
        with open(filename) as source:
            iptr.run(source.read())
            if iptr.error:
                sys.exit(2)
    except FileNotFoundError:
        parser.error("File not found: {0}".format(filename))

def run_prompt(iptr, parser):
    """Creates a prompt (REPL) for executing code.

    Args:
        iptr (Interpreter): Interpreter to pass code into.
        parser (ArgumentParser): ArgumentParser of the executable, used to output
            exec-level errors (e.g. file not found).
    """
    print("pylox version alpha")
    while True:
        try:
            line = input(">>> ")
            iptr.run(line)
        except KeyboardInterrupt:
            sys.exit(0)

def main():
    iptr = interpreter.Interpreter()
    # set up cmd arguments
    parser = argparse.ArgumentParser(
        description='The Lox programming language.')
    parser.add_argument('filename', metavar='file', type=str, nargs='?', default=None,
                        help='Filename of the script to be run. If not specified, runs an interactive prompt.')

    args = parser.parse_args()
    if args.filename is None:
        run_prompt(iptr, parser)
    else:
        run_file(args.filename, iptr, parser)

if __name__ == "__main__":
    main()
