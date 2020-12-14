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
        self.lexer.add('ATR', ':=')
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('LESS_THAN', r'\<')
        self.lexer.add('GREATER_THAN', r'\>')
        self.lexer.add('LESS_THAN_EQ', r'\<=')
        self.lexer.add('GREATER_THAN_EQ', r'\>=')
        self.lexer.add('TIMES', r'\*')
        self.lexer.add('DIV', '/')
        self.lexer.add('MOD', r'\%')
        self.lexer.add('AND', r'\&')
        self.lexer.add('OR', r'\|')
        self.lexer.add('LEFT_SHIFT', r'<<')
        self.lexer.add('RIGHT_SHIFT', r'>>')
        self.lexer.add('DIF', r'<>')
        self.lexer.add('<<<', r'<<<')
        self.lexer.add('>>>', r'>>>')
        self.lexer.add('NOT', r'not')

        #Número
        self.lexer.add('INTEGER', r'\d+')

        #Ignorar espaços
        self.lexer.ignore(r'\s+')

        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('END', r'end')

        self.lexer.add('READ', r'read')
        self.lexer.add('WRITE', r'write')
        self.lexer.add('DO', r'do')
        self.lexer.add('WHILE', r'while')
        self.lexer.add('THEN', r'then')

        self.lexer.add('PROGRAM', r'program')   
        self.lexer.add('BEGIN', r'begin')    

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()