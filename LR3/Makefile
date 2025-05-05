CC = gcc
FL = flex
BIS = bison

LEX_FILE = lexems.l
YACC_FILE = grammar.y

LEX_C = lex.yy.c
YACC_C = grammar.tab.c
YACC_H = grammar.tab.h

TARGET = parser
INPUT = input

all: $(TARGET)

$(TARGET): $(LEX_C) $(YACC_C)
	$(CC) -o $(TARGET) $(LEX_C) $(YACC_C) -lfl

$(LEX_C): $(LEX_FILE) $(YACC_H)
	$(FL) $(LEX_FILE)

$(YACC_C) $(YACC_H): $(YACC_FILE)
	$(BIS) -d $(YACC_FILE)

run: all
	./$(TARGET) < $(INPUT)

clean:
	rm -f $(TARGET) $(LEX_C) $(YACC_C) $(YACC_H)