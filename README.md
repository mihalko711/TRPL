# В чем суть?

В данной работе будем проводить синтаксический анализ куска Паскалеподобного кода со следующими обрабатываемыми лексемами:

1. `Program`
2. `var`
3. `const`
4. `begin`
5. `end`
6. `write`
7. `read`
8. `if, else`
9. `for`
10. `string`

Подразумевается следующая логика программы:

1. В `main.py` будет построена логика ввода и обработки текста программы с подключением классов из `syntax_analyzer.py`
2. В `syntax_analyzer.py` будет как минимум класс `SyntaxAnalyzer`, реализующий функциолнал синтаксического анализатора текстов программ с помощью метода рекурсивного спуска

# Что есть метод рекурсивного спуска?
