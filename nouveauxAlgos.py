#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 12:06:40 2017

@author: romain
"""


from classeProjet import rd as rd
from emploiDuTemps import emploiDuTemps

def diviser(L,d):
    L1 = rd.sample(L,d)
    L2 = [x for x in L if x not in L1]
    rd.shuffle(L2)
    return L1, L2

#n = 10
#print(diviser(list(range(n)),(n+1)//2))

def _autreVersionR(LE, LF):
    LE1, LE2= diviser(LE,(len(LE)+1)//2)
    edt, d = emploiDuTemps(LE1,LF)
    LF1 = [x for x in edt.values()]
    for x in LF1:
        x.reset()
    edt2, d2 = emploiDuTemps(LE2,LF1)
    edt.update(edt2)
    for x in LF1:
        x.reset()
    return edt, d+d2

def _autreVersionRA(LE, LF):
    LE1, LE2= diviser(LE,(len(LE)+1)//2)
    edt, d = edtEfficace(LE1,LF)
    LF1 = [x for x in edt.values()]
    edt2, d2 = edtEfficace(LE2,LF1)
    edt.update(edt2)
    return edt, d+d2


def edtEfficace(LE,LF):
    rd.shuffle(LE)
    dejaVu = []
    edt = dict()
    d = 0
    for etu in LE:
        LFC = list(set(LF)-set(dejaVu+etu.getContrainteFormateur()))
        try:
            res = min(LFC, key= lambda x: etu.distance(x))
        except ValueError:
            return edt, 1000000000
        d += etu.distance(res)
        edt[etu] = res
    return edt, d





def autreVersion(LE, LF, nbIter):
    best = 10000000
    edtF = 'rien'
    for i in range(nbIter):
        edt, distance = _autreVersionR(LE, LF)
        if distance < best:
            edtF = edt
            best = distance
    return edtF, best

def autreVersionA(LE, LF, nbIter):
    rd.shuffle(LE)
    best = 10000000
    edtF = 'rien'
    for i in range(nbIter):
        edt, distance = _autreVersionRA(LE, LF)
        if distance < best:
            edtF = edt
            best = distance
    return edtF, best
