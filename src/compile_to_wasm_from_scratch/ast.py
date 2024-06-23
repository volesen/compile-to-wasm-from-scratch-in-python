from dataclasses import dataclass


class Node:
    pass


class Expression(Node):
    pass


class Statement(Node):
    pass


class Declaration(Node):
    pass


@dataclass
class Let(Statement):
    name: str
    value: Expression


@dataclass
class ExpressionStatement(Statement):
    expression: Expression


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
class Block(Expression):
    statements: list[Statement]
    expression: Expression


@dataclass
class If(Expression):
    condition: Expression
    then_block: Block
    else_block: Block


@dataclass
class Call(Expression):
    name: str
    arguments: list[Expression]


@dataclass
class FunctionDeclaration(Declaration):
    name: str
    parameters: list[str]
    body: Block


@dataclass
class Program:
    declarations: list[Declaration]
