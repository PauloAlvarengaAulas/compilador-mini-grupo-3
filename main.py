from analisador_lexico import Analisador_Lexico

text_input = """
not 8
"""
lexer = Analisador_Lexico().get_lexer()
tokens = lexer.lex(text_input)

for token in tokens:
    print(token)