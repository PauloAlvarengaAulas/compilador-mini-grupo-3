from analisador_lexico import Analisador_Lexico
from rply import ParserGenerator
from ast import * 
from erros import *
class ParserState(object):
    def __init__(self):
        self.vars = {}

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # Uma lista com todos os nomes de tokens aceitos pelo Parser
            ['INT', 'WRITE', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SOMA', 'SUBTRACAO', 'MULT', 'DIV', 'MOD', 'LEFT_SHIFT',
             'RIGHT_SHIFT', '>>>', 'PROGRAM', 'IDENTIFIER', 'AND', 'READ', 'DECLARE',
             'BEGIN', 'END', 'INTEGER', 'ATR', ',', 'IF', 'ELSE', 'THEN', 'DIF', 'IGUAL',
             'OR', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_EQ', 'GREATER_THAN_EQ', 'WHILE',
             'DO'],
             
             precedence=[
                 ('left', ['IDENTIFIER']),
                 ('left', ['WRITE']),
                 ('left', ['INTEGER']),
                 ('left', ['ATR']),
                 ('left', [',']),
                 ('left', ['IF', 'ELSE', 'END', 'THEN' , 'WHILE']),
                 ('left', ['>>>', 'AND', 'OR']),
                 ('left', ['MOD']),
                 ('left', ['IGUAL', 'DIF', 'GREATER_THAN_EQ', 'GRETER_THAN', 'LESS_THAN', 'LESS_THAN_EQ']),
                 ('left', ['LEFT_SHIFT', 'RIGHT_SHIFT']),
                 ('left', ['SOMA', 'SUBTRACAO']),
                 ('left', ['MULT', 'DIV']),
                 ('left', ['READ'])  
             ],
             cache_id='myparser'
        )
        
    def parse(self):
        @self.pg.production('program : PROGRAM IDENTIFIER DECLARE variaveis BEGIN body END')
        def main_program_with_variable(state, p):
            return p[5]

        @self.pg.production('program : PROGRAM IDENTIFIER BEGIN body END')
        def main_program(state, p):
            return p[3]

        @self.pg.production('body : statement_full')
        def body_statement(state, p):
            return Program(p[0])

        @self.pg.production('body : statement_full body')
        def body_statement_program(state, p):
            if type(p[1]) is Program:
                body = p[1]
            else:
                body = Program(p[12])
            
            body.adiciona_statement(p[0])
            return p[1]

        @self.pg.production('bloco : statement_full')
        def bloco(state, p):
            return Bloco(p[0])

        @self.pg.production('bloco : statement_full bloco')
        def bloco_expr(state, p):
            if type(p[1]) is Bloco:
                b = p[1]
            else:
                b = Bloco(p[1])
            b.adiciona_statement(p[0])
            return b

        @self.pg.production('statement_full : statement')
        @self.pg.production('statement_full : statement SEMI_COLON')  
        def statement_full(state, p):
            return p[0]
        
        @self.pg.production('statement : expression')
        def statement_expr(state, p):
            return p[0]

        @self.pg.production('statement : WRITE OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def write(state, p):
            return Write(p[2])

        @self.pg.production('statement : READ OPEN_PAREN IDENTIFIER CLOSE_PAREN SEMI_COLON')
        def read(state, p):
            return Read(p[2])
        
        @self.pg.production('variaveis : INTEGER IDENTIFIER ATR expressao SEMI_COLON')
        def atribuicao_variaveis(state, p):
            return Atribuicao(Variaveis(p[1].getstr()), p[3])

        @self.pg.production('expressao : expression')
        @self.pg.production('expressao : expression ,')
        def expressoes(state, p):
            return p[0]

        @self.pg.production('expression : IF OPEN_PAREN expression CLOSE_PAREN THEN bloco END')
        def if_sem_else(state, p):
            return If_stmt(condicao=p[2], corpo=p[5])

        @self.pg.production('expression : IF OPEN_PAREN expression CLOSE_PAREN THEN bloco ELSE bloco END')
        def if_sem_com_else(state, p):
            return If_stmt(condicao=p[2], corpo=p[5], corpo_else=p[7])

        @self.pg.production('expression : DO bloco WHILE OPEN_PAREN expression CLOSE_PAREN')
        def while_stmt(state, p):
            return Do_While(condicao=p[4], corpo=p[1])

        #Função que define as regras das operações da linguagem
        @self.pg.production('expression : expression SOMA expression')
        @self.pg.production('expression : expression SUBTRACAO expression')
        @self.pg.production('expression : expression MULT expression')
        @self.pg.production('expression : expression DIV expression')
        @self.pg.production('expression : expression MOD expression')
        @self.pg.production('expression : expression LEFT_SHIFT expression')
        @self.pg.production('expression : expression RIGHT_SHIFT expression')
        @self.pg.production('expression : expression >>> expression')
        @self.pg.production('expression : expression AND expression')
        @self.pg.production('expression : expression DIF expression')
        @self.pg.production('expression : expression IGUAL expression')
        @self.pg.production('expression : expression OR expression')
        @self.pg.production('expression : expression GREATER_THAN_EQ expression')
        @self.pg.production('expression : expression GREATER_THAN expression')
        @self.pg.production('expression : expression LESS_THAN expression')
        @self.pg.production('expression : expression LESS_THAN_EQ expression')
        def operacoes(state, p):
            esquerda = p[0]
            direita = p[2]
            operator = p[1]

            if operator.gettokentype() == 'SOMA':
                return Soma(esquerda, direita)
            
            elif operator.gettokentype() == 'SUBTRACAO':
                return Subtracao(esquerda, direita)
            
            elif operator.gettokentype() == 'MULT':
                return Mult(esquerda, direita)
            
            elif operator.gettokentype() == 'DIV':
                return Div(esquerda, direita)
            
            elif operator.gettokentype() == 'MOD':
                return Mod(esquerda, direita)

            elif operator.gettokentype() == 'LEFT_SHIFT':
                return Left_Shift(esquerda, direita)
            
            elif operator.gettokentype() == 'RIGHT_SHIFT':
                return Right_Shift(esquerda, direita)

            elif operator.gettokentype() == '>>>':
                return Unsigned_Right_Shift(esquerda, direita)

            elif operator.gettokentype() == 'AND':
                return And(esquerda, direita)

            elif operator.gettokentype() == 'DIF':
                return Diff(esquerda, direita)

            elif operator.gettokentype() == 'IGUAL':
                return Igual(esquerda, direita)

            elif operator.gettokentype() == 'OR':
                return Or(esquerda, direita)
            
            elif operator.gettokentype() == 'GREATER_THAN_EQ':
                return Gte(esquerda, direita) 
            
            elif operator.gettokentype() == 'GREATER_THAN':
                return Gt(esquerda, direita) 
            
            elif operator.gettokentype() == 'LESS_THAN':
                return Lt(esquerda, direita) 
            
            elif operator.gettokentype() == 'LESS_THAN_EQ':
                return Lte(esquerda, direita) 

            else:
                raise AssertionError('Opa, isso não é possível!')
        
        #Definição do único tipo aceitado em MINI: inteiro
        @self.pg.production('expression : INT')
        def numero(state, p):
            return Integer(int(p[0].value))

        @self.pg.production('expression : IDENTIFIER')
        def identifier(state, p):
            return Variaveis(p[0].getstr())

        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def expression_parens(state, p):
            return p[1]

        @self.pg.error
        def error_handler(state, token):
            pos = token.getsourcepos()
            if pos:
                raise UnexpectedTokenError(token.gettokentype())
            elif token.gettokentype() == '$end':
                raise UnexpectedEndError()
            else:
                raise UnexpectedTokenError(token.gettokentype())

    state = ParserState()

    def get_parser(self, text_input, state=state):
        parser = self.pg.build()
        lexer = Analisador_Lexico().get_lexer()
        tokens = lexer.lex(text_input)
        result = parser.parse(tokens, state).eval(state)
        return result
