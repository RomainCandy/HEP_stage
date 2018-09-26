import random
import numpy as np
import warnings
# Si on arrive à une impasse les coordonnées ont été choisies
# pour dissuader de choisir une solution avec...
FANTOME = 'FANTOME'

_all__ = ['edtGreedy', 'edtGreedyA']


def separerTC(LP):
    res = {'elem': [], 'moyen': []}
    for personne in LP:
        res[personne.typeClasse].append(personne)
    return res


def lire(edt):
    res = ''
    for etu in edt:
        res += "l'étudiant " + str(etu) + " va avec le formateur " + str(edt[etu]) + '\n'
    return res


def distanceCumulee(edt):
    d = 0
    for etu in edt:
        try:
            if edt[etu] == FANTOME:
                return np.Inf
        except AttributeError:
            pass
        d += etu.distance(edt[etu])
    return d


def emploiDuTemps(LE, LF):
    """LE liste d'étudiants et LF liste de formateurs
    retourne un emploi du temps en utilisant un algo glouton"""
    random.shuffle(LE)
    edt = dict()
    d = 0
    LFP = [x for x in LF if x.prioritaire == 'oui']
    for Etudiant in LE:
        if not LFP:
            LFP = [x for x in LF if x.prioritaire == 'non']
            if not LFP:
                return edt, np.Inf
        LFP.sort(key=lambda x: Etudiant.distance(x))
        i = 0
        while (LFP[i] in Etudiant.getContrainteFormateur()) or (not LFP[i].restePlace()):
            if len(LFP) == i+1:
                return edt, np.Inf
            i += 1
        edt[Etudiant] = LFP[i]
        d = d + Etudiant.distance(LFP[i])
        LFP[i].addEtudiant(Etudiant)
    for x in LF:
        x.reset()
    return edt, d


def edtEfficace(LE, LF):
    random.shuffle(LE)
    LF1 = LF.copy()
    edt = dict()
    d = 0
    LF1P = [x for x in LF1 if x.prioritaire == 'oui']
    for etu in LE:
        LFCP = list(set(LF1P)-set(etu.getContrainteFormateur()))
        try:
            res = min(LFCP, key=lambda x: etu.distance(x))
        except ValueError:
            if not LF1P:
                LF1P = [x for x in LF1 if x.prioritaire == 'non']
                LFCR = list(set(LF1P)-set(etu.getContrainteFormateur()))
                try:
                    res = min(LFCR, key=lambda x: etu.distance(x))
                except ValueError:
                    return edt, np.Inf
            else:
                return edt, np.Inf
        d += etu.distance(res)
        edt[etu] = res
        try:
            LF1P.remove(res)
        except ValueError:
            raise ValueError('res = ', res, 'LF1 = ', LF1)
            
    return edt, d


def edtGreedy(LE, LF, n, variant='A'):
    edtF = None
    distance = np.Inf
    if variant == 'N':
        edt = emploiDuTemps
    else:
        edt = edtEfficace
    best = np.Inf
    for i in range(n):
        if (i*10) % n == 0:
            print((i*100)/n, '%')
        for x in LF:
            x.reset()
        edtTemp, distance = edt(LE, LF)
        if distance < best:
            best = distance
            edtF = edtTemp
    return edtF, distance


def permute1(seq):
    if not seq:
        return [seq]
    else:
        res = []
        for i in range(len(seq)):
            rest = seq[:i]+seq[i+1:]
            for x in permute1(rest):
                res.append(seq[i:i+1]+x)
        return res


def appliBij(X, Y):
    res = []
    for perm in permute1(X):
        res.append(list(zip(perm, Y)))
    return res


def possible(L):
    for etu, form in L:
        if form in etu.getContrainteFormateur():
            return False
    return True


def distBrute(L):
    d = 0
    for etu, form in L:
        try:
            if form == FANTOME:
                return np.Inf
        except AttributeError:
            pass
        d += etu.distance(form)
    return d


def bruteForce(LE, LF):
    ens = appliBij(LE, LF)
    d = np.Inf
    res = []
    for x in ens:
        if possible(x):
            if d > distBrute(x):
                d = distBrute(x)
                res = x
    edt = dict()
    for elem in res:
        edt[elem[0]] = elem[1]
    return edt, d


def lireBrute(res):
    x = ''
    print("commence la fin")
    for etu, form in res:
        x += "l'étudiant " + str(etu) + " va avec le formateur " + str(form) + '\n'
    return x


def emploiDuTempsA(LE, LF):
    """LE liste d'étudiants et LF liste de formateurs
    retourne un emploi du temps en utilisant un algo glouton"""
    if len(LE) != len(LF):
        warnings.warn('risque de probleme choisir plutot la version normale')
    d = 0
    random.shuffle(LE)
    edt = dict()
    LFtemp = LF[:]
    for Etudiant in LE:
        if len(LFtemp) <= 5:
            index = LE.index(Etudiant)
            edtB, distance = bruteForce(LE[index:], LFtemp)
            if edtB:
                edt.update(edtB)
            else:
                return edt, np.Inf
            return edt, d + distance
        LFC = list(set(LFtemp) - set(Etudiant.getContrainteFormateur()))
        try:
            res = min(LFC, key=lambda x: Etudiant.distance(x))
        except ValueError:
            return edt, np.Inf
        d += Etudiant.distance(res)
        edt[Etudiant] = res
        LFtemp.remove(res)
    return edt, d


def edtGreedyA(LE, LF, n):
    best = np.Inf
    edtF = None
    distance = np.Inf
    for i in range(n):
        if (i*10) % n == 0:
            print((i*100)/n, '%')
        edtTemp, distance = emploiDuTempsA(LE, LF)
        if distance < best:
            best = distance
            edtF = edtTemp
    return edtF, distance


def edtVF(LE, LF, n):
    assert len(LE) <= len(LF)
    if len(LE) == len(LF)-512:
        print('choisi edtgreedyA ligne 197')
        return edtGreedyA(LE, LF, n)
    else:
        print('choisi edtGreedy ligne 200')
        return edtGreedy(LE, LF, n, 'A')


def attributionNormale(edtED):
    """ edtED edt avec etudiant double en clé"""
    edtRes = dict()
    edt = edtED[0]
    distance = edtED[1]
    for etuD, form in edt.items():
        edtRes[etuD.id[0]] = form
        edtRes[etuD.id[1]] = form
    return edtRes, distance


""" autre idée on fait la création du doubleEtudiant et la recherche d'edt en une seule fois
puis on repete en changeant l'ordre"""