# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:39:41 2024

@author: lcuev
"""
import keywords as kw
from token_ import Token,MULTOKEN

def NUM(n):
    return Num(Token(kw.INT,n))

def ID(char):
    return Num(Token(kw.ID,char))

class AST(object):
    pass

class NoOp(AST):
    pass

class Compound(AST):
    def __init__(self):
        self.children = []
    
class Num(AST):
    def __init__(self,token,weight = 1):
        self.token = token
        self.weight = weight
        
    def __eq__(self,opp):
        return self.token == opp.token
    
    def copy(self):
        return Num(self.token,self.weight)
        
class Id(AST):
    def __init__(self, token, weight = 1):
        self.token = token
        self.weight = weight
        
    def __eq__(self,opp):
        return self.token == opp.token
    
    
    def copy(self):
        return Id(self.token,self.weight)
        
class Var(AST):
    def __init__(self, token, order = 1, weight = 1):
        self.token = Token(kw.VAR,token.value)
        self.order = order
        self.weight = weight
    
    def __eq__(self,opp):
        return self.token == opp.token
    
    def copy(self):
        return Var(self.token,self.order,self.weight)

class AsOp(AST):
    def __init__(self, token, weight = 1):
        self.token = self.op = token
        self.args = []
        self.weight = weight
        
    def __eq__(self,opp):
        if opp.token != self.token:
            return False
        for arg in self.args:
            if arg not in opp.args:
                return False
        for arg in opp.args:
            if arg not in self.args:
                return False
        return True
    
    def __str__(self):
        string = ''
        
        for arg in self.args:
            string += f'({arg.token},{arg.weight})' + ','
            
        return string
    
    def __repr__(self):
        return self.__str__()
    
    def copy(self):
        copy = AsOp(self.token,self.weight)
        copy.args += self.args
        return copy
    
class UnOp(AST):
    def __init__(self, token, arg, weight = 1):
        self.token = self.op = token
        self.arg = arg
        self.weight = weight
        
    def __eq__(self,opp):
        return self.token == opp.token and self.arg == opp.arg
    
    def copy(self):
        return UnOp(self.token,self.arg,self.weight)
    
class BinOp(AST):
    def __init__(self, left, token, right, weight = 1):
        self.token = self.op = token
        self.left = left
        self.right = right
        
    def __eq__(self,opp):
        return self.token == opp.token and self.arg == opp.arg
    
    def copy(self):
        return BinOp(self.left,self.token,self.right)
    
class Reference(AST):
    def __init__(self, token, tensorid, ids):
        self.token = token
        self.tensorid = tensorid
        self.ids = ids
    
class Assign(AST):
    def __init__(self, left, token, right):
        self.left = left
        self.token = self.op = token
        self.right = right
        
class Show(AST):
    def __init__(self,token,args):
        self.token = self.op = token
        self.args = args
        
class DiMeRef(AST):
    def __init__(self,token,arg):
        self.token=token
        self.arg=arg
        
class DiMeRefToCh(AST):
    def __init__(self,token,arg):
        self.token=token
        self.arg=arg
        
class DiCh:
    def __init__(self,token):
        self.token = token
        self.args = {}
    
    def __getitem__(self, id):
        return self.args[id]
    
    def __setitem__(self,id,newitem):
        self.args[id]=newitem
        
        
class DiMe:
    def __init__(self, token, args):
        self.token = token
        self.args = args

    def inverse(self):
        invargs={}
        
        for key,value in self.args.items():
            valcopy=value.copy()
            valcopy.weight=-1
            mulop = AsOp(MULTOKEN())
            mulop.args += [valcopy]
            invargs[key] = mulop
            
        return DiMe(self.token, invargs)
        
    def __getitem__(self, id):
        return self.args[id]
    
    def __setitem__(self,id,newitem):
        self.args[id]=newitem
        

        
