from syntax_analyzer import Tokenizer,SyntaxAnalyzer

def main():
    kop = Tokenizer()

    print(kop.tokenize('program main\nvar x = 5, y = 67;\nbegin if x then var p = 1; end.'))

    syn_an = SyntaxAnalyzer('program main\nvar x = 5, y = 67;\nbegin if x then begin  var p = 1; end; end')
    print(f"The result of check is {syn_an.parse()}")


if __name__ == '__main__':
    main()