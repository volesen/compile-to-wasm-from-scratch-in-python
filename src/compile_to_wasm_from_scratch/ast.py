from dataclasses import dataclass


class Node:
    pass


class Expression(Node):
    pass


class Declaration(Node):
    pass


@dataclass
class Number(Expression):
    value: int


@dataclass
class Variable(Expression):
    name: str


@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression


@dataclass
class BinaryOp(Expression):
    operator: str
    left: Expression
    right: Expression


@dataclass
class Let(Expression):
    name: str
    value: Expression
    body: Expression


@dataclass
class If(Expression):
    condition: Expression
    then_branch: Expression
    else_branch: Expression


@dataclass
class Call(Expression):
    name: str
    arguments: list[Expression]


@dataclass
class Sequence(Expression):
    first: Expression
    second: Expression


@dataclass
class FunctionDeclaration(Declaration):
    name: str
    parameters: list[str]
    body: Expression


@dataclass
class Program:
    declarations: list[Declaration]
