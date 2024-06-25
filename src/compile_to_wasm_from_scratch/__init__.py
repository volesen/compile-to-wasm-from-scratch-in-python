import argparse
from .scanner import scanner
from .parser import CTWFSParser, ParserError
from .compiler import compile_prog


def serialize_sexpr(sexpr):
    if isinstance(sexpr, list):
        return f"({' '.join(serialize_sexpr(x) for x in sexpr)})"
    return str(sexpr)


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
        # print(program)
    except ParserError as e:
        print(e)
        return 1

    wat = compile_prog(program)

    print(serialize_sexpr(wat))

    return 0
