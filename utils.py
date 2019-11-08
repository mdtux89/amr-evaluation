#!/usr/bin/env python
#coding=utf-8

'''
Various routines used by scores.py
'''

def disambig(lst):
    lst2 = []
    for v in lst:
        idx = 1
        v_idx = v + '_0'
        while str(v_idx) in lst2:
            v_idx = v + '_' + str(idx)
            idx += 1
        lst2.append(str(v_idx))
    return lst2

def concepts(v2c_dict):
    return [str(v) for v in v2c_dict.values()]

def namedent(v2c_dict, triples):
    return [str(v2c_dict[v1]) for (l,v1,v2) in triples if l == "name"]

def negations(v2c_dict, triples):
    return [v2c_dict[v1] for (l,v1,v2) in triples if l == "polarity"]    

def wikification(triples):
    return [v2 for (l,v1,v2) in triples if l == "wiki"]

def reentrancies(v2c_dict, triples):
    lst = []
    vrs = []
    for n in v2c_dict.keys():
        parents = [(l,v1,v2) for (l,v1,v2) in triples if v2 == n and l != "instance"]
        if len(parents) > 1:
            #extract triples involving this (multi-parent) node
            for t in parents:
                lst.append(t)
                vrs.extend([t[1],t[2]])
    #collect var/concept pairs for all extracted nodes
    dict1 = {}
    for i in v2c_dict:
         if i in vrs:
            dict1[i] = v2c_dict[i]
    return (lst, dict1)

def srl(v2c_dict, triples):
    lst = []
    vrs = []
    for t in triples:
        if t[0].startswith("ARG"):
            #although the smatch code we use inverts the -of relations
            #there seems to be cases where this is not done so we invert
            #them here
            if t[0].endswith("of"):
                lst.append((t[0][0:-3],t[2],t[1]))
                vrs.extend([t[2],t[1]])
            else:
                lst.append(t)
                vrs.extend([t[1],t[2]])

    #collect var/concept pairs for all extracted nodes            
    dict1 = {}
    for i in v2c_dict:
        if i in vrs:
            dict1[i] = v2c_dict[i]
    return (lst, dict1)

def var2concept(amr):
    v2c = {}
    for n, v in zip(amr.nodes, amr.node_values):
        v2c[n] = v
    return v2c
