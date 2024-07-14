# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 20:56:05 2024

@author: lcuev
"""

def increment(arr,base):
    pos=0
    remainder=1
    while remainder and pos<len(arr):
        proposal=arr[pos] + remainder
        if proposal<base:
            arr[pos]=proposal
            remainder=0
        else:
            arr[pos]=0
            pos+=1
    return arr

class DiagTensor:
    def __init__(self, names, order):
        self.args = self.argsfromnames(names,order)
        
    def __getitem__(self, name):
        return self.args[name]
    
    def __setitem__(self,name,newitem):
        self.args[name]=newitem
        
    def argsfromnames(self,names,order):
        keys = []
        
        for name in names:
            key = (name,)*order
            keys += [key]

        return dict.fromkeys(keys)
        
        
        

names = ['x','y']
order = 2

T = DiagTensor(names,order)
T['x','x']=5
print(T['x','x'])


    