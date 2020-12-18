from rply import ParserGenerator
from ast import Integer, Soma, Subtracao, Mult, Div, Mod, Write, Left_Shift, Right_Shift, Unsigned_Right_Shift, And


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # Uma lista com todos os nomes de tokens aceitos pelo Parser
            ['INTEGER', 'WRITE', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SOMA', 'SUBTRACAO', 'MULT', 'DIV', 'MOD', 'LEFT_SHIFT', 'RIGHT_SHIFT', '>>>'],
             
             precedence=[
                 ('left', ['SOMA', 'SUBTRACAO']),
                 ('left', ['MULT', 'DIV']),
                 ('left', ['MOD']),
                 ('left', ['LEFT_SHIFT', 'RIGHT_SHIFT']),
                 ('left', ['>>>', 'AND'])
             ],
             cache_id='myparser'
        )

    def parse(self):
        '''@self.pg.production('program : statement')
        @self.pg.production('program : statement SEMI_COLON')
        @self.pg.production('program : statement SEMI_COLON program')
        def program(p):
            pass 
         '''       
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
        def operacoes(p):
            esquerda = p[0]
            direita = p[2]
            operator = p[1]

            if operator.gettokentype() == 'SOMA':
                print()
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
            raise ValueError(f'Encontrou um {token.gettokentype()} onde não era esperado')

    def get_parser(self):
        return self.pg.build()