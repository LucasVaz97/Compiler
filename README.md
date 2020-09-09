# Compiler
EBNF
EXPRESSION =TERM, {("+" | "-"), TERM};
TERM = FACTOR, {("*" | "/"), FACTOR};
FACTOR = NUMBER | "(", EXPRESSION, ")";
