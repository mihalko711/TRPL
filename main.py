class Expression:

    def __init__(self, str_xpr):
        self._str_xpr = str_xpr.replace(' ', '')


    def str_xpr(self):
        return self._str_xpr

    def check_on(self):
        correct = True
        balance = 0
        #  Состояния:
        #   0 - старт, 1 - откр скобка, 2 - закр скобка
        #   3 - цифра, 4 - буква, 5 - точка,  6 - унарн.минус, 7 - бинарние операции
        #   8 - брейк стейт
        state = 0
        for el in self._str_xpr():
            match state:
                case 0:
                    match el:
                        case '(':
                            state = 1
                            balance += 1
                        case ')':
                            state = 8
                        case
                case 8:
                    break

    
a = Expression(input('Input expression: '))
print(a.str_xpr())
print(a.lst_repr())