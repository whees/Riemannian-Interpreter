import keywords as kw
import derivers as dv
import nodevisitor as nv
import nodeclasses as nc
from token_ import MULTOKEN,ADDTOKEN
from parser_ import Parser
from lexer import Lexer
import riemann as ri


WEIGHT_KEYS = {kw.ADD: '*', 
               kw.MUL: '^'}

class Interpreter(nv.NodeVisitor):
    GLOBAL_SCOPE = {}
    
    def __init__(self):
        pass
    
    def visit_DiMeRef(self,node):
        var_name = node.arg.token.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is not None:
            return val
        else:
            NameError(f'no metric named {node.token.value} in global scope')
    
    
    
    def visit_DiMeRefToCh(self,node):
        dime=self.visit(node.arg)
        if dime.token.type == kw.dime:
            node=nc.DiCh(node.token)
            node.args=ri.getdichargs(dime)
            for key in node.args.keys():
                node.args[key] = self.visit(node.args[key])
            
            return node
        else:
            raise Exception(f'{node.arg.token.value} is not a tensor')
            
    def visit_DiCh(self,node):
        return node
        
    
    def visit_DiMe(self,node):
        return node
    
    def visit_UnOp(self,node):
        if node.token.type == kw.DIF:
            node = self.visit(dv.FunctionalDeriver(node.arg).derive())
        return node
    
    def visit_BinOp(self,node):
        if node.token.type == kw.PART:
            node = self.visit(dv.PartialDeriver(node.left,node.right).derive())
        return node
    
    def visit_Num(self,node):
        return node
    
    def visit_Var(self,node):
        return node
    
    def visit_Id(self,node):
        var_name = node.token.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is not None:
            node = self.visit(val)
        return node
    
    def visit_NoOp(self,node):
        pass
        
    def visit_AsOp(self, node):    
        newnode = nc.AsOp(node.token,node.weight)
               
        for arg in node.args:
            newnode.args += [self.visit(arg)]
        
        newnode = self.chain(newnode)  
        newnode = self.string(newnode)
        newnode = self.combinelike(newnode)
        newnode = self.trim(newnode)
        return newnode
    
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)
            
    def visit_Assign(self, node):
        if node.left.token.type == kw.ID:
            var_name = node.left.token.value
            self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
        elif node.left.token.type == kw.REF:
            var_name = node.left.tensorid.token.value
            ids = tuple(node.left.ids)
            self.GLOBAL_SCOPE[var_name][ids] = self.visit(node.right)
        else:
            raise Exception(f'cannot assign value to type {node.left.token.type}')
        
        
    def visit_Show(self, node):
        if node.args.token.type == kw.ID:
            var_name = node.args.token.value
            val = self.GLOBAL_SCOPE.get(var_name)
            if val is None:
                raise NameError(f'{var_name} does not exist in global scope')
            else:
                self.show(val)
        elif node.args.token.type == kw.REF:
            var_name = node.args.tensorid.token.value
            ids = tuple(node.args.ids)
            val = self.GLOBAL_SCOPE[var_name][ids]
            if val is None:
                raise NameError(f'{var_name} does not exist in global scope')
            else:
                self.show(val)
        else:
            raise Exception(f'cannot print argument of type {node.token.type}')
            
            
    def show(self,node):              
        string = ''
        
        if isinstance(node,nc.AsOp):
            for i,arg in enumerate(node.args):
                string += str(node.token.value)*int(i>0)+self.arg_string(arg,node.token) 
                string += (WEIGHT_KEYS[node.token.type] + f'({arg.weight})') * int(arg.weight!=1)
        elif isinstance(node,nc.Id):
            string += str(node.token.value) 
        elif isinstance(node,nc.Var):
            string += '&' * node.order + str(node.token.value)
        elif isinstance(node,nc.Num):
            string += str(node.token.value)
            
        print(string)
        
    def arg_string(self,node,token):
        string = ''
        if isinstance(node,nc.Id):
            return '(' + str(node.token.value) + ')'
        elif isinstance(node,nc.Var):
            return   '(' + '&' * node.order + str(node.token.value) + ')'
        elif isinstance(node,nc.Num):
            return str(node.token.value)
        
        if len(node.args) == 0:
            return '('+str(node.token.value) + (WEIGHT_KEYS[token.type] + str(node.weight)) * int(node.weight!=1)+')'
        

        string += '{'
        for i,arg in enumerate(node.args):
            string += str(node.token.value)*int(i>0)+self.arg_string(arg,node.token) 
            string += (WEIGHT_KEYS[node.token.type] + f'({arg.weight})') * int(arg.weight!=1)
            
        string += '}'
        return string
            
    def trim(self,node):
        if not isinstance(node,nc.AsOp):
            return node
        if node.token.type == kw.MUL:
            for arg in node.args:
                if arg.token.value == 0:
                    return nc.NUM(0)
        
        newnode = nc.AsOp(node.token, weight = node.weight)
        for arg in node.args:
            if arg.weight != 0 and (arg.token != nc.NUM(0).token and node.token == ADDTOKEN() or arg.token != nc.NUM(1).token and node.token == MULTOKEN()):
                newnode.args += [arg]
        
        if not len(newnode.args):
            if node.token.type == kw.MUL:
                return nc.NUM(1)
            elif node.token.type == kw.ADD:
                return nc.NUM(0)
                
        return newnode

    def string(self,node):
        if not isinstance(node,nc.AsOp):
            return node
        if node.weight == 1 and len(node.args) == 1 and node.token.type != kw.DIF:
            if node.args[0].weight == 1:
                return node.args[0]
        
        return node              
        
    def combinelike(self,node):
        if not isinstance(node,nc.AsOp):
            return node
        
        newnode = nc.AsOp(node.token,weight=node.weight)
        
        for arg in node.args:
            if arg in newnode.args:
                i = newnode.args.index(arg)
                newnode.args[i].weight += arg.weight
            else:
                newnode.args += [arg]
            
        return newnode
    
    def chain(self,node):
        if not isinstance(node,nc.AsOp):
            return node
        
        newnode = nc.AsOp(node.token,weight=node.weight)
        
        for arg in node.args:
            if arg.token.type == node.token.type and (arg.weight == 1 or len(node.args) == 1):
                for argarg in arg.args:
                    argargcopy = argarg.copy()
                    argargcopy.weight *= arg.weight
                    newnode.args += [argargcopy]
            else:
                newnode.args += [arg]
                
        return newnode
                        
    def interpret(self):
        while True:
            try:
                text = input('> ')
            except EOFError:
                break
            
            if not text:
                continue
            lexer = Lexer(text)
            parser = Parser(lexer)
            tree = parser.parse()
            tree = self.visit(tree)