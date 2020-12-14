from rply import LexerGenerator

class Analisador_Lexico():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        #Parenteses
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        #Ponto e vírgula
        self.lexer.add('SEMI_COLON', r'\;')

        #Operadores
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')

        #Número
        self.lexer.add('NUMBER', r'\d+')

        #Ignorar espaços
        self.lexer.ignore(r'\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()