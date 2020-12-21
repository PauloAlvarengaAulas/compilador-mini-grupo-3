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

class Or(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) or self.direita.eval(env)

class Diff(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) != self.direita.eval(env)

class Igual(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) == self.direita.eval(env)

class Gte(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) >= self.direita.eval(env)

class Gt(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) > self.direita.eval(env)

class Lte(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) <= self.direita.eval(env)

class Lt(OpBinarios):
    def eval(self, env):
        return self.esquerda.eval(env) < self.direita.eval(env)

class Variaveis():
    def __init__(self, nome):
        self.nome = str(nome)
        self.valor = None

    def getnome(self):
        return str(self.nome)

    def eval(self, env):
        if env.vars.get(self.nome, None) is not None:
            self.valor = env.vars[self.nome].eval(env)
            return self.valor
        raise LogicError('Não definido ainda')

class Bloco():
    def __init__(self, st):
        self.statements = []
        self.statements.append(st)

    def adiciona_statement(self, st):
        self.statements.insert(0, st)

    def get_statements(self):
        return self.statements

    def eval(self, env):
        resultado = None
        for s in self.statements:
            result = s.eval(env)
        return resultado

class Atribuicao(OpBinarios):
    def eval(self, env):
        if isinstance(self.esquerda, Variaveis):
            if env.vars.get(self.esquerda.getnome(), None) is None:
                env.vars[self.esquerda.getnome()] = self.direita
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

class If_stmt():
    def __init__(self, condicao, corpo, corpo_else=Null()):
        self.condicao = condicao
        self.corpo = corpo
        self.corpo_else = corpo_else

    def eval(self, env):
        condicao = self.condicao.eval(env)
        if condicao == True:
            return self.corpo.eval(env)
        else:
            if type(self.corpo_else) is not Null:
                return self.corpo_else.eval(env)
            return Null()

class Do_While():
    def __init__(self, condicao, corpo):
        self.condicao = condicao
        self.corpo = corpo

    def eval(self, env):
        condicao = self.condicao.eval(env)
        #self.corpo.eval(env)
        while condicao == True:
            return self.corpo.eval(env)

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