import compile_to_wasm_from_scratch.ast as ast


class ParserError(Exception):
    pass


class Parser:
    tokens: list
    current: int

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.current = 0

    def is_at_end(self):
        return self.current >= len(self.tokens)

    def consume(self, token_type: str, msg: str | None = None):
        """
        Consume the current token if it is of the given type, otherwise raise an error.
        """

        try:
            token = self.tokens[self.current]
        except IndexError:
            raise ParserError(f"Unexpected end of input, expected {token_type}")

        if token.type != token_type:
            raise ParserError(
                msg or f"Expected token of type {token_type}, got {token.type}"
            )

        self.current += 1

        return token

    def match(self, *token_types: str):
        """
        Optionally consume one of the given token types if the current token is one of them.
        """
        for token_type in token_types:
            try:
                return self.consume(token_type)
            except ParserError:
                continue


class CTWFSParser(Parser):
    def parse(self):
        return self.program()

    def program(self):
        decls = []

        while not self.is_at_end():
            decls.append(self.function_declaration())

        return ast.Program(decls)

    def function_declaration(self):
        self.consume("FN", "Expected 'fn' keyword to start function declaration")
        name = self.consume("IDENT", "Expected function name")
        parameters = self.parameter_list()
        self.consume("EQUALS", "Expected '=' after parameter list")
        body = self.expression()

        return ast.FunctionDeclaration(name.value, parameters, body)

    def parameter_list(self):
        params = []

        self.consume("LPAREN", "Expected '(' after function name")

        while not self.is_at_end() and not self.match("RPAREN"):
            param = self.consume("IDENT", "Expected parameter name")
            params.append(param.value)

            if not self.match("COMMA"):
                self.consume("RPAREN", "Expected ')' after parameter list")
                break

        return params

    def expression(self):
        if self.match("IF"):
            condition = self.expression()
            self.consume("THEN", "Expected 'then' keyword after condition")
            then_expr = self.expression()
            self.consume("ELSE", "Expected 'else' keyword after then expression")
            else_expr = self.expression()

            return ast.If(condition, then_expr, else_expr)

        if self.match("LET"):
            name = self.consume("IDENT", "Expected variable name")
            self.consume("EQUALS", "Expected '=' after variable name")
            value = self.expression()
            self.consume("IN", "Expected 'in' after expression")
            expr = self.expression()

            return ast.Let(name.value, value, expr)

        return self.sequence()

    def sequence(self):
        expr = self.term()

        while self.match("SEMICOLON"):
            right = self.term()
            expr = ast.Sequence(expr, right)

        return expr

    def term(self):
        expr = self.factor()

        while op := self.match("PLUS", "MINUS"):
            right = self.factor()
            expr = ast.BinaryOp(op.type, expr, right)

        return expr

    def factor(self):
        expr = self.unary()

        while op := self.match("STAR", "SLASH"):
            right = self.unary()
            expr = ast.BinaryOp(op.type, expr, right)

        return expr

    def unary(self):
        if op := self.match("MINUS"):
            right = self.unary()
            return ast.UnaryOp(op.type, right)

        return self.primary()

    def primary(self):
        if self.match("LPAREN"):
            expr = self.expression()
            self.consume("RPAREN", "Expected ')' after expression")
            return expr

        elif name := self.match("IDENT"):
            if self.match("LPAREN"):
                args = self.finish_argument_list()
                return ast.Call(name.value, args)

            return ast.Variable(name.value)

        elif number := self.match("NUMBER"):
            return ast.Number(number.value)

        raise ParserError("Expected expression")

    def finish_argument_list(self):
        args = []

        while not self.is_at_end() and not self.match("RPAREN"):
            arg = self.expression()
            args.append(arg)

            if not self.match("COMMA"):
                self.consume("RPAREN", "Expected ')' after argument list")
                break

        return args
