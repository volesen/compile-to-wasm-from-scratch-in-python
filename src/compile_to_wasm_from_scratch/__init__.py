import argparse
from .scanner import scanner
from .parser import CTWFSParser, ParserError
from .compiler import compile_prog, serialize_sexpr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("r"))
    args = parser.parse_args()

    tokens, remainder = scanner.scan(args.input.read())

    if remainder:
        print(f"Unrecognized input: {remainder}")
        return 1

    parser = CTWFSParser(tokens)

    try:
        program = parser.parse()
    except ParserError as e:
        print(e)
        print(f"{parser.tokens[parser.current:]=}")
        raise
        return 1

    wat = compile_prog(program)

    print(serialize_sexpr(wat))

    return 0
