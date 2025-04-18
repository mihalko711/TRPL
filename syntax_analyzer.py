import re
from collections import namedtuple

class SyntaxAnalyzer():
    def __init__(self,prog_code):
        tokenizer = Tokenizer()
        self.tokens = tokenizer.tokenize(prog_code)
        self.pos = 0 # стартовая позиция
        self.curr_token = self.tokens[self.pos] # текущий токен


    def parse(self):
        try:
            self.parse_program()
            return True  # Парсинг прошёл успешно
        except SyntaxError as e:
            return e

    def expect(self,type_):
        # здесь сверяем текущий токен с необходимым, если подходит - деламе шаг вперед
        if self.curr_token.type == type_:
            self.advance()
        else:
            raise SyntaxError(f'Expected {type_}, got {self.curr_token.type}!')

    def advance(self):
        # передвигаем позицию, меняем текущий токен
        self.pos += 1
        if self.pos < len(self.tokens):
            self.curr_token = self.tokens[self.pos]

    def parse_program(self):
        self.expect('PROGRAM') # проверка ключевого слова program
        self.expect('ID') # проверка идентификатора(сделана в лексере)
        self.parse_declaration()
        self.expect('BEGIN') # проверка ключевого слова begin
        self.parse_command_sequence()
        self.expect('END') # проверка ключевых end.
        self.expect('DOT')
        return True

    def parse_identificator(self):
        self.expect('ID')

    def parse_declaration(self):
        while self.curr_token.type in ('VAR','CONST'):
            if self.curr_token.type == 'VAR':
                self.parse_var()
            else:
                self.parse_const()

    def parse_command_sequence(self):
        while self.curr_token.type in ('FOR', 'IF', 'READ', 'WRITE', 'ID','VAR'):
            self.parse_command()

    def parse_command(self):
        if self.curr_token.type == 'FOR':
            self.parse_for()
        elif self.curr_token.type == 'IF':
            self.parse_if_else()
        elif self.curr_token.type == 'READ':
            self.parse_read()
        elif self.curr_token.type == 'WRITE':
            self.parse_write()
        elif self.curr_token.type == 'VAR':
            self.parse_var()
        else:
            self.parse_assignment()

    def parse_var(self):
        self.expect('VAR')
        self.parse_variable_list()
        self.expect('SEMI')

    def parse_variable_list(self):
        while self.curr_token.type == 'ID':
            if self.tokens[self.pos + 1].type == 'EQ':
                self.parse_assignment()
            else:
                self.expect('ID')

            if self.curr_token.type == 'COMMA':
                self.advance()
            elif self.curr_token.type == 'SEMI':
                break
            else:
                raise SyntaxError(f"Expected 'SEMI' or 'COMA', got {self.curr_token.type}!")

    def parse_expression(self):
        self.parse_operand()
        while self.curr_token.type in ('PLUS', 'MINUS', 'MULT', 'DEL' ,'NE','LE','GE', 'LT','GT'):
            self.advance()
            self.parse_operand()

    def parse_operand(self):
        if self.curr_token.type in ('ID', 'STRING', 'NUMBER'):
            self.advance()
        elif self.curr_token.type == 'LPAREN':
            self.advance()
            self.parse_expression()
            self.expect('RPAREN')
        else:
            print(f"curr_token.type = {self.curr_token.type}, curr_token.type == 'NUMBER': {self.curr_token.type == 'NUMBER'}")
            raise SyntaxError(f"Expected 'LPAREN' or 'ID', 'STRING', 'NUMBER', got {self.curr_token.type}!")

    def parse_assignment(self):
        self.expect('ID')
        self.expect('EQ')
        self.parse_expression()

    def parse_const(self):
        self.expect('CONST')
        self.expect('ID')
        self.expect('EQ')
        if self.curr_token in ('NUMBER', 'STRING', 'TRUE', 'FALSE'):
            self.advance()
            self.expect('SEMI')
        else:
            raise SyntaxError(f"Expected 'NUMBER', 'STRING', 'TRUE' or 'FALSE', got {self.curr_token.type}!")


    def parse_write(self):
        self.expect('WRITE')
        self.expect('LRAPEN')
        while self.curr_token.type in ('STRING', 'NUMBER', 'ID'):
            self.advance()
            if self.curr_token == 'COMMA':
                self.advance()
        self.expect('PRAPEN')
        self.expect('SEMI')

    def parse_read(self):
        self.expect('READ')
        self.expect('LRAPEN')
        while self.curr_token.type == 'ID':
            self.advance()
            if self.curr_token == 'COMMA':
                self.advance()
        self.expect('PRAPEN')
        self.expect('SEMI')

    def parse_if_else(self):
        self.expect('IF')
        self.parse_expression()
        self.expect('THEN')
        self.expect('BEGIN')
        self.parse_command_sequence()
        self.expect('END')
        self.expect('SEMI')
        if self.curr_token.type == 'ELSE':
            self.advance()
            self.expect('BEGIN')
            self.parse_command_sequence()
            self.expect('END')
            self.expect('SEMI')

    def parse_for(self):
        self.expect('FOR')
        self.expect('LRAPEN')
        if self.curr_token.type == 'VAR':
            self.expect('VAR')
            self.expect('ID')
            self.expect('EQ')
            self.parse_expression()
        elif self.curr_token.type == 'ID':
            self.expect('ID')
        self.expect('SEMI')
        self.parse_expression()
        self.expect('SEMI')
        self.parse_expression()
        self.expect('SEMI')
        self.expect('LRAPEN')
        self.expect('BEGIN')
        self.parse_command_sequence()
        self.expect('END')


