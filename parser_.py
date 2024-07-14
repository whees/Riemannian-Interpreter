# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 15:31:39 2024

@author: lcuev
"""
import nodeclasses as nc
import keywords as kw
from token_ import ADDTOKEN,MULTOKEN
    
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception(f'Invalid syntax at {self.current_token}')
        
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f'Invalid syntax: Expected {token_type}, got {self.current_token.type}')
            
    def program(self):
       node = self.compound_statement()
       return node
   
    def compound_statement(self):
        nodes = self.statement_list()

        root = nc.Compound()
        for node in nodes:
            root.children.append(node)

        return root
    
    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()
  
        results = [node]
  
        while self.current_token.type == kw.SEMI:
            self.eat(kw.SEMI)
            results.append(self.statement())
  
        if self.current_token.type == kw.ID:
            self.error()
  
        return results
    
    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type in (kw.ID,kw.REF):
            node = self.assignment_statement()
        elif self.current_token.type == kw.show:
            node = self.show_statement()
        else:
            node = self.empty()
            
        return node
    
    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        if self.current_token.type == kw.ID:
            left = self.variable()
        else:
            left = self.reference()
        token = self.current_token
        self.eat(kw.ASSIGN)
        right = self.expr()
        node = nc.Assign(left, token, right)
        return node
    
    def reference(self):
        token = self.current_token
        tensorid = nc.Id(token.value)
        self.eat(kw.REF)
        ids = self.ids()
        self.eat(kw.RBRACE)
        
        return nc.Reference(token,tensorid,ids)
        
    def show_statement(self):
        token = self.current_token
        self.eat(kw.show)
        self.eat(kw.LPAREN)
        if self.current_token.type==kw.ID:
            args = self.variable()
        else:
            args = self.reference()
        node = nc.Show(token, args)
        self.eat(kw.RPAREN)
        return node
    
    def variable(self):
        node = nc.Id(self.current_token)
        self.eat(kw.ID)
        return node

   
    def empty(self):
        return nc.NoOp()
    
    def order(self):
        token = self.current_token
        self.eat(kw.INT)
        return nc.Num(token)
    
    def ids(self):
        ids = []
        
        while self.current_token.type in (kw.COMMA,kw.ID):
            ids += [self.variable().token.value]
            if self.current_token.type not in (kw.COMMA,kw.ID):
                break
            self.eat(kw.COMMA)
        return ids
        
    def factor(self):
        token = self.current_token
     
        if token.type == kw.INT:
            self.eat(kw.INT)
            return nc.Num(token)
        elif token.type == kw.ID:
            node = self.variable()
            return node
        elif token.type == kw.LPAREN:
            self.eat(kw.LPAREN)
            node = self.expr()
            self.eat(kw.RPAREN)
            return node
        elif token.type == kw.DIF:
            self.eat(kw.DIF)
            node = self.expr()
            return nc.UnOp(token,node)
        elif token.type == kw.log:
            self.eat(kw.log)
            self.eat(kw.LPAREN)
            node = nc.UnOp(token,self.expr())
            self.eat(kw.RPAREN)
            return node
        elif token.type == kw.PART:
            self.eat(kw.PART)
            left = self.variable()
            self.eat(kw.LPAREN)
            right = self.expr()
            self.eat(kw.RPAREN)
            node = nc.BinOp(left,token,right)
            return node
        elif token.type == kw.diag:
            self.eat(kw.diag)
            self.eat(kw.LPAREN)
            ids=self.ids()
            self.eat(kw.RPAREN)
            self.eat(kw.UPCAR)
            order = self.order()
            node = nc.DiagTensor(ids,order)
            return node
            
    def term(self):
        node = self.factor()
        
        while self.current_token.type in (kw.MUL,kw.DIV):
            token = self.current_token
            newnode = nc.AsOp(MULTOKEN())
            newnode.args += [node]
            
            if token.type == kw.MUL:
                self.eat(kw.MUL)
                newnode.args += [self.factor()]
            elif token.type == kw.DIV:
                self.eat(kw.DIV)
                divnode = nc.AsOp(MULTOKEN(),weight = -1)
                divnode.args += [self.factor()]
                newnode.args += [divnode]
            
            node = newnode
                
        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (kw.ADD,kw.SUB):
            token = self.current_token
            newnode = nc.AsOp(ADDTOKEN())
            newnode.args += [node]
            
            
            if token.type == kw.ADD:
                self.eat(kw.ADD)
                newnode.args += [self.term()]
            elif token.type == kw.SUB:
                self.eat(kw.SUB)
                minnode = nc.AsOp(ADDTOKEN(),weight = -1)
                minnode.args += [self.term()]
                newnode.args += [minnode]
                
            node = newnode
                
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != kw.EOF:
            self.error()
        return node
