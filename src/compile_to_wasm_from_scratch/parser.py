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

        token = self.tokens[self.current]

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
        self.consume("FN", "Expected 'fn' keyword")
        name = self.consume("IDENT", "Expected function name")
        parameters = self.parameter_list()
        self.consume("LBRACE", "Expected '{' before function body")
        body = self.finish_block_expression()
        return ast.FunctionDeclaration(name.value, parameters, body)

    def parameter_list(self):
        params = []

        self.consume("LPAREN", "Expected '(' after function name")

        while not self.is_at_end():
            if self.match("RPAREN"):
                break

            param = self.consume("IDENT", "Expected parameter name")
            params.append(param.value)

            if not self.match("COMMA"):
                self.consume("RPAREN", "Expected ')' after parameter list")
                break

        return params

    def expression(self):
        return self.term()

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

        elif self.match("LBRACE"):
            return self.finish_block_expression()

        elif self.match("IF"):
            return self.finish_if_expression()

        elif name := self.match("IDENT"):
            if self.match("LPAREN"):
                args = self.finish_argument_list()
                return ast.Call(name.value, args)

            return ast.Variable(name.value)

        elif number := self.match("NUMBER"):
            return ast.Number(number.value)

        raise ParserError("Expected expression")

    def finish_block_expression(self):
        stmts = []
        expr = None

        while not self.is_at_end() and not self.match("RBRACE"):
            if self.match("LET"):
                stmt = self.finish_let_statement()
                stmts.append(stmt)
                continue

            # Either an expression statement or the return expression
            expr = self.expression()

            if self.match("SEMICOLON"):
                stmt = ast.ExpressionStatement(expr)
                stmts.append(stmt)
                expr = None
                continue

        if not expr:
            raise ParserError(
                "Expected a last expression in block. Maybe you added a semicolon after the last expression?"
            )

        return ast.Block(stmts, expr)

    def finish_let_statement(self):
        name = self.consume("IDENT", "Expected variable name")
        self.consume("EQUALS", "Expected '=' after variable name")
        value = self.expression()
        self.consume("SEMICOLON", "Expected ';' after expression")
        return ast.Let(name.value, value)

    def finish_if_expression(self):
        condition = self.expression()
        self.consume("LBRACE", "Expected '{' after if condition")
        then_block = self.finish_block_expression()
        self.consume("ELSE", "Expected 'else' keyword after then block")
        self.consume("LBRACE", "Expected '{' after else keyword")
        else_block = self.finish_block_expression()

        return ast.If(condition, then_block, else_block)

    def finish_argument_list(self):
        args = []

        while not self.is_at_end() and not self.match("RPAREN"):
            arg = self.expression()
            args.append(arg)

            if not self.match("COMMA"):
                self.consume("RPAREN", "Expected ')' after argument list")
                break

        return args
