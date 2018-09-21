from emploiDuTemps import edtVF, attributionNormale, emploiDuTemps, separerTC, edtEfficace
from emploiDuTemps import np as np
from emploiDuTemps import random as rd
from creerBinome import _greedyBinomeR
from getDistances import distanceAdresse
import unidecode
import shelve



def formater(s):
    res = unidecode.unidecode(s)
#    res = res.replace(' ','+')
    res = res.replace(' ','+')+'+suisse'
    return res

class Distance:

    def __init__(self, precompute_distance: str):
        self.precompute_distance = precompute_distance
        with shelve.open(precompute_distance) as db:
            try:
                self.all_distances = db['distance']
                self.villes = set((x for x, _ in self.all_distances))
            except KeyError:
                self.all_distances = dict()
                db['distance'] = dict()
                self.villes = set()
        self.changes = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save()

    def get_distance(self, ville1, ville2):
        try:
            return self.all_distances[(ville1, ville2)]
        except KeyError:
            try:
                adresseO = formater(ville1)
                adresse = formater(ville2)
                dist = distanceAdresse(adresse , adresseO)
                self.all_distances[(ville1, ville2)] = dist
                self.all_distances[(ville2, ville1)] = dist
                self.changes = True
                return dist
            except KeyError:
                raise AttributeError("l'adresse {} ou "
                                     "l'adresse {} a un probleme."
                                     "Impossible de calculer "
                                     "la durÃ©e du trajet.".format(ville1,
                                                                 ville2))

    def add_distance(self, ville1, ville2, d):
        self.changes = True
        self.all_distances[(ville1, ville2)] = d
        self.all_distances[(ville2, ville1)] = d

    def add_ville(self, ville):
        self.changes = True
        if ville not in self.villes:
            for v in self.villes:
                d = float(input('distance beetween '
                                '{} and {}: '.format(v, ville)))
                self.add_distance(ville, v, d)
        self.villes.add(ville)

    def add_everything(self, all_villes):
        for ville in all_villes:
            self.add_ville(ville)

    def save(self):
        if self.changes:
            with shelve.open(self.precompute_distance) as db:
                db['distance'] = self.all_distances

Dist = Distance('distance/test_dist_stages')
D = Dist.all_distances

class Personne:
    
    def __init__(self, name, adresse, typeClasse, numStage, corresp = 'distance/correspondance'):
        assert numStage in list(range(7))
        global D
        # pour l'instant adresse est un np.array représentant les coordonnées
        assert typeClasse in ['elem', 'moyen']
        self.name = name
        self.adresse = adresse
        self.typeClasse = typeClasse
        self.numStage = numStage
        if corresp != None:
            with shelve.open(corresp) as db:
                temp = db['corresp']
                if adresse in temp:
                    self.adresse = temp[adresse]

    def distance(self, other):
       """ calcul la distance entre deux personnes """
       if self.typeClasse != other.typeClasse:
           return np.Inf
       if (type(other) is Formateur or type(self) is Formateur) and self.adresse.strip().lower() == other.adresse.strip().lower():
           return np.Inf
       if type(other) == type(self) == Etudiant and self.adresse.strip().lower() == other.adresse.strip().lower():
           return 0
       try:
           return D[(self.adresse, other.adresse)]
       except KeyError:
            raise AttributeError("la distance entre {} ({}) et {} ({})"
                                 "n'est pas rentrée dans la matrice".format(
                                         self.adresse,
                                         self.name,
                                         other.adresse,
                                         other.name))
               
    def changerAdresse(self,nAdresse):
        self.adresse = nAdresse
#        self.getDistance = dict()
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name 
    def __eq__(self,other):
        return ((self.name == other.name) and (self.adresse == other.adresse))
    
    def __hash__(self):
        return hash(self.name+str(self.adresse))
        
        
class Etudiant(Personne):
    
    def __init__(self, name, adresse, typeClasse, numStage, permis=True):
        Personne.__init__(self, name, adresse, typeClasse, numStage)
        self.dejaFormateur=[]
        self.binome = []
        self.permis=permis
    
    def addContrainteFormateur(self,formateur):
        """ suppose que formateur est un Formateur"""
        self.dejaFormateur.append(formateur)
    
    def supprContrainteFormateur(self, formateur):
        self.dejaFormateur.remove(formateur)
    
    
    def getStage(self):
        return self.numStage
    
    def addBinome(self,etudiant):
        try:
            self.binome.extend(etudiant)
            self.binome = list(set(self.binome))
            etudiant.binome.extend(self)
            etudiant.binome = list(set(etudiant.binome))
        except TypeError:
            self.binome.append(etudiant)
            self.binome = list(set(self.binome))
            etudiant.binome.append(self)
            etudiant.binome = list(set(etudiant.binome))
    
    def supprBinome(self,etudiant):
        try:
            for etu in etudiant:
                self.binome.remove(etu)
                etu.binome.remove(self)
        except TypeError:
            self.binome.remove(etudiant)
            etudiant.binome.remove(self)
    
    def getBinome(self):
        return self.binome
    
    def distance(self, other):
                
        if not self.permis:
            try:
                if not other.gare:
                    return np.Inf
