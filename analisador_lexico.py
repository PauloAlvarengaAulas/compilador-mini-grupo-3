import sys
import os.path

class Analisador_lexico():
    def __init__(self):
        self.arquivo = 'programa.txt'

    def tem_digito(self, dig):
        digitos = '0123456789'
        if dig in digitos:
            return True
        return False

    def tem_letra(self, letra):
        letras = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if letra in letras:
            return True
        return False