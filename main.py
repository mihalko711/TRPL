from syntax_analyzer import Tokenizer

def main():
    kop = Tokenizer()

    print(kop.tokenize('program main\nvar x = 5, y = 67;\nbegin if x then var p = 1; end.'))


if __name__ == '__main__':
    main()