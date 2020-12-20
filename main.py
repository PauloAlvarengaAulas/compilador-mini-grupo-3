from analisador_lexico import Analisador_Lexico
from analisador_sintatico import Parser

text_input = """
program teste1
declare
    integer a := 2;
begin
    write(3 / 2);
    write(3 * 3);
    write(9 - 5);
    write(a);
end
"""

pg = Parser()
pg.parse()
parser = pg.get_parser(text_input)
