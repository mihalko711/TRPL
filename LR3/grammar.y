%{
    #include <stdio.h>

    int yylex();
    int yyerror(const char *s);
%}

%token ASSIGNMENT ID LPAR RPAR SEMI
%token BIN_ONLY_OPERATIONS MINUS
%token SYMBOL_CONST COMMENT

%%
axiom_new
    :axiom
    ;


axiom
    :expr_list
    ;

expr_list
    : expr expr_list_tail
    |
    ;

expr_list_tail
    : SEMI expr_list
    ;

expr
    : ID ASSIGNMENT expr_eval
    ;

expr_eval
    : term expr_eval_tail
    ;

expr_eval_tail
    : BIN_ONLY_OPERATIONS term expr_eval_tail
    | MINUS term expr_eval_tail
    |
    ;

term
    : ID
    | SYMBOL_CONST
    | MINUS term
    | LPAR expr_eval RPAR
    ;

%%

int main() {
    int result = yyparse();

    if (result == 0) printf("Parsing succesful!\n");
    else printf("Parsing failed with code %d!\n", result);
    return result;
}

int yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
    return 1;
}