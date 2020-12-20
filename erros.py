class UnexpectedTokenError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

class UnexpectedEndError(Exception):
    texto = 'Missing ; in the end of the statement'
    
    def __str__(self):
        return "Missing ; in the end of the statement"

class LogicError(Exception):
    def __init__(self, texto):
        self.texto = texto

    def __str__(self):
        return self.texto

class AssignError(Exception):
    def __init__(self, nome):
        self.nome = nome
    
    def __str__(self):
        return f'Não pode atribuir para variável imutável {self.nome}'
