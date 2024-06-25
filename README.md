# compile-to-wasm-from-scratch-in-python

## Example

```
fn main() =
  sum_to(10)

fn sum_to(n) =
  if n
    then n + sum_to(n - 1)
    else 0
```

##

## Grammar

```bnf
<program> ::= <declaration>*

<declaration> ::= <function-declaration>

<function-declaration> ::= "fn" <identifier> "(" <parameter-list> ")" "=" <expression>
<parameter-list> ::= <identifier> ("," <identifier>)*

<expression> ::= <if-expression> | <let-expression> | <sequence-expression>
<if-expression> ::= "if" <expression> "then" <expression> "else" <expression>
<let-expression> ::= "let" <identifier> "=" <expression> "in" <expression>
<sequence-expression> ::= <term> ( ";" <expression> )?
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