#                    return (100*Personne.distance(self, other)+1000000)
            except AttributeError:
                pass
            try:
                if not other.permis:
                    return  (100*Personne.distance(self, other))
            except AttributeError:
                return Personne.distance(self, other)
        return Personne.distance(self, other)
    
    def getContrainteFormateur(self):
        return self.dejaFormateur
    
    def pasPossible(self, other):
        return other in self.getBinome()
    
    def changerPermis(self):
        self.permis = not(self.permis)
#        self.getDistance = dict()
    

class DoubleEtudiant:    
    def __init__(self,etu1 , etu2):
        self.name = str(etu1.name) + ' -_- ' +  str(etu2.name)
        self.id = (etu1, etu2)
        self.dejaFormateur = list(set(etu1.getContrainteFormateur())|set(etu2.getContrainteFormateur()))
    
    def distance(self, other):
        return (self.id[0].distance(other) + self.id[1].distance(other))
    
    def getContrainteFormateur(self):
        return self.dejaFormateur
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)

class Formateur(Personne):
    
    def __init__(self, name, adresse, typeClasse, numStage, prioritaire='non', 
                 gare=True):
        Personne.__init__(self, name, adresse, typeClasse, numStage)
        """ si le nb d'étudiant que peut accueillir un formateur peut varier le dire huhu"""
        prioritaire = prioritaire.strip()
        assert prioritaire in ['oui', 'non']
        self.nbEtumax = 1
        self.etudiantEnFormation = []
        self.prioritaire = prioritaire
        self.gare = gare
        
    def reset(self):
        self.etudiantEnFormation = []
    
    def addEtudiant(self,etudiant):
        assert self.restePlace()
        self.etudiantEnFormation.append(etudiant)
    
    """restePlace inutile maintenant?"""
    def restePlace(self):
        return len(self.etudiantEnFormation) < self.nbEtumax
    
    def changerGare(self):
        self.gare = not(self.gare)
#        self.getDistance = dict()
    
    def changerPrio(self):
        if self.prioritaire == 'oui':
            self.prioritaire = 'non'
        else:
            self.prioritaire = 'oui'
#        self.getDistance = dict()
    
    def getStage(self):
        return self.numStage
    

        
    
class Stages:
    """ si on met le defaut à [] prend toute les instances avec défaut comme etant les même"""
    def __init__(self, lEtudiants=None, lFormateurs=None, version=0):
