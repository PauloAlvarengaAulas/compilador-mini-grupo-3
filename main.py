from analisador_lexico import Analisador_Lexico
from analisador_sintatico import Parser

text_input = """
write((2 + 2) * 2);
"""

lexer = Analisador_Lexico().get_lexer()
tokens = lexer.lex(text_input)

pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()