import classeProjet as Projet
import random
import shelve
from copy import deepcopy
from nouveauxAlgos import autreVersion, autreVersionA
from classeProjet import np as np
import emploiDuTemps as EDT
from recupererDonnee import makeStage
N_ETU = 5
N_FORMATEUR = 5
R_MIN = -50
R_MAX = 50
NOUVEAUTEST = False
NB_CONTRAINTE = 1
NB_ITERATION = 1000
NB_BINOME = 1
NUMERO_STAGE = 4
""" creation des données test"""
if NOUVEAUTEST:
    nomE = []
    for i in range(N_ETU):
        nomE.append("E"+str(i+1))
    
    nomF = []
    for i in range(N_FORMATEUR):
        nomF.append("F"+str(i+1))
        
    adresseE = []
    for i in range(N_ETU):
        adresseE.append((random.randint(R_MIN,R_MAX),random.randint(R_MIN,R_MAX)))
    
    adresseF = []
    for i in range(N_FORMATEUR):
        adresseF.append((random.randint(R_MIN,R_MAX),random.randint(R_MIN,R_MAX)))
    
    typeClasse = ['elem','moyen'] 
    
    EnsembleEtu = []
    for i in range(N_ETU):
        EnsembleEtu.append(Projet.Etudiant(nomE[i],adresseE[i],random.choice(typeClasse)))
    
    EnsembleForm = []
    # par défaut chaque formateur ne peut prendre qu'un seul étudiant
    for i in range(N_FORMATEUR):
        EnsembleForm.append(Projet.Formateur(nomF[i],adresseF[i],random.choice(typeClasse)))
    
    for x in EnsembleEtu:
        formTemp = random.sample(EnsembleForm,NB_CONTRAINTE)
        for f in formTemp:
            x.addContrainteFormateur(f)
    
    for x in EnsembleEtu:
        etuTemp=random.sample(EnsembleEtu,NB_BINOME)
        for b in etuTemp:
            x.addBinome(b)
    
    Stage = Projet.Stage(NUMERO_STAGE,EnsembleEtu,EnsembleForm)
    db=shelve.open('testRandom')
    db['EnsembleEtu']=EnsembleEtu
    db['EnsembleForm']=EnsembleForm
    db['Stage']=Stage
    db['ToutLesStages'] = {NUMERO_STAGE:Stage}
    db.close()
    """ fin création de données"""
else :
    test = shelve.open('bdTest')
    etu1 = Projet.Etudiant('E1','saxon','moyen',2)
    form1 = Projet.Formateur('F1','martigny','moyen',2)
    form2 = Projet.Formateur('F2','martigny','moyen',2)
    print(etu1.getDistance)
    etu1.distance(form1)
    print(etu1.getDistance)
    test['ToutLesStages']=etu1
    hum=deepcopy(etu1)
    test.close()
    test = shelve.open('bdTest')
    x = test['ToutLesStages']
    x.distance(form2)
    test['ToutLesStages']=x
    print(test['ToutLesStages'].getDistance)
    test.close()
#    test = shelve.open('bdTest')
#    stages=test['ToutLesStages']
#    stage4 = stages[4]
#    etu4 = deepcopy(stage4.lEtudiants)
#    form4 = deepcopy(stage4.lFormateurs)
#    for etu in etu4:
#        for form in form4:
#            print(etu.distance(form))
#    for etu in etu4:
#        for etu2 in etu4:
#            if etu2 != etu:
#                print(etu.distance(etu2))
#    for etu in etu4:
#        print('après calcul ',etu.getDistance)
#    newListeEtu = list()
#    for x in etu4:
#        dist = {etu:x.distance(etu) for etu in etu4}
#        dist2 = {form:x.distance(form) for form in form4}
#        dist.update(dist2)
#        newListeEtu.append(Projet.Etudiant(x.name,x.adresse,x.typeClasse,x.permis,dist))
#    newListeEtu=[Projet.Etudiant(etu.name,etu.adresse,etu.typeClasse,etu.permis,{etu2:etu.distance(etu2)
#    for etu2 in etu4})  for etu in etu4]
#    deepcopy(newListeEtu)
#    for etu in newListeEtu:
#        print(etu,etu.getDistance)
#    test.close()
#    hum = Projet.Stage(4,etu4,form4)
#    deepcopy(hum)
#    for x in hum.lEtudiants:
#        print(x.getDistance)
#    test2=shelve.open('avecDist')
#    test2['yo']=Projet.Stage(4,stage4.lEtudiants,stage4.lFormateurs)
#    print('dans nouvelle base ',test2['yo'])
#    test2.close()
#    testStage4 = makeStage('stage4E.txt', 'stage4F.txt')
#    lEtu = testStage4[4].lEtudiants
#    lForm = testStage4[4].lFormateurs
#    etu0 = lEtu[0]
#    for i in range(len(lForm)):
#        print(etu0.name,' distance avec ', lForm[i].name, ' de ', etu0.distance(lForm[i]))
#    jeuTest = shelve.open('testRandom')
#    EnsembleEtutS = jeuTest['EnsembleEtu']
#    EnsembleFormS = jeuTest['EnsembleForm']
#    StageTest = jeuTest['Stage']
#    EnsembleStage = jeuTest['ToutLesStages']
#    print(EnsembleEtutS)
#    print(EDT.separerTC(EnsembleEtutS))
#    res = Projet.nouvelleVersion(EnsembleEtutS, EnsembleFormS, 1)
#    print(res)
#    print(Projet.distanceCumulee(res))
#    print('-'*30)
#    for elem in jeuTest:
#        print(elem)
#    print(StageTest)
#    res = StageTest.attributionStage(10)
#    print(Projet.distanceCumulee(res))
#    print(StageTest.distanceOpti)
#    print(StageTest)
#    print(Projet.distanceCumulee(StageTest.attribution))
#    print(Projet.lire(StageTest.attribution))
#    def fun(LE,LF,nbIter):
#        LE = Projet.greedyBinome(LE,nbIter)[0]
#        LE = Projet.creerDoubleEtudiant(LE)
#        edt = Projet.edtVF(LE,LF,nbIter)
#        return  Projet.attributionNormale(edt)
    
#    def fun2(LE,LF,nbIter):
#        return Projet.nouvelleVersion(LE, LF, nbIter)

    

#    print(EDT.edtEfficace(EnsembleEtutS, EnsembleFormS))
#    print("-"*40)
#    print(EDT.emploiDuTemps(EnsembleEtutS,EnsembleFormS))