#        assert numeroStage in list(range(1,7))
        self.lEtudiants = lEtudiants
        self.lFormateurs = lFormateurs
        self.version = version
        self.attribution = {i:[] for i in range(1,7)}
        
        
    def ajoutListeEtu(self, lE):
        if self.lEtudiants is None:
            self.lEtudiants = lE
        for etu in lE:
            self.ajoutEtudiant(etu)
            
    def ajoutListeForm(self, lF):
        if self.lFormateurs is None:
            self.lFormateurs = lF
        for form in lF:
            self.ajoutFormateur(form)
        
    def changerVersion(self):
        self.version = not self.version
    
    def ajoutEtudiant(self, etu):
        if etu:
            if self.lEtudiants is None:
                self.lEtudiants = [etu]
            elif etu not in self.lEtudiants:
                self.lEtudiants.append(etu)
        
    def ajoutFormateur(self,form):
        if form :
            if self.lFormateurs is None:
                self.lFormateurs = [form]
            elif form not in self.lFormateurs:
                self.lFormateurs.append(form)
    
    def supprEtudiant(self,etu):
        for binome in etu.getBinome():
            etu.supprBinome(binome)
        self.lEtudiants.remove(etu)
        
    def supprFormateur(self,form):
        self.lFormateurs.remove(form)
    
    def getListeEtudiants(self):
        return self.lEtudiants
    
    def getListeFormateurs(self):
        return self.lFormateurs
    
    def getListeEtuStage(self, i):
        return [etu for etu in self.getListeEtudiants() if etu.numStage == i]
    
    def getListeFormStage(self, i):
        return [form for form in self.getListeFormateurs() if form.numStage == i]
    
    def attributionStage(self, numStage, nbIter=100000):
        """ quels sont les stages où ils doivent être tout seul?
        """
        
        LE = self.getListeEtuStage(numStage)
        LF = self.getListeFormStage(numStage)
        sepLE = separerTC(LE)
        LEelem = sepLE['elem']
        LEmoyen = sepLE['moyen']
        sepLF = separerTC(LF)
        LFelem = sepLF['elem']
        LFmoyen = sepLF['moyen']
        if numStage in [5,6]:
            if len(LEelem) <= len(LFelem) and len(LEmoyen)<= len(LFmoyen):
                self.attribution[numStage], distanceOptiElem = edtVF(LEelem,LFelem,nbIter)
                attributionMoyen,distanceOptiMoyen = edtVF(LEmoyen,LFmoyen,nbIter)
                self.distanceOpti = distanceOptiElem + distanceOptiMoyen
                self.attribution[numStage].update(attributionMoyen)
            else:
                self.attribution[numStage], self.distanceOpti= edtVF(LE,LF,nbIter)
                print("probleme possible d'équilibre")
        else:
            if self.version == 0:
                if len(LEelem) <= len(LFelem)*2 and len(LEmoyen) <= len(LFmoyen)*2:
                    print("version opti avec elem d'un coté et de l'autre moyen")
                    self.attribution[numStage], self.distanceOpti = nouvelleVersion(LEelem, LFelem, nbIter)
                    attributionMoyen,distanceMoyen = nouvelleVersion(LEmoyen,LFmoyen,nbIter)
                    self.attribution[numStage].update(attributionMoyen)
                    self.distanceOpti += distanceMoyen
                else:
                    print('elem ',LEelem,LFelem)
                    print('moyen ',LEmoyen,LFmoyen)
                    raise UnboundLocalError('pas équilibré au moins un étudiant ne va pas avoir un stage dans sa classe'
                                            + 'changer de version ou changer les classes ')
            elif self.version == 1:
                self.attribution[numStage], self.distanceOpti = nouvelleVersion(LE, LF, nbIter)
        if not self.attribution[numStage]:
            raise UnboundLocalError('aucune attribution trouvée')
        return self.attribution[numStage]
    
    def update(self, numStage):
        assert self.attribution
        for etu, form in self.attribution[numStage].items():
            etu.addContrainteFormateur(form)
            if etu.numStage in list(range(1, 5)):
                for etu2,form2 in self.attribution[numStage].items():
                    if etu != etu2 and form == form2:
                        etu.addBinome(etu2)
                        
    def changerAttribution(self, etu1, etu2):
        assert etu1 in self.getListeEtudiants() and etu2 in self.getListeEtudiants() and etu1.numStage == etu2.numStage
        self.attribution[etu1],self.attribution[etu2] = self.attribution[etu2],self.attribution[etu1]
    
    def reset(self):
        self.attribution = dict()
        
    def garderPersonnes(self):
        self.lEtudiants = [etu for etu in self.lEtudiants if etu.getStage() in list(range(7))]
        self.lFormateurs = [form for form in self.lFormateurs if form.getStage() in list(range(7))]
    
    def __str__(self):
        return "Stage "+  " etudiant: " + str(self.getListeEtudiants()
                             )+" formateurs: " + str(self.getListeFormateurs())

    def __repr__(self):
        return str(self)
        
        
def creerDoubleEtudiant(LB):
    res = []
    for binome in LB:
        try:
            res.append(DoubleEtudiant(binome[0], binome[1]))
        except IndexError:
            
            res.append(DoubleEtudiant(binome[0], binome[0]))
    return res
            
def _nouvelleVersionR(LE,LF):
    try:
        NLE, distance = _greedyBinomeR(LE, variant='G')
        DNLE = creerDoubleEtudiant(NLE)
#        edtTemp, distEdt = emploiDuTemps(DNLE, LF)
        edtTemp, distEdt = edtEfficace(DNLE, LF)
    except AttributeError as exc:
        """moche mais pour gerer les erreurs liées au fait qu'on ne trouve pas d'attribution..."""
        raise UnboundLocalError(exc.args)
    return edtTemp, distEdt

def nouvelleVersion(LE,LF, nbIter):
    best = np.Inf
    rd.shuffle(LE)
    for i in range(nbIter):
        if (i*10)%nbIter == 0:
            print((i*100)/nbIter,'%')
        for x in LF:
            x.reset()
        etd, distance = _nouvelleVersionR(LE, LF)
        if distance < best:
            best = distance
            edtF = etd
    return attributionNormale((edtF, best))


#FANTOME = Formateur('Fantome','paris','elem',1,'oui')

if __name__ == '__main__':
    pass
#    etu = Etudiant('E1','martigny','elem',1)
#    etu2 = Etudiant('E2', 'conthey', 'elem',1)
#    form = Formateur('F1','martigny','elem',1)
#    detu = DoubleEtudiant(etu, etu2)
#    print(detu.distance(form))

        
        
