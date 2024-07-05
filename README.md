# compile-to-wasm-from-scratch-in-python

A toy compiler for the "Compiling to WASM from scratch" BornHack 2024 talk.

## Example

```
fn main() =
    sum_to(10)

fn sum_to(n) =
    if n = 0
        then 0
        else n + sum_to(n - 1)
```

## Quick Start

You need to have [`rye`](https://rye.astral.sh) and [Webassembly Binary Toolkit (`wabt`)](https://github.com/WebAssembly/wabt) installed.

```sh
rye sync

rye run generate

sh run.sh examples/sum_to.ctwfs
```

## Grammar

```bnf
<program> ::= <declaration>*

<declaration> ::= <function-declaration>

<function-declaration> ::= "fn" <identifier> "(" <parameter-list> ")" "=" <expression>
<parameter-list> ::= <identifier> ("," <identifier>)*

<expression> ::= <if-expression> | <let-expression> | <sequence-expression>
<if-expression> ::= "if" <expression> "then" <expression> "else" <expression>
<let-expression> ::= "let" <identifier> "=" <expression> "in" <expression>
<sequence-expression> ::= <comparison> ( ";" <expression> )?
<comparison> ::= <sum> ( ( "=" ) <sum> )*
<term> ::= <factor> ( ("+" | "-") <factor> )*
<factor> ::= <unary> ( ("*" | "/") <unary> )*
<unary> ::= "-" <unary> | <call>
<call> ::= <identifier> "(" <argument-list> ")" | <primary>
<argument-list> ::= <expression> ("," <expression>)*
<primary> ::= <number> | <identifier> | "(" <expression> ")"

<identifier> ::= <letter> (<letter> | <digit>)*
<number> ::= <digit>+
<letter> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"
<digit> ::= "0" | "1" | ... | "9"
```
