from emploiDuTemps import FANTOME
from emploiDuTemps import random as rd
from emploiDuTemps import np as np

__all__=['greedyBinome','bruteForceBin']

def listeBinome(L,res=[]):
    if not L:
        return (res,)
    if len(L) == 1:
        return [res+[(L,)]]
    temp = L[:]
    x=temp.pop()
    aRes=[]
    for i in range(len(temp)):
        aRes += listeBinome(temp[:i]+temp[i+1:],res+[(x,temp[i])])
    return aRes
    

def _greedyBinomeR(LE,variant,res=[],d=0):
    """ LE liste d'étudiants
    renvoi une liste où chaque élément est une paire d'étudiant
    avec la distance correspondante"""
    assert variant in ['G','BG']
    if variant is 'G':
        if not LE:
            return (res),d
        if len(LE) == 1:
            return res + [(LE)],d
    elif variant is 'BG':
        if len(LE)<= 10:
            bestR = bruteForceBin(LE)
            return res + bestR[0],d+bestR[1]
    temp = LE.copy()
    etu = temp.pop()
    temp.sort(key=lambda x:etu.distance(x))
    i = 1
    etuBi = temp[0]
    while(etu.pasPossible(etuBi)):
        try:
            etuBi = temp[i]
        except IndexError:
            return res + [(etu,FANTOME)],np.Inf
        i+=1
    temp.remove(etuBi)
    return _greedyBinomeR(temp,variant,res + [(etu,etuBi)],d+etu.distance(etuBi))
    
def greedyBinome(LE,nbIter,variant='G'):
    d = np.Inf
    print("avancement greedyBinome")
    for i in range(nbIter):
        
        if not int((i+1)*100/nbIter) %10:
            print(int((i+1)*100/nbIter),'%')
            
        rd.shuffle(LE)
        arrangement,distance = _greedyBinomeR(LE,variant)
        if distance<d:
            d = distance
            listeBinome = arrangement
    print('fin greedyBinome')
    try:
        return listeBinome,d
    except UnboundLocalError:
        raise UnboundLocalError("L'algo n'a pas pu former une paire de binome. "
                                +"Peut être un problème avec la liste des binomes"
                                +" deja formée")
    

def computeDistance(LB):
    d = 0
    for binome in LB:
        if(len(binome) == 1):
            return d
        if binome[0].pasPossible(binome[1]):
            return np.Inf
        d+=binome[0].distance(binome[1])
    return d
        
def bruteForceBin(LE):
    tout = listeBinome(LE)
    distances = list(map(lambda x:computeDistance(x),tout))
    i = np.argmin(distances)
    return tout[i],min(distances)


