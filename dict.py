#-*- coding: utf-8 -*-

from lib.clp import clp

# word = u'duży'
# print word
#
# ids = clp(word)
#
# for id in ids:
# 	print word, clp.label(id)[0], clp.vec(id, word)

def check_if_verb(word):
    ids = clp(word)
    for id in ids:
        if clp.vec(id, word) not in [1, 45, 46, 47, 13, 14]:
            return clp.label(id)[0] == 'B'
        else:
            return False