class Tokenizer:
    def __init__(self):


        # структура токена для хранения (тип, значение)
        self.Token = namedtuple('Token', ['type', 'value'])
        # множество ключевх слов
        self.KEYWORDS  = {
            'program' , 'var', 'const', 'begin', 'end', 'write', 'read', 'if',
            'else', 'then', 'for', 'string', 'true', 'false'
        }
        # описание токенов регулярними виражениями
        token_specs = [
            ('NUMBER' , r'\d+(\.\d+)?'),
            ('ID', r'[A-Za-z_][A-Za-z0-9_\-]*'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('COMMA', r','),
            ('SEMI', r';'),
            ('DOT', r'\.'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULT', r'\*'),
            ('DEL', r'/'),
            ('EQ', r'='),
            ('NE', r'<>'),
            ('LE', r'<='),
            ('GE', r'>='),
            ('LT', r'<'),
            ('GT', r'>'),
            ('STRING', r'("[^"]*")' + r"|('[^']*')"),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+')
        ]
        # сборка РВ, проверяющего вхождение любого токена
        re_parts = [f"(?P<{name}>{parts})" for name,parts in token_specs]
        self.re_pattern = re.compile("|".join(re_parts))

    def tokenize(self, string):
        # здесь описывается разбиение на токены pos - текущая позиция в строке
        pos  = 0

        # не хотим портить уже существующую строку
        string_copy = string

        # здесь будем хранить токены
        tokens = []


        while pos < len(string_copy):
            #  match_obj - находит токен в начале строки
            match_obj = self.re_pattern.match(string_copy[pos:])

            # случай ненайденного токена(но pos еще не на последнем элементе)
            if not match_obj:
                raise SyntaxError(f'Неизвестный символ: {string_copy[pos]}')

            # type_ - название токена, его достаем из match_obj с помощью lastgroup - имя группы последнего найденного вхождения
            # имя группы описывается в РВ так ?P<group_name>
            # value - значение найденного токена, определяется с помощью .group(), возвращающего подгруппу match_obj
            type_ = match_obj.lastgroup
            value = match_obj.group()

            # пропускаем пробелы и переносы, а также табуляции
            if type_ != 'SKIP'  and type_ != 'NEWLINE':
                # обработаем случай ключевых слов
                if type_ == 'ID' and  value in self.KEYWORDS:
                    tokens.append(self.Token(value.upper(), value.upper()))
                else:
                    tokens.append(self.Token(type_,value))


            # накапливаем позицию, просто присваивание не поможет, ибо поиск по подстроке сбивает исходную индексацию
            pos += match_obj.end()

        return tokens

    def print(self):
        print(self.re_pattern)