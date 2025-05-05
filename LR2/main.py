from syntax_analyzer import Tokenizer,SyntaxAnalyzer

def main():
    tok = Tokenizer()

    with open('prog_code.txt', 'r', encoding='utf-8') as f:
        prog_code = f.read()
    print(prog_code)

    tokenized = tok.tokenize(prog_code)

    for i in range(len(tokenized)):
        print(f"{i}: {tokenized[i]}")

    syn_an = SyntaxAnalyzer(prog_code)
    print(f"The result of check is {syn_an.parse()}")


if __name__ == '__main__':
    main()