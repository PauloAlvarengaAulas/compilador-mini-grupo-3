from analisador_lexico import Analisador_Lexico
from analisador_sintatico import Parser

text_input = """
program teste
write(3 / 2);
write(3 * 3);
write(9 - 5);
"""

lexer = Analisador_Lexico().get_lexer()
tokens = lexer.lex(text_input)

pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()