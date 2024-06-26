import argparse
from .parser import parse
from .compiler import compile_prog, serialize_sexpr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("r"))

    args = parser.parse_args()

    program = parse(args.input)

    wat = compile_prog(program)

    print(serialize_sexpr(wat))

    return 0
