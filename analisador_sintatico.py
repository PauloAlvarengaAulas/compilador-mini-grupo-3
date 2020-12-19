from rply import ParserGenerator
from ast import * 
from erros import *
class ParserState(object):
    def __init__(self):
        self.variables = {}

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # Uma lista com todos os nomes de tokens aceitos pelo Parser
            ['INTEGER', 'WRITE', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SOMA', 'SUBTRACAO', 'MULT', 'DIV', 'MOD', 'LEFT_SHIFT',
             'RIGHT_SHIFT', '>>>', 'PROGRAM', 'IDENTIFIER', 'AND'],
             
             precedence=[
                 ('left', ['WRITE']),
                 ('left', ['SOMA', 'SUBTRACAO']),
                 ('left', ['MULT', 'DIV']),
                 ('left', ['MOD']),
                 ('left', ['LEFT_SHIFT', 'RIGHT_SHIFT']),
                 ('left', ['>>>', 'AND'])
             ],
             cache_id='myparser'
        )
        
    def parse(self):
        @self.pg.production('program : PROGRAM IDENTIFIER body')
        def main_program(p):
            return p[2]

        @self.pg.production('body : statement_full')
        def body_statement(p):
            return Program(p[0])

        @self.pg.production('body : statement_full body')
        def body_statement_program(p):
            if type(p[1]) is Program:
                body = p[1]
            else:
                body = Program(p[12])
            
            body.adiciona_statement(p[0])
            return p[1]

        @self.pg.production('statement_full : statement')
        @self.pg.production('statement_full : statement SEMI_COLON')  
        def statement_full(p):
            return p[0]
        
        @self.pg.production('statement : expression')
        def statement_expr(p):
            return p[0]

        @self.pg.production('statement : WRITE OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def write(p):
            return Write(p[2])

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
        def operacoes(p):
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
            else:
                raise AssertionError('Opa, isso não é possível!')
        
        #Definição do único tipo aceitado em MINI: inteiro
        @self.pg.production('expression : INTEGER')
        def numero(p):
            return Integer(int(p[0].value))

        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def expression_parens(p):
            return p[1]

        @self.pg.error
        def error_handler(token):
            pos = token.getsourcepos()
            if pos:
                raise UnexpectedTokenError(token.gettokentype())
            elif token.gettokentype() == '$end':
                raise UnexpectedEndError()
            else:
                raise UnexpectedTokenError(token.gettokentype())

    def get_parser(self):
        parser = self.pg.build()
        self.state = ParserState()
        return parser
