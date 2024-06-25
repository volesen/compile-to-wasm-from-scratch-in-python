# compile-to-wasm-from-scratch-in-python

## Grammar

```bnf
<program> ::= <declaration>*

<declaration> ::= <function-declaration>

<function-declaration> ::= "fn" <identifier> "(" <parameter-list> ")" <expression-block>
<parameter-list> ::= <identifier> ("," <identifier>)*

<statement> ::= <let-statement> | <expression-statement>
<let-statement> ::= "let" <identifier> "=" <expression> ";"
<expression-statement> ::= <expression> ";"

<expression> ::= <term>
<term> ::= <factor> ( ("+" | "-") <factor> )*
<factor> ::= <unary> ( ("*" | "/") <unary> )*
<unary> ::= "-" <unary> | <call>
<call> ::= <identifier> "(" <argument-list> ")" | <primary>
<argument-list> ::= <expression> ("," <expression>)*
<primary> ::= <number> | <identifier> | "(" <expression> ")" | <if-expression> | <expression-block>
<if-expression> ::= "if" <expression> "then" <expression-block> "else" <expression-block>
<expression-block> ::= "{" <statement>* <expression> "}"

<identifier> ::= <letter> (<letter> | <digit>)*
<number> ::= <digit>+
<letter> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"
<digit> ::= "0" | "1" | ... | "9"
```
