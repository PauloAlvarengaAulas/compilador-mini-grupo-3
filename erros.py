class UnexpectedTokenError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

class UnexpectedEndError(Exception):
    texto = 'Missing ; in the end of the statement'
    
    def __str__(self):
        return "Missing ; in the end of the statement"
