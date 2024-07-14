# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 17:45:29 2024

@author: lcuev
"""
import keywords as kw

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self,opp):
        return opp.type == self.type and opp.value == self.value
    
def ADDTOKEN():
    return Token(kw.ADD,'+')

def MULTOKEN():
    return Token(kw.MUL,'*')

def DIFTOKEN():
    return Token(kw.DIF,'&')

RESERVED_KEYWORDS = {kw.show: Token(kw.show,kw.show),
                     kw.log: Token(kw.log,kw.log),
                     kw.diag: Token(kw.diag,kw.diag)}