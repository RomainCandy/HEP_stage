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
