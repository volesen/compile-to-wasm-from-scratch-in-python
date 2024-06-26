#!/usr/bin/env python3.8
# @generated by pegen from src/compile_to_wasm_from_scratch/ctwfs.gram

import ast
import sys
import tokenize

from typing import Any, Optional

from pegen.parser import memoize, memoize_left_rec, logger, Parser

import traceback
from typing import Generator
from pegen.tokenizer import Tokenizer
import compile_to_wasm_from_scratch.ast as ast

# Keywords and soft keywords are listed at the end of the parser definition.
class GeneratedParser(Parser):

    @memoize
    def start(self) -> Optional[Any]:
        # start: decl* $
        mark = self._mark()
        if (
            (decls := self._loop0_1(),)
            and
            (self.expect('ENDMARKER'))
        ):
            return ast . Program ( decls or [] );
        self._reset(mark)
        return None;

    @memoize
    def decl(self) -> Optional[Any]:
        # decl: 'fn' NAME '(' params? ')' '=' expr
        mark = self._mark()
        if (
            (self.expect('fn'))
            and
            (name := self.name())
            and
            (self.expect('('))
            and
            (params := self.params(),)
            and
            (self.expect(')'))
            and
            (self.expect('='))
            and
            (expr := self.expr())
        ):
            return ast . FunctionDeclaration ( name . string , params or [] , expr );
        self._reset(mark)
        return None;

    @memoize
    def params(self) -> Optional[Any]:
        # params: NAME ((',' NAME))*
        mark = self._mark()
        if (
            (name := self.name())
            and
            (names := self._loop0_2(),)
        ):
            return [name . string] + names;
        self._reset(mark)
        return None;

    @memoize
    def expr(self) -> Optional[Any]:
        # expr: 'if' expr 'then' expr 'else' expr | 'let' NAME '=' expr 'in' expr | comparison ';' expr | comparison
        mark = self._mark()
        if (
            (self.expect('if'))
            and
            (condition := self.expr())
            and
            (self.expect('then'))
            and
            (then_branch := self.expr())
            and
            (self.expect('else'))
            and
            (else_branch := self.expr())
        ):
            return ast . If ( condition , then_branch , else_branch );
        self._reset(mark)
        if (
            (self.expect('let'))
            and
            (name := self.name())
            and
            (self.expect('='))
            and
            (value := self.expr())
            and
            (self.expect('in'))
            and
            (body := self.expr())
        ):
            return ast . Let ( name . string , value , body );
        self._reset(mark)
        if (
            (comparison := self.comparison())
            and
            (self.expect(';'))
            and
            (expr := self.expr())
        ):
            return ast . Sequence ( comparison , expr );
        self._reset(mark)
        if (
            (comparison := self.comparison())
        ):
            return comparison;
        self._reset(mark)
        return None;

    @memoize
    def comparison(self) -> Optional[Any]:
        # comparison: term '=' comparison | term
        mark = self._mark()
        if (
            (term := self.term())
            and
            (self.expect('='))
            and
            (comparison := self.comparison())
        ):
            return ast . BinaryOp ( "EQUALS" , term , comparison );
        self._reset(mark)
        if (
            (term := self.term())
        ):
            return term;
        self._reset(mark)
        return None;

    @memoize
    def term(self) -> Optional[Any]:
        # term: factor '+' term | factor '-' term | factor
        mark = self._mark()
        if (
            (factor := self.factor())
            and
            (self.expect('+'))
            and
            (term := self.term())
        ):
            return ast . BinaryOp ( "PLUS" , factor , term );
        self._reset(mark)
        if (
            (factor := self.factor())
            and
            (self.expect('-'))
            and
            (term := self.term())
        ):
            return ast . BinaryOp ( "MINUS" , factor , term );
        self._reset(mark)
        if (
            (factor := self.factor())
        ):
            return factor;
        self._reset(mark)
        return None;

    @memoize
    def factor(self) -> Optional[Any]:
        # factor: primary '*' factor | primary '/' factor | primary
        mark = self._mark()
        if (
            (primary := self.primary())
            and
            (self.expect('*'))
            and
            (factor := self.factor())
        ):
            return ast . BinaryOp ( "STAR" , primary , factor );
        self._reset(mark)
        if (
            (primary := self.primary())
            and
            (self.expect('/'))
            and
            (factor := self.factor())
        ):
            return ast . BinaryOp ( "SLASH" , primary , factor );
        self._reset(mark)
        if (
            (primary := self.primary())
        ):
            return primary;
        self._reset(mark)
        return None;

    @memoize
    def primary(self) -> Optional[Any]:
        # primary: NUMBER | NAME '(' args? ')' | NAME | '(' expr ')'
        mark = self._mark()
        if (
            (number := self.number())
        ):
            return ast . Number ( int ( number . string ) );
        self._reset(mark)
        if (
            (name := self.name())
            and
            (self.expect('('))
            and
            (args := self.args(),)
            and
            (self.expect(')'))
        ):
            return ast . Call ( name . string , args or [] );
        self._reset(mark)
        if (
            (name := self.name())
        ):
            return ast . Variable ( name . string );
        self._reset(mark)
        if (
            (self.expect('('))
            and
            (expr := self.expr())
            and
            (self.expect(')'))
        ):
            return expr;
        self._reset(mark)
        return None;

    @memoize
    def args(self) -> Optional[Any]:
        # args: expr ((',' expr))*
        mark = self._mark()
        if (
            (expr := self.expr())
            and
            (exprs := self._loop0_3(),)
        ):
            return [expr] + exprs;
        self._reset(mark)
        return None;

    @memoize
    def _loop0_1(self) -> Optional[Any]:
        # _loop0_1: decl
        mark = self._mark()
        children = []
        while (
            (decl := self.decl())
        ):
            children.append(decl)
            mark = self._mark()
        self._reset(mark)
        return children;

    @memoize
    def _loop0_2(self) -> Optional[Any]:
        # _loop0_2: (',' NAME)
        mark = self._mark()
        children = []
        while (
            (_tmp_4 := self._tmp_4())
        ):
            children.append(_tmp_4)
            mark = self._mark()
        self._reset(mark)
        return children;

    @memoize
    def _loop0_3(self) -> Optional[Any]:
        # _loop0_3: (',' expr)
        mark = self._mark()
        children = []
        while (
            (_tmp_5 := self._tmp_5())
        ):
            children.append(_tmp_5)
            mark = self._mark()
        self._reset(mark)
        return children;

    @memoize
    def _tmp_4(self) -> Optional[Any]:
        # _tmp_4: ',' NAME
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (name := self.name())
        ):
            return [literal, name];
        self._reset(mark)
        return None;

    @memoize
    def _tmp_5(self) -> Optional[Any]:
        # _tmp_5: ',' expr
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (expr := self.expr())
        ):
            return [literal, expr];
        self._reset(mark)
        return None;

    KEYWORDS = ('else', 'fn', 'if', 'in', 'let', 'then')
    SOFT_KEYWORDS = ()

def filter_tokens(
    it: Generator[tokenize.TokenInfo, None, None],
) -> Generator[tokenize.TokenInfo, None, None]:
    # Out of laziness, we reuse the Python tokenizer,
    # however, we do not need indentation information.
    for tok in it:
        if tok.type not in {tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT}:
            yield tok

def parse(file):
    tokengen = filter_tokens(tokenize.generate_tokens(file.readline))
    tokenizer = Tokenizer(tokengen)
    parser = GeneratedParser(tokenizer)

    tree = parser.start()

    if not tree:
        err = parser.make_syntax_error(file.name)
        traceback.print_exception(err.__class__, err, None)

    return tree
