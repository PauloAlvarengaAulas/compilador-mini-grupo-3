#Definição de classes para construção da AST(Abstract Syntax Tree) do Parser
from erros import *
class Program():
    def __init__(self, st):
        self.statements = []
        self.statements.append(st)

    def adiciona_statement(self, statement):
        self.statements.insert(0, statement)

    def eval(self, env):
        result = None
        for s in self.statements:
            result = s.eval(env)
        return result
    
    def get_statement(self):
        return self.statements

class Integer():
    def __init__(self, valor):
        self.valor = valor

    def eval(self, env):
        return int(self.valor)

    def to_string(self):
        return str(self.valor)
    
class OpBinarios():
    def __init__(self, esquerda, direita):
        self.esquerda = esquerda
        self.direita = direita

class Subtracao(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) - self.direita.eval(env)

class Soma(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) + self.direita.eval(env)

class Mult(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) * self.direita.eval(env)

class Div(OpBinarios):
    def eval(self, env):
        return int(self.esquerda.eval(env) / self.direita.eval(env))

class Mod(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) % self.direita.eval(env)

class Left_Shift(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) << self.direita.eval(env)

class Right_Shift(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) >> self.direita.eval(env)

class Unsigned_Right_Shift(OpBinarios):
    def eval(self, env):
        return (self.esquerda.eval(env) % 0x100000000) >> self.direita.eval(env)

class And(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) and self.direita.eval(env)

class Variaveis():
    def __init__(self, nome):
        self.nome = str(nome)
        self.valor = None

    def getnome(self):
        return str(self.nome)

    def eval(self, env):
        if env.variables.get(self.nome, None) is not None:
            self.value = env.variables[self.nome].eval(env)
            return self.valor
        raise LogicError('Não definido ainda')

class Atribuicao(OpBinarios):
    def eval(self, env):
        if isinstance(self.esquerda, Variaveis):
            if env.variables.get(self.esquerda.getnome(), None) is None:
                env.variables[self.esquerda.getnome()] = self.direita
                return self.direita.eval(env)

            raise AssignError(self.esquerda.getnome())
        else:
            raise LogicError('Não dá para atribuir a isso')

class Null():
    def eval(self, env):
        return self

    def to_string(self):
        return 'null'

    def rep(self):
        return 'Null()'

class Write():
    def __init__(self, valor):
        self.valor = valor
    
    def eval(self, env):
        print(self.valor.eval(env))
        return Null()

    def to_string(self):
        return 'Write'

class Read():
    def __init__(self, valor):
        self.valor = valor
    
    def eval(self, env):
        self.valor = int(input())