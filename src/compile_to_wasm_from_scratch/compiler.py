import compile_to_wasm_from_scratch.ast as ast


class CompilerError(Exception):
    pass


def compile_prog(prog):
    ftab = {decl.name: i for i, decl in enumerate(prog.declarations)}

    return [
        "module",
        *(compile_decl(ftab, decl) for decl in prog.declarations),
    ]


def compile_decl(ftab, decl):
    match decl:
        case ast.FunctionDeclaration(name, parameters, body):
            vtab = {param: i for i, param in enumerate(parameters)}

            return [
                "func",
                ["export", '"' + name + '"'],
                *(["param", "i32"] for _ in parameters),
                ["result", "i32"],
                *(["local", "i32"] for _ in range(count_locals(body))),
                *compile_expr(ftab, vtab, body),
            ]


def compile_expr(ftab, vtab, expr):
    match expr:
        case ast.Number(value):
            return ["i32.const", value]

        case ast.Variable(name):
            return ["local.get", vtab[name]]

        case ast.UnaryOp("-", operand):
            return ["i32.const", 0, *compile_expr(ftab, vtab, operand), "i32.sub"]

        case ast.BinaryOp(operator, left, right):
            return (
                compile_expr(ftab, vtab, left)
                + compile_expr(ftab, vtab, right)
                + compile_binary_op(operator)
            )

        case ast.If(condition, then_branch, else_branch):
            return [
                *compile_expr(ftab, vtab, condition),
                [
                    "if",
                    ["result", "i32"],
                    ["then", *compile_expr(ftab, vtab, then_branch)],
                    ["else", *compile_expr(ftab, vtab, else_branch)],
                ],
            ]

        case ast.Call(name, arguments):
            return [
                *sum((compile_expr(ftab, vtab, arg) for arg in arguments), []),
                "call",
                ftab[name],
            ]

        case ast.Sequence(first, second):
            return [
                *compile_expr(ftab, vtab, first),
                "drop",
                *compile_expr(ftab, vtab, second),
            ]

        case ast.Let(name, value, body):
            slot = len(vtab)

            return [
                *compile_expr(ftab, vtab, value),
                "local.set",
                slot,
                *compile_expr(ftab, {**vtab, name: slot}, body),
            ]

        case _:
            raise ValueError(f"Unknown expression type: {expr}")


def compile_binary_op(operator):
    match operator:
        case "+":
            return ["i32.add"]
        case "-":
            return ["i32.sub"]
        case "*":
            return ["i32.mul"]
        case "/":
            return ["i32.div_s"]
        case "=":
            return ["i32.eq"]
        case _:
            raise ValueError(f"Unknown binary operator: {operator}")


def flat_map(f, xs):
    return [y for x in xs for y in f(x)]


def count_locals(expr) -> int:
    """
    Counts the maximum number of local variables needed to evaluate the given expression.
    """
    match expr:
        case ast.Number(_) | ast.Variable(_):
            return 0

        case ast.UnaryOp(_, operand):
            return count_locals(operand)

        case ast.BinaryOp(_, left, right):
            return max(count_locals(left), count_locals(right))

        case ast.Sequence(first, second):
            return max(count_locals(first), count_locals(second))

        case ast.If(condition, then_branch, else_branch):
            return max(
                count_locals(condition),
                count_locals(then_branch),
                count_locals(else_branch),
            )

        case ast.Call(_, arguments):
            return max(count_locals(arg) for arg in arguments)

        case ast.Let(_, value, body):
            return max(count_locals(value), 1 + count_locals(body))

        case _:
            raise ValueError(f"Unknown expression type: {expr}")


def serialize_sexpr(sexpr):
    if isinstance(sexpr, list):
        return f"({' '.join(serialize_sexpr(x) for x in sexpr)})"
    return str(sexpr)
