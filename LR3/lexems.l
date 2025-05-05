%{
    #include <stdio.h>
    #include <stdlib.h>
    #include "grammar.tab.h"
%}

ASSIGNMENT ":="
ID [a-zA-Z_][a-zA-Z0-9_]*
LPAR "("
RPAR ")"
SEMI ";"
BIN_ONLY_OPERATIONS [+/*]
MINUS [-]
SYMBOL_CONST  \'([^']|\'\')\'
COMMENT "//".*|\{(.|\n)*\}|\(\*(.|\n)*\*\)
WS [ \t]+

%%
{ASSIGNMENT}            {printf("ASSIGNMENT: %s\n", yytext); return ASSIGNMENT;}
{ID}                    {printf("ID: %s\n", yytext); return ID;}
{COMMENT}               {printf("COMMENT: %s\n", yytext);}
{LPAR}                  {printf("LPAR: %s\n", yytext); return LPAR;}
{RPAR}                  {printf("RPAR: %s\n", yytext); return RPAR;} 
{SEMI}                  {printf("SEMI\n"); return SEMI;}
{BIN_ONLY_OPERATIONS}   {printf("BIN_ONLY_OPERATIONS: %s\n", yytext); return BIN_ONLY_OPERATIONS;}
{MINUS}                 {printf("MINUS: %s\n", yytext); return MINUS;}
{SYMBOL_CONST}          {printf("SYMBOL_CONST: %s\n", yytext); return SYMBOL_CONST;}
{WS}                    {printf("WS\n");}
\n                      {printf("NEWLINE\n");}
.                       {printf("UNMATCHED: %s\n", yytext);}
%%
