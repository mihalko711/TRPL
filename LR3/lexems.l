%{
    #include <stdio.h>
    #include <stdlib.h>
%}

ASSIGNMENT ":="
ID [a-zA-Z_][a-zA-Z0-9_]*
LPAR "("
RPAR ")"
BIN_ONLY_OPERATIONS [+\*]
UN_VAR_OPERATIONS [-]
STRING_LITERAL \"([^\"\\]|\\.)*\"

%%
{ASSIGNMENT}            {printf("ASSIGNMENT: %s\n", yytext);}
{ID}                    {printf("ID: %s\n", yytext);}
{LPAR}                  {printf("LPAR: %s\n", yytext);}
{RPAR}                  {printf("RPAR: %s\n", yytext);}
{BIN_ONLY_OPERATIONS}   {printf("BIN_ONLY_OPERATIONS: %s\n", yytext);}
{UN_VAR_OPERATIONS}     {printf("UN_VAR_OPERATIONS: %s\n", yytext);}
{STRING_LITERAL}        {printf("STRING_LITERAL: %s\n", yytext);}
.                       {printf("UNMATCHED: %s\n", yytext);}

%%
