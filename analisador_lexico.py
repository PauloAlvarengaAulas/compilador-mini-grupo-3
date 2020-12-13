import os.path
from plymaster.ply import *

class Analisador_lexico():
    reservado = {
        'if'	 :	'IF',
        'else'	 :	'ELSE',
        'then'   :  'THEN',
        'int'	 :	'INTEGER',
        'while'	 :	'WHILE',
        'write'  :	'WRITE',
        'read'   :	'READ',
        'program':  'PROGRAM',
        'declare':  'DECLARE',
        'not'    :  'NOT',
        'and'    :  'AND',
        'do'     :  'DO',
        'begin'  :  'BEGIN',
        'end'    :  'END',
        'or'     :  'OR',
        'mod'    :  'MOD'
    }