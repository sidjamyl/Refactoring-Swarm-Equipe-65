# sandbox/bad_code.py

import math  # import inutilisé

x = 42  # variable globale

def add(a, b):
    c = a + b
    d = 0  # variable jamais utilisée
    return c

def badFunctionName(x,y):
    print("Result =",add(x,y))
    return
