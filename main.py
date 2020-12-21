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
    %write(a);

    if(9 = 1) then
        write(3);
    else if(9 <> 3) then
        write(10);
        end
    end
end
"""

pg = Parser()
pg.parse()
parser = pg.get_parser(text_input)
