import re
from collections import namedtuple

class Tokenizer:
    def __init__(self):


        # структура токена для хранения (тип, значение)
        self.Token = namedtuple('Token', ['type', 'value'])
        # множество ключевх слов
        self.KEYWORDS  = {
            'program' , 'var', 'const', 'begin', 'end', 'write', 'read', 'if',
            'else', 'then', 'for', 'string'
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
            ('STRING', r'"[^"]*"'),
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
            if type_ != 'SKIP':
                # обработаем случай ключевых слов
                if type_ == 'ID' and  value in self.KEYWORDS:
                    tokens.append(self.Token(type_, value.upper()))
                else:
                    tokens.append(self.Token(type_,value))


            # накапливаем позицию, просто присваивание не поможет, ибо поиск по подстроке сбивает исходную индексацию
            pos += match_obj.end()
            print(f'pos:{pos}')
            print(f'type:{type_}')

        return tokens

    def print(self):
        print(self.re_pattern)