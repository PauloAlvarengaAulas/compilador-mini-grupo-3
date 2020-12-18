#Definição de classes para construção da AST(Abstract Syntax Tree) do Parser
'''class Program():
    def __init__(self, st):
        self.st = st
        self.statements.append(self.st)

    def eval(self):
        for s in self.statements:
            return s.eval()
'''
class Integer():
    def __init__(self, valor):
        self.valor = valor

    def eval(self):
        return int(self.valor)
    
class OpBinarios():
    def __init__(self, esquerda, direita):
        self.esquerda = esquerda
        self.direita = direita

class Subtracao(OpBinarios):
    def eval(self):
        return self.esquerda.eval() - self.direita.eval()

class Soma(OpBinarios):
    def eval(self):
        return self.esquerda.eval() + self.direita.eval()

class Mult(OpBinarios):
    def eval(self):
        return self.esquerda.eval() * self.direita.eval()

class Div(OpBinarios):
    def eval(self):
        return self.esquerda.eval() / self.direita.eval()

class Mod(OpBinarios):
    def eval(self):
        return self.esquerda.eval() % self.direita.eval()

class Left_Shift(OpBinarios):
    def eval(self):
        return self.esquerda.eval() << self.direita.eval()

class Right_Shift(OpBinarios):
    def eval(self):
        return self.esquerda.eval() >> self.direita.eval()

class Unsigned_Right_Shift(OpBinarios):
    def eval(self):
        return (self.esquerda.eval() % 0x100000000) >> self.direita.eval()

class And(OpBinarios):
    def eval(self):
        return self.esquerda.eval() and self.direita.eval()

class Write():
    def __init__(self, valor):
        self.valor = valor
    
    def eval(self):
        print(self.valor.eval())

class Read():
    def __init__(self, valor):
        self.valor = valor
    
    def eval(self):
        input(self.valor.eval())