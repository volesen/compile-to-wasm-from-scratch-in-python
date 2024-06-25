import compile_to_wasm_from_scratch.symbol_table as symbol_table
import compile_to_wasm_from_scratch.ast as ast


class CompilerError(Exception):
    pass


def compile_prog(prog):
    ftab = symbol_table.SymbolTable()

    for i, decl in enumerate(prog.declarations):
        ftab[decl.name] = i

    return [
        "module",
        *(compile_decl(ftab, decl) for decl in prog.declarations),
    ]


def compile_decl(ftab, decl):
    match decl:
        case ast.FunctionDeclaration(name, parameters, body):
            vtab = symbol_table.SymbolTable()

            for i, param in enumerate(parameters):
                vtab[param] = i

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

        case ast.UnaryOp(operator, operand):
            return compile_expr(ftab, vtab, operand) + compile_unary_op(operator)

        case ast.BinaryOp(operator, left, right):
            return (
                compile_expr(ftab, vtab, left)
                + compile_expr(ftab, vtab, right)
                + compile_binary_op(operator)
            )

        case ast.Block(statements, expression):
            vtab = vtab.new_scope()

            return sum(
                (compile_stmt(ftab, vtab, stmt) for stmt in statements), []
            ) + compile_expr(ftab, vtab, expression)

        case ast.If(condition, then_block, else_block):
            return [
                *compile_expr(ftab, vtab, condition),
                [
                    "if",
                    ["result", "i32"],
                    ["then", *compile_expr(ftab, vtab, then_block)],
                    ["else", *compile_expr(ftab, vtab, else_block)],
                ],
            ]

        case ast.Call(name, arguments):
            return [
                *(compile_expr(ftab, vtab, arg) for arg in arguments),
                "call",
                ftab[name],
            ]

        case _:
            raise ValueError(f"Unknown expression type: {expr}")


def compile_stmt(ftab, vtab, stmt):
    match stmt:
        case ast.Let(name, value):
            vtab[name] = len(vtab)

            return [
                *compile_expr(ftab, vtab, value),
                "local.set",
                vtab[name],
            ]

        case ast.ExpressionStatement(expr):
            return [
                *compile_expr(ftab, vtab, expr),
                "drop",
            ]

        case _:
            raise ValueError(f"Unknown statement type: {stmt}")


def compile_unary_op(operator):
    match operator:
        case "MINUS":
            return ["i32.neg"]
        case _:
            raise ValueError(f"Unknown unary operator: {operator}")


def compile_binary_op(operator):
    match operator:
        case "PLUS":
            return ["i32.add"]
        case "MINUS":
            return ["i32.sub"]
        case "STAR":
            return ["i32.mul"]
        case "SLASH":
            return ["i32.div_s"]
        case _:
            raise ValueError(f"Unknown binary operator: {operator}")


def count_locals(expr):
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

        case ast.Block(statements, expression):
            return sum(count_locals(stmt) for stmt in statements) + count_locals(
                expression
            )

        case ast.If(condition, then_block, else_block):
            return max(
                count_locals(condition),
                count_locals(then_block),
                count_locals(else_block),
            )

        case ast.Call(_, arguments):
            return max(count_locals(arg) for arg in arguments)

        case ast.Let(_, value):
            return 1 + count_locals(value)

        case ast.ExpressionStatement(expr):
            return count_locals(expr)

        case _:
            raise CompilerError("Unknown node type")
