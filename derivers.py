# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:18:25 2024

@author: lcuev
"""
import nodevisitor as nv
import keywords as kw
import nodeclasses as nc
from token_ import ADDTOKEN,MULTOKEN


class FunctionalDeriver(nv.NodeVisitor):
    def __init__(self,tree):
        self.tree = tree
    
    def visit_Num(self,node):
        return nv.NUM(0)
    
    def visit_Var(self,node):
        return nc.Var(node.token,node.order + 1,node.weight)
        
    def visit_AsOp(self,node):
        if node.token.type == kw.ADD:
            newnode = nc.AsOp(node.token, weight = node.weight)
            for arg in node.args:
                newnode.args += [self.visit(arg)]
            return newnode
        elif node.token.type == kw.MUL:
            newnode = nc.AsOp(ADDTOKEN(),weight = node.weight)
            for i,arg in enumerate(node.args):
                coeff = [node.args[j] for j in range(len(node.args)) if i!=j]
                argcopy = arg.copy()
                mulnode = nc.AsOp(node.token,arg.weight)
                argcopy.weight -= 1                
                coeff += [argcopy]
                coeff += [self.visit(arg)]                
                mulnode.args += coeff
                newnode.args += [mulnode]
            
            return newnode
        return node
    
    def visit_UnOp(self,node):
        if node.token.type == kw.log:
            newnode = nc.AsOp(MULTOKEN(),weight=node.weight)
            argcopy = node.arg.copy()
            argcopy.weight = -1
            newnode.args += [argcopy]
            newnode.args += [self.visit(node.arg)]
            return newnode
        else:
            raise Exception(f'cannot differentiate unop of type {node.token.type}')
        
    def visit_Id(self,node):
        return nc.Var(node.token)
        
    def derive(self):
        return self.visit(self.tree)
    
class PartialDeriver(nv.NodeVisitor):
    def __init__(self,left,right):
        self.right = right
        self.left = left
    
    def visit_Num(self,node):
        return nv.NUM(0)
        
    def visit_AsOp(self,node):
        if node.token.type == kw.ADD:
            newnode = nc.AsOp(node.token, weight = node.weight)
            for arg in node.args:
                newnode.args += [self.visit(arg)]
            return newnode
        elif node.token.type == kw.MUL:
            newnode = nc.AsOp(ADDTOKEN(),weight = node.weight)
            for i,arg in enumerate(node.args):
                coeff = [node.args[j] for j in range(len(node.args)) if i!=j]
                argcopy = arg.copy()
                mulnode = nc.AsOp(node.token,arg.weight)
                argcopy.weight -= 1
                coeff += [argcopy]
                coeff += [self.visit(arg)]
                mulnode.args += coeff
                newnode.args += [mulnode]
            return newnode
        return node
    
    def visit_UnOp(self,node):
        if node.token.type == kw.log:
            newnode = nc.AsOp(MULTOKEN(),weight=node.weight)
            argcopy = node.arg.copy()
            argcopy.weight = -1
            newnode.args += [argcopy]
            newnode.args += [self.visit(node.arg)]
            return newnode
        else:
            raise Exception(f'cannot differentiate unop of type {node.token.type}')
        
    def visit_Id(self,node):
        if node == self.left:
            return nv.NUM(1)
                
        return nv.NUM(0)
        
    def derive(self):
        return self.visit(self.right)