class Expression:

    def __init__(self, str_xpr):
        self.stack= []# стек для хранения скобок
        self.stack_RPN = []
        self.stack_RPN_res = []
        self.state = 'START'
        self.final_states = {'NUMBER_1', 'NUMBER_2', 'VARIABLE', 'CLOSE_BRACKET'} # конечные состояния автомата
        self._str_xpr = str_xpr.replace(' ', '')
        self._tokenized_xpr = []
        self._op_priority = {'*':0, '/':0, '+':1, '-':1}
        self._var_dict ={}


    def str_xpr(self):
        return self._str_xpr

    def is_valid(self):
        self.stack = []
        self.state = 'START'
        for char in self._str_xpr:
            if not self.process_char(char):
                return False

        # После обработки всей строки проверяем стек и финальное состояние
        return self.state in self.final_states and not self.stack

    def process_char(self,char):
        if self.state == 'START' or self.state == 'OPEN_BRACKET':
            if char.isdigit():
                self.state = 'NUMBER_1'
            elif char == '(':
                self.stack.append('(')
                self.state = 'OPEN_BRACKET'
            elif char.isalpha():
                self.state = 'VARIABLE'
            elif char == '-':
                self.state = 'MINUS'
            else:
                return False
        elif self.state == 'CLOSE_BRACKET':
            if char == ')':
                if not self.stack or self.stack[-1] != '(':
                    return  False
                self.stack.pop()
                self.state = 'CLOSE_BRACKET'
            elif char in '*/+':
                self.state = 'OPERATOR'
            elif char == '-':
                self.state = 'MINUS'
            else:
                return False
        elif self.state ==  'NUMBER_1':
            if char == ')':
                if not self.stack or self.stack[-1] != '(':
                    return  False
                self.stack.pop()
                self.state = 'CLOSE_BRACKET'
            elif char in '*/+':
                self.state = 'OPERATOR'
            elif char == '-':
                self.state = 'MINUS'
            elif char.isdigit():
                self.state = 'NUMBER_1'
            elif char == '.':
                self.state = 'DOT'
            else:
                return False
        elif self.state == 'NUMBER_2':
            if char == ')':
                if not self.stack or self.stack[-1] != '(':
                    return  False
                self.stack.pop()
                self.state = 'CLOSE_BRACKET'
            elif char in '*/+':
                self.state = 'OPERATOR'
            elif char == '-':
                self.state = 'MINUS'
            elif char.isdigit():
                self.state = 'NUMBER_2'
            else:
                return False
        elif self.state == 'VARIABLE':
            if char == ')':
                if not self.stack or self.stack[-1] != '(':
                    return  False
                self.stack.pop()
                self.state = 'CLOSE_BRACKET'
            elif char in '*/+':
                self.state = 'OPERATOR'
            elif char == '-':
                self.state = 'MINUS'
            elif char.isdigit():
                self.state = 'NUMBER_2'
            elif char.isalpha():
                self.state = 'VARIABLE'
            else:
                return False
        elif self.state == 'MINUS':
            if char.isdigit():
                self.state = 'NUMBER_1'
            elif char == '(':
                self.stack.append('(')
                self.state = 'OPEN_BRACKET'
            elif char.isalpha():
                self.state = 'VARIABLE'
            else:
                return False
        elif self.state == 'OPERATOR':
            if char.isdigit():
                self.state = 'NUMBER_1'
            elif char == '(':
                self.stack.append('(')
                self.state = 'OPEN_BRACKET'
            elif char == '-':
                self.state = 'MINUS'
            elif char.isalpha():
                self.state = 'VARIABLE'
            else:
                return False
        elif self.state == 'DOT':
            if char.isdigit():
                self.state = 'NUMBER_2'
            else:
                return  False

        return True

    def tokenize(self):
        pos_from = 0
        for i in range(len(self._str_xpr)):
            char = self._str_xpr[i]
            if char=='-' and (i==0 or (i>0 and self._str_xpr[i-1] in '(+-*/')):
                if self._str_xpr[pos_from:i]:
                    self._tokenized_xpr.append(self._str_xpr[pos_from:i])
                pos_from = i
            elif char in '(+-*/)':
                if self._str_xpr[pos_from:i]:
                    self._tokenized_xpr.append(self._str_xpr[pos_from:i])
                self._tokenized_xpr.append(char)
                pos_from = i+1


            if i == len(self._str_xpr)-1:
                if self._str_xpr[pos_from:]:
                    self._tokenized_xpr.append(self._str_xpr[pos_from:])


    def tokens(self):
        return self._tokenized_xpr

    def get_RPN(self):
        self.stack_RPN = []
        self.stack_RPN_res = []
        for token in self._tokenized_xpr:
            if token == '(':
                self.stack_RPN.append(token)
            elif  token == ')':
                while self.stack_RPN[-1] != '(':
                    self.stack_RPN_res.append(self.stack_RPN.pop())
                self.stack_RPN.pop()
            elif token in '*/-+':
                # print(self._op_priority[self.stack_RPN[-1]])
                while self.stack_RPN and self.stack_RPN[-1] != '(' and self._op_priority[self.stack_RPN[-1]]<=self._op_priority[token]:
                    self.stack_RPN_res.append(self.stack_RPN.pop())
                self.stack_RPN.append(token)
            else:
                self.stack_RPN_res.append(token)
        while self.stack_RPN:
            self.stack_RPN_res.append(self.stack_RPN.pop())

        return  self.stack_RPN_res

    def get_variables_dict(self):
        self._var_dict = {}
        for token in self._tokenized_xpr:
            if token[0].isalpha() and token not in self._var_dict.keys():
                self._var_dict[token] = float(input('Введите значение переменной {}:'.format(token) ))
            elif len(token) > 1 and token[0] == '-' and token[1].isalpha():
                self._var_dict[token] = (-1)*float(input('Введите значение переменной {}:'.format(token[1:])))

        return self._var_dict

    def calc_value(self):
        val = []
        for el in self.stack_RPN_res:
            if el in self._var_dict.keys():
                val.append(self._var_dict[el])
            elif el not in '+-/*':
                val.append((float(el)))
            elif el == '-':
                val.append(-val.pop() + val.pop())
            elif el == '+':
                val.append(val.pop() + val.pop())
            elif el == '*':
                val.append(val.pop() * val.pop())
            elif el == '/':
                val.append(1 / val.pop() * val.pop())
            print(val)

        return val
    def calc_example(self):
        u  = self._var_dict['u']
        y = self._var_dict['y']
        t = self._var_dict['t']
        r = self._var_dict['r']
        e = self._var_dict['e']
        w = self._var_dict['w']
        q = self._var_dict['q']
        l = self._var_dict['l']
        k = self._var_dict['k']
        j = self._var_dict['j']
        h = self._var_dict['h']
        g = self._var_dict['g']
        f = self._var_dict['f']
        d = self._var_dict['d']
        s = self._var_dict['s']
        return (u * y * t + r - e - w) * (q * l + k / j * h + g - f + d - s)
while True:
    fl = False
    check = input('Input expression: ')
    if check == 'bye-bye':
        break
    elif check == 'example':
        fl = True
        check = '' + '(u*y*t + r - e - w)*(q*l + k/j*h + g - f + d - s)'

    a = Expression(check)

    try:
        if a.is_valid():
            a.tokenize()
            print('Tokens: ',a.tokens())
            print('Reverse Polish Notation: ',' '.join(a.get_RPN()))
            print('Variables dictionary: ',a.get_variables_dict())
            print('Calculated value: ',a.calc_value())
            if fl:
                print('Real value: ',a.calc_example())
        else:
            print('Expression incorrect!')

    except ValueError:
        print('Incorrect float input')
    except ZeroDivisionError:
        print('Zero division attempt')
