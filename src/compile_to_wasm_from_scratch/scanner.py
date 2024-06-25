import re
from typing import Any, Callable
from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: Any


def skip(scanner, token):
    return None


def make_rule(type: str, to_value: Callable[[str], Any] = lambda x: x):
    def inner(scanner, token):
        return Token(type, to_value(token))

    return inner


scanner = re.Scanner(
    [
        (r"\s+", skip),
        # Skip newlines
        (r"\n+", skip),
        # Keywords
        (r"fn", make_rule("FN")),
        (r"let", make_rule("LET")),
        (r"in", make_rule("IN")),
        (r"if", make_rule("IF")),
        (r"then", make_rule("THEN")),
        (r"else", make_rule("ELSE")),
        # Punctuation
        (r"\(", make_rule("LPAREN")),
        (r"\)", make_rule("RPAREN")),
        (r"\,", make_rule("COMMA")),
        (r"\;", make_rule("SEMICOLON")),
        # Operators
        (r"\+", make_rule("PLUS")),
        (r"\-", make_rule("MINUS")),
        (r"\*", make_rule("STAR")),
        (r"\/", make_rule("SLASH")),
        (r"\=", make_rule("EQUALS")),
        # Numbers
        (r"\d+", make_rule("NUMBER", int)),
        # Identifiers
        (r"[a-zA-Z_][a-zA-Z0-9_]*", make_rule("IDENT")),
    ]
)
