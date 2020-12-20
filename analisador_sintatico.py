from analisador_lexico import Analisador_Lexico
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
            ['INT', 'WRITE', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SOMA', 'SUBTRACAO', 'MULT', 'DIV', 'MOD', 'LEFT_SHIFT',
             'RIGHT_SHIFT', '>>>', 'PROGRAM', 'IDENTIFIER', 'AND', 'READ', 'DECLARE',
             'BEGIN', 'END', 'INTEGER', 'ATR'],
             
             precedence=[
                 ('left', ['WRITE']),
                 ('left', ['SOMA', 'SUBTRACAO']),
                 ('left', ['MULT', 'DIV']),
                 ('left', ['MOD']),
                 ('left', ['LEFT_SHIFT', 'RIGHT_SHIFT']),
                 ('left', ['>>>', 'AND']),
                 ('left', ['READ']),
                 ('left', ['ATR'])
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
        
        @self.pg.production('variaveis : INTEGER IDENTIFIER ATR expression SEMI_COLON')
        def statement_assignment(state, p):
            return Atribuicao(Variaveis(p[1].getstr()), p[3])

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
            else:
                raise AssertionError('Opa, isso não é possível!')
        
        #Definição do único tipo aceitado em MINI: inteiro
        @self.pg.production('expression : INT')
        def numero(state, p):
            return Integer(int(p[0].value))

        @self.pg.production('expression : IDENTIFIER')
        def identifier(state, p):
            return p[0]

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
