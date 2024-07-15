# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 19:30:44 2024

@author: lcuev
"""
import nodeclasses as nc
from token_ import ADDTOKEN,MULTOKEN
from derivers import PartialDeriver
     
def getdichargs(dime):
    args = {}
    for u,ukey in enumerate(dime.args.keys()):
        args[ukey*3]=nc.NUM(1)
        for v,vkey in enumerate(dime.args.keys()):
            if u!=v:
                args[vkey*2+ukey]=nc.NUM(1)
                args[tuple(sorted(ukey+vkey))+ukey]=nc.NUM(1)
    
    
    invdime=dime.inverse()
    for key in args.keys():
        u,v,l=key
        uid,vid,lid=nc.ID(u),nc.ID(v),nc.ID(l)
        if u==v==l:
            mulop = nc.AsOp(MULTOKEN(),weight=0.5)
            mulop.args += [dime[(u,)]]
            mulop.args += [PartialDeriver(uid,invdime[(u,)]).derive()]
            addop=nc.AsOp(ADDTOKEN())
            addop.args += [mulop]
            args[key]=addop
        elif u==v:
            mulop = nc.AsOp(MULTOKEN(),weight=-0.5)
            mulop.args += [dime[(l,)]]
            mulop.args += [PartialDeriver(lid,invdime[(u,)]).derive()]
            addop=nc.AsOp(ADDTOKEN())
            addop.args += [mulop]
            args[key]=addop
        elif u==l:
            mulop = nc.AsOp(MULTOKEN(),weight=0.5)
            mulop.args += [dime[(u,)]]
            mulop.args += [PartialDeriver(vid,invdime[(u,)]).derive()]
            addop=nc.AsOp(ADDTOKEN())
            addop.args += [mulop]
            args[key]=addop
        elif v==l:
            mulop = nc.AsOp(MULTOKEN(),weight=0.5)
            mulop.args += [dime[(v,)]]
            mulop.args += [PartialDeriver(uid,invdime[(v,)]).derive()]
            addop=nc.AsOp(ADDTOKEN())
            addop.args += [mulop]
            args[key]=addop
    
    return args