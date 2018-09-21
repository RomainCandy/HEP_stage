#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 22:41:13 2017


reflechir à un moyen de ne pas retrier tout le temps les listes...
voir comment faire marcher tout ça sur mac
@author: romain
"""

import sys
import os
import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter.messagebox import showerror, askokcancel, showinfo
import classeProjet as cP
import tkinter.filedialog  as tkf
import shelve
from time import asctime
from functools import reduce
from recupererDonnee import makeStage, makeListeEtudiant,PasAuNormeEtu,PasAuNormeForm,makeListeFormateur
from urllib.request import URLError

if sys.platform.startswith('linux'):
    extension = "*.bak"

elif sys.platform.startswith('darwin'):
    extension = '*.bd'

else:
    extension = "*.bak"

class Application(tk.Frame):
    def __init__(self,root,file=''):
        tk.Frame.__init__(self)
        self.root = root
        self.file = file
        self.tempTout = cP.Stages()
        self.hasSaved = True
        self.toutLesStages = cP.Stages()
        self.make_gui()

        
    def make_gui(self):
        self.master.title('Projet tifemme' + self.file)


        self.width = 40
        self.height = 6
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.toptop = tk.Frame(self)
        
        self.top = tk.Frame(self)
        self.top.pack(side = tk.TOP, fill=tk.BOTH)
        
        self.buttonS1 = tk.Button(self.top, width= self.width, height = self.height, text='voir stage 1', command=lambda :self.getStage(1))
        self.buttonS1.pack(side = tk.LEFT)
        
        self.buttonS2 = tk.Button(self.top,width= self.width, height = self.height, text='voir stage 2', command= lambda :self.getStage(2))
        self.buttonS2.pack(side = tk.LEFT)
        
        self.buttonS3 = tk.Button(self.top,width= self.width, height = self.height, text='voir stage 3', command= lambda :self.getStage(3))
        self.buttonS3.pack(side = tk.LEFT)
        
        self.middle = tk.Frame(self)
        self.middle.pack(side= tk.TOP, fill=tk.X)
        
        self.buttonS4 = tk.Button(self.middle,width= self.width, height = self.height, text='voir stage 4', command= lambda :self.getStage(4))
        self.buttonS4.pack(side = tk.LEFT)
        
        self.buttonS5 = tk.Button(self.middle,width= self.width, height = self.height, text='voir stage 5', command= lambda :self.getStage(5))
        self.buttonS5.pack(side = tk.LEFT)
        
        self.buttonS6 = tk.Button(self.middle,width= self.width, height = self.height, text='voir stage 6', command= lambda :self.getStage(6))
        self.buttonS6.pack(side = tk.LEFT)
        
        for i in range(1,7):
            self.root.bind("<F" + str(i)+">",lambda event,i=i: self.getStage(i,event))
        
        self.bot = tk.Frame(self)
        self.bot.pack(side= tk.TOP,fill=tk.X)
        
        self.buttonQ = tk.Button(self.bot,width= self.width, height = self.height, text='Quitter', command= self.quit)
        self.buttonQ.pack(side = tk.LEFT)
        
        self.buttonL = tk.Button(self.bot,width= self.width, height = self.height, text='charger les données', command= self.load)
        self.buttonL.pack(side = tk.LEFT)
        
        self.buttonSa = tk.Button(self.bot,width= self.width, height = self.height, text='sauvegarder', 
                                  command= self.save)
        self.buttonSa.pack(side = tk.LEFT)
        
        
        self.botbot = tk.Frame(self)
        self.botbot.pack(side= tk.TOP,fill=tk.X)
        tk.Button(self.botbot,width= self.width, height = self.height, text='n->n+1E', 
                  command= lambda: self.toutBouger('etudiant',lambda x:x+1)).pack(side= tk.LEFT)
        
        
        """ a remettre si cela s'avère utile
        tk.Button(self.botbot,width= self.width, height = self.height ,text='n->n+1F',state=tk.DISABLED,
                  command= lambda: self.toutBouger('formateur',lambda x:x-1)).pack(side= tk.LEFT)
        """
        
        tk.Button(self.botbot,width=self.width, height = self.height, text='importer les données pour la premiere utilisation',
                  command= self.importerDonnee).pack(side=tk.LEFT)
        """
        tk.Button(self.botbot,width= self.width, height = self.height ,text='n->n+1T',state=tk.DISABLED,
                  command= lambda: self.toutBouger('tout',lambda x:x-1)).pack(side= tk.LEFT)
        """
        tk.Button(self.botbot,width= self.width, height = self.height ,text='ajouter donnée',
                  command= self.ajouterDonnee).pack(side= tk.LEFT)
        
        
        self.botbotbot = tk.Frame(self)
        self.botbotbot.pack(side= tk.TOP,fill=tk.X)
        tk.Button(self.botbotbot,width= self.width, height = self.height ,text='n->n-1E', 
                  command= lambda: self.toutBouger('etudiant',lambda x: x-1)).pack(side= tk.LEFT)
        tk.Button(self.botbotbot,width= self.width, height = self.height ,text='n->n-1F',state=tk.DISABLED,
                  command= lambda: self.toutBouger('formateur',lambda x: x+1)).pack(side= tk.LEFT)
        tk.Button(self.botbotbot,width= self.width, height = self.height ,text='n->n-1T',state=tk.DISABLED,
                  command= lambda: self.toutBouger('tout',lambda x: x+1)).pack(side= tk.LEFT)
    
    def ajouterDonnee(self):
        if self.file:
            self.gen = GeneriqueTopLevelListe(self, champ=['liste des stages, fichier .txt',self.choixAjoutFile],
                                              selection= 'multiple')
            self.gen.genbListe.delete(0, tk.END)
            self.gen.bind("<Return>",self.choixFile)
            files = os.listdir('.')
            self.filesTxt = [file for file in files if ".txt" in file or ".xlsx" in file ]
            for file in self.filesTxt:
                self.gen.genbListe.insert(tk.END,file)
        else:
            showerror(message='aucune base séléctionnée')
    
    def choixAjoutFile(self, event = None):
        index = self.gen.genbListe.curselection()
        if not len(index):
            showerror(title="Erreur", message="il faut choisir au moins un fichier avant de compléter la base")
        else:
            nLE = []
            nLF = []
            choix = [self.filesTxt[i] for i in index]
            for choice in choix:
                try:
                    etuts = makeListeEtudiant(choice)
                    nLE += etuts
                except PasAuNormeEtu:
                    try:
                        forms = makeListeFormateur(choice)
                        nLF += forms
                    except PasAuNormeForm :
                        showerror(title='Erreur', message= "le fichier %s n'est pas aux normes, rappel "%(choice) +  
                                " pour un étudiant nomeE,adresseE,tc,stage" + 
                                " pour un formateur nomF,adresseF,tc,stage ")
                        return
            self.tempTout.ajoutListeEtu(nLE)
            self.tempTout.ajoutListeForm(nLF)
            self.gen.destroy()
            
    def importerDonnee(self):
        self.gen = GeneriqueTopLevelListe(self, champ=['liste des stages, fichier .txt',self.choixFile],selection= 'multiple')
        self.gen.genbListe.delete(0, tk.END)
        self.gen.bind("<Return>",self.choixFile)
        files = os.listdir('.')
        self.filesTxt = [file for file in files if ".txt" in file or ".xlsx" in file ]
        for file in self.filesTxt:
            self.gen.genbListe.insert(tk.END,file)

    
    def choixFile(self,event = None):
        index = self.gen.genbListe.curselection()
        if not len(index):
            showerror(title="Erreur", message="il faut choisir au moins un fichier avant de créer la base")
        else:
            choix = [self.filesTxt[i] for i in index]
            try:
                stageTemp = makeStage(*choix)
                result= tkf.asksaveasfilename(title="Sauver la nouvelle base de donnée:",
                                      filetypes=(("", extension),
                                        ("Tout fichier", "")),
                               initialfile="Nom par défaut",
                               defaultextension="")
                name=result[:-(len(extension)-1)]
                db = shelve.open(name)
                db['ToutLesStages']=stageTemp
                self.file = name
                self.recupereDonnee()
                self.gen.destroy()
            except ValueError as exc:
                showerror(title="Erreur", message=exc.args)
    
    def toutBouger(self,typePersonne, fun):
        for etu in self.tempTout.lEtudiants:
            etu.numStage = fun(etu.numStage)
        showinfo(message="changement effectué")
        print(self.tempTout.lEtudiants)
        """
        res = dict()
        for key in range(0,8):
            if typePersonne == 'etudiant':
                try:
                    LF = self.tempTout[key].getListeFormateurs()
                except KeyError:
                    LF = None
                try:
                    LE = self.tempTout[fun(key)].getListeEtudiants()
                except KeyError:
                    LE = None
                res[key]=cP.Stages(key, LE, LF)
            elif  typePersonne == 'formateur':
                try:
                    LF = self.tempTout[fun(key)].getListeFormateurs()
                except KeyError:
                    LF = None
                try:
                    LE = self.tempTout[key].getListeEtudiants()
                except KeyError:
                    LE = None
                res[key]=cP.Stages(key, LE, LF)
            elif typePersonne == 'tout':
                try:
                    LF = self.tempTout[fun(key)].getListeFormateurs()
                except KeyError:
                    LF = None
                try:
                    LE = self.tempTout[fun(key)].getListeEtudiants()
                except KeyError:
                    LE = None
                res[key]=cP.Stages(key, LE, LF)
        self.tempTout = res
        showinfo(message="changement effectué")
        self.hasSaved = False
        """
    def quit(self):
        if not self.hasSaved:
            if askokcancel("Quit", "Des modifications n'ont pas été sauvegardées, quitter quand même?", parent=self, default=tkmsg.OK):
                self.root.destroy()
        else:
            if askokcancel("Quit", "Quitter projet tifemme?", parent=self, default=tkmsg.OK):
                self.root.destroy()
        
    def recupereDonnee(self):
        jeuTest = shelve.open(self.file)
        try:
            self.toutLesStages= jeuTest['ToutLesStages']
        except KeyError:
            self.toutLesStages = cP.Stages()
        self.tempTout = self.toutLesStages
        jeuTest.close()
    
    def getStage(self,i,event= None):
        self.hasSaved = False
        try: 
            etu = self.tempTout.getListeEtuStage(i)
        except AttributeError:
            etu = []
        try:
            form= self.tempTout.getListeFormStage(i)
        except AttributeError:
            form = []
        FenetreStage(self,i,etu,form)
        
        
        
    def load(self):
        result = tkf.askopenfilename(title="Ouvrir un fichier:",
                             filetypes=(("", extension),
                                        ("Tout fichier", "*")))
        self.file = result[:-(len(extension)-1)]
        self.recupereDonnee()
        if result:
            showinfo(title= "Chargement", message= "Chargement des données effectuées")
        self.master.title('Projet tifemme ' + self.file)
    
    def save(self):
        result= tkf.asksaveasfilename(title="Sauver un fichier:",
                                      filetypes=(("", extension),
                                        ("Tout fichier", "*")),
                               initialfile="Nom par défaut",
                               defaultextension="")
        self.file = result[:-(len(extension)-1)]
        if self.file:
            db = shelve.open(self.file)
            self.tempTout.garderPersonnes()
            self.toutLesStages = self.tempTout
            print(self.tempTout)
            db['ToutLesStages'] = self.toutLesStages
            db.close()
            print('aucun probleme')
            self.hasSaved = True

class FenetreStage(tk.Toplevel):
    def __init__(self,root,numStage,lEtu,lForm):
        tk.Toplevel.__init__(self)
        self.title('Stage ' + str(numStage))
        self.root = root
        self.root.hasSaved = False
        self.numStage = numStage
        self.changement = False
        self.LE=lEtu
        self.LF = lForm
        self.root.tempTout.ajoutListeEtu(lEtu)
        self.root.tempTout.ajoutListeForm(lForm)
        self.stage = self.root.toutLesStages
        self.init_gui()
        self.updateAffichage()
        
    def init_gui(self):
        
        self.etudiant1 = tk.Frame(self, height = 200, width = 200)
        self.etudiant1.pack(side = tk.LEFT, expand=tk.YES, padx=5, pady=5)

        self.formateur1 = tk.Frame(self, height= 200, width= 200)
        self.formateur1.pack(side= tk.LEFT, expand= tk.YES, padx= 5, pady= 5)
        
        self.formateur_frame = tk.Frame(self.formateur1)
        self.formateur_frame.pack(side = tk.BOTTOM)
        
        self.FormateurTitre = tk.Label(self.formateur1, text='Liste des formateurs du stage ' + str(self.numStage))
        self.FormateurTitre.pack(side = tk.TOP)
        
        self.etudiant_frame = tk.Frame(self.etudiant1)
        self.etudiant_frame.pack(side = tk.BOTTOM)
        
        self.etudiantTitre = tk.Label(self.etudiant1, text='Liste des étudiants du stage ' + str(self.numStage))
        self.etudiantTitre.pack(side = tk.TOP)
        
        self.scrollbarE = tk.Scrollbar(self.etudiant_frame, orient= tk.VERTICAL)
        self.bListeE = tk.Listbox(self.etudiant_frame, background='yellow', height = 20, width=50,
                                  yscrollcommand= self.scrollbarE.set)
        self.scrollbarE.config(command=self.bListeE.yview)
        self.scrollbarE.pack(side=tk.RIGHT, fill= tk.Y)
        self.bListeE.pack(side= tk.TOP)
        
        self.barreE = tk.Frame(self.etudiant_frame,background='black')
        self.barreE.pack(side= tk.LEFT, fill=tk.X, expand=False)
        self.modifierEtu = tk.Button(self.barreE, text="voir étudiant", command = self.modifierEtudiant)
        self.modifierEtu.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.supprimerEtu = tk.Button(self.barreE, text="supprimer étudiant", command= self.supprEtudiant)
        self.supprimerEtu.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.ajouterEtu = tk.Button(self.barreE, text="ajouter étudiant", command= lambda: self.addPersonne('etudiant'))
        self.ajouterEtu.pack(side=tk.LEFT, expand=True, fill=tk.X)
                
        self.scrollbarF = tk.Scrollbar(self.formateur_frame, orient=tk.VERTICAL)
        self.bListeF = tk.Listbox(self.formateur_frame, background='white', height = 20, width = 50,
                                  yscrollcommand= self.scrollbarF.set)
        self.scrollbarF.config(command=self.bListeF.yview)
        self.scrollbarF.pack(side=tk.RIGHT, fill=tk.Y)
        self.bListeF.pack(side= tk.TOP)
        
        self.barreF = tk.Frame(self.formateur_frame,background='black')
        self.barreF.pack(side= tk.LEFT, fill=tk.X, expand=False)
        self.modifierForm = tk.Button(self.barreF, text="voir formateur", command= self.modifierFormateur )
        self.modifierForm.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.supprimerForm = tk.Button(self.barreF, text="supprimer formateur",command=self.supprFormateur)
        self.supprimerForm.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.ajouterForm = tk.Button(self.barreF, text="ajouter formateur", command=lambda: self.addPersonne('formateur'))
        self.ajouterForm.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        
        self.attribution1 = tk.Frame(self, height = 200, width = 200)
        self.attribution1.pack(side = tk.RIGHT, expand=tk.YES, padx=5, pady=5)
        
        self.attributionTitre = tk.Label(self.attribution1, text='attribution de stages proposée')
        self.attributionTitre.pack(side = tk.TOP)
        
        self.attribution_frame = tk.Frame(self.attribution1)
        self.attribution_frame.pack(side = tk.BOTTOM)
        
        self.scrollbarA = tk.Scrollbar(self.attribution_frame, orient=tk.VERTICAL)
        self.bListeA = tk.Listbox(self.attribution_frame, background='white', height = 20, width = 50,
                                  yscrollcommand= self.scrollbarA.set)
        self.scrollbarA.config(command=self.bListeA.yview)
        self.scrollbarA.pack(side=tk.RIGHT, fill=tk.Y)
        self.bListeA.pack(side= tk.TOP)
        
        self.barreA = tk.Frame(self.attribution_frame,background='black')
        self.barreA.pack(side= tk.LEFT, fill=tk.X, expand=False)
        self.modifierA = tk.Button(self.barreA, text="générer attribution", command= self.genererEdt)
        self.modifierA.pack(side=tk.LEFT, expand=True)
        
        tk.Button(self.barreA, text="changer de version", command= self.changerVersionAlgo).pack(side= tk.LEFT)
        tk.Button(self.barreA, text="accepter attribution", command= self.updateContrainte).pack(side= tk.LEFT)
        
        tk.Button(self.barreA, text="permuter etudiants", command= self.changerAttribution).pack(side= tk.LEFT)
        
        self.bind("<Control-e>", lambda event: self.addPersonne('etudiant',event))
        self.bind("<Control-E>", lambda event: self.addPersonne('etudiant',event))
        
        self.bind("<Control-f>", lambda event: self.addPersonne('formateur',event))
        self.bind("<Control-F>", lambda event: self.addPersonne('formateur',event))
        
        self.bListeE.bind("<Return>", self.modifierEtudiant)
        self.bListeE.bind("<Double-ButtonRelease>", self.modifierEtudiant)
        
        self.bListeF.bind('<Return>', self.modifierFormateur)
        self.bListeF.bind('<Double-ButtonRelease>', self.modifierFormateur)
        
    def changerAttribution(self):
        
        index = self.bListeA.curselection()
        if not len(index):
            showerror(title= 'probleme choix etudiant',message= " il faut d'abord choisir un étudiant avant de pouvoir permuter ")
        else:
            self.LE.sort(key = lambda x:x.name)
            self.etu1 = self.LE[index[0]]
            self.gen = GeneriqueTopLevelListe(self, champ=['permuter %s avec '%(self.etu1.name),self.permutation])
            self.gen.title = 'yo'
            self.gen.genbListe.delete(0, tk.END)
            self.gen.bind("<Return>",self.permutation)
            for etu in self.LE:
                self.gen.genbListe.insert(tk.END,etu)
                self.updateAffichage()

    def permutation(self,event = None):
        
        index = self.gen.genbListe.curselection()
        etu2 = self.LE[index[0]]
        self.stage.changerAttribution(self.etu1,etu2)
        self.attributionFinale = self.stage.attribution
        self.gen.destroy()
        self.updateAffichage()
        
    
    def updateContrainte(self):
        if self.changement:
            showerror(title= "Changement", message= 'Il y a eu des modifications depuis la dernière attribution de stage. ' +
                      "Faites une nouvelle attribution de stage avant de pouvoir l'accepter")
        else:
            try :
                self.stage.attribution[self.numStage]
                print('yoooooo ',self.stage.attribution[self.numStage])
                result = askokcancel(title = "Confirmation", message= "Toutes les contraintes de l'emploi du temps proposé" + 
                                     ' seront ajoutées à tous les étudiants, continuer?')
                if result:
                    self.stage.update(self.numStage)
            except AttributeError as exc:
                showerror(title= 'Erreur', message= "Il faut générer un stage avant de pouvoir l'accepter" + str(exc.args))
                
    
    def changerVersionAlgo(self):
        self.stage.changerVersion()
        self.changement = True
    
    def supprEtudiant(self):
        index = self.bListeE.curselection()
        if len(index) == 1:
            etu = self.LE[index[0]]
            self.supprEtu= askokcancel(message="enlever " + etu.name + "du stage " + str(self.numStage))
            if self.supprEtu:
                self.stage.supprEtudiant(etu)
        self.updateAffichage()
        self.changement = True
        
    def supprFormateur(self):
        index = self.bListeF.curselection()
        if len(index) == 1:
            form = self.LF[index[0]]
            self.supprForm= askokcancel(message="enlever " + form.name + "du stage " + str(self.numStage))
            if self.supprForm:
                self.stage.supprFormateur(form)
        self.updateAffichage()
        self.changement = True
                
    def addPersonne(self,typePersonne, event= None):
        self.changement = True
        self.addEtu = Saisie(self, typePersonne= typePersonne)
    
    def ajouterEtudiant(self, etudiant):
        self.changement = True
        self.stage.ajoutEtudiant(etudiant)
        self.updateAffichage()
    
    def ajouterFormateur(self, etudiant):
        self.changement = True
        self.stage.ajoutFormateur(etudiant)
        self.updateAffichage()
    
    def genererEdt(self):
        
        self.bListeA.delete(0, tk.END)
        try:
            self.attributionFinale = self.stage.attributionStage(self.numStage)
            for etu in sorted(self.attributionFinale, key=lambda x:str(x)):
                if etu.typeClasse != self.attributionFinale[etu].typeClasse:
                    self.bListeA.insert(tk.END, '-'*50)
                    self.bListeA.insert(tk.END, str(etu.name) + " va avec " + str(self.attributionFinale[etu].name))
                    self.bListeA.insert(tk.END, '-'*50)
                else:
                    self.bListeA.insert(tk.END, str(etu.name) + " va avec " + str(self.attributionFinale[etu].name))
            print('somme temps: ', self.stage.distanceOpti)
            self.changement = False
            self.root.tempTout =self.stage
            for x in self.LE:
                pass
        except UnboundLocalError as exc:
            showerror(title= 'aucune attribution trouvée',message= "aucune attribution trouvée, vérifier peut-être les données rentrées ou changer de version"+
                      str(exc.args))
        except AttributeError as exc:
            showerror(title="probleme dans le calcul d'une distance", message= exc.args)
        except URLError as exc:
            showerror(title= "probleme connexion", message= exc.reason)
        
        for etu in self.stage.lEtudiants:
            if etu.getStage() == 5:
                print(etu.name,len(etu.getDistance))
        
    def updateAffichage(self):
        
        self.LE = self.stage.getListeEtuStage(self.numStage)
        self.LF = self.stage.getListeFormStage(self.numStage)
        if self.LE:
            self.LE.sort(key= lambda x: x.name)
        if self.LF:
            self.LF.sort(key= lambda x:x.name)
        self.bListeE.delete(0, tk.END)
        self.bListeF.delete(0, tk.END)
        if self.LE:
            for etu in sorted(self.LE, key=lambda x:str(x)):
                self.bListeE.insert(tk.END, etu)
        if self.LF:
            for form in sorted(self.LF, key=lambda x:str(x)):
                self.bListeF.insert(tk.END, form)
        self.bListeA.delete(0, tk.END)
        
        try:
            for etu in sorted(self.stage.attribution[self.numStage], key=lambda x:str(x)):
                if etu.typeClasse != self.stage.attribution[self.numStage][etu].typeClasse:
                    self.bListeA.insert(tk.END, '-'*50)
                    self.bListeA.insert(tk.END, str(etu.name) + " va avec " + str(self.stage.attribution[self.numStage][etu].name))
                    self.bListeA.insert(tk.END, '-'*50)
                else:
                    self.bListeA.insert(tk.END, str(etu.name) + " va avec " + str(self.stage.attribution[self.numStage][etu].name))
            print(self.stage.distanceOpti)
        except AttributeError or TypeError:
            pass
        
    def modifierEtudiant(self, event= None):
        try:
            index = self.bListeE.curselection()[0]
            self.LE.sort(key = lambda x:x.name)
            self.info = InfoPersonne(self, self.LE[index],self.numStage, typePersonne='etudiant')
        except IndexError:
            pass
        self.updateAffichage()
        self.changement = True
    
    def modifierFormateur(self, event= None):
        try:
            index = self.bListeF.curselection()[0]
            self.LF.sort(key = lambda x:x.name)
            self.info = InfoPersonne(self, self.LF[index],self.numStage, typePersonne='formateur')
        except IndexError:
            pass
        self.updateAffichage()
        self.changement = True
    
    def save(self):
        db = shelve.open('temp')
        db['ToutlesStages'] = self.toutLesStages
        db.close()
        print('aucun probleme2')
        
class InfoPersonne(tk.Toplevel):
    def __init__(self,root, personne,numStage, typePersonne = 'etudiant'):
        tk.Toplevel.__init__(self)
        self.title('Information ' + typePersonne )
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.root = root
        self.numStage = numStage
        self.file = 'temp' + reduce(lambda x,y:x+y,asctime().split(' ')[:2])
        self.personne = personne
        self.typePersonne = typePersonne
        tk.Label(self, text = 'Nom:').grid(row = 0, sticky = tk.E)
        self.LabelNom = tk.Label(self, text=personne.name)
        self.LabelNom.grid(row = 0, column = 1)
        tk.Label(self, text = 'Adresse:').grid(row = 1, sticky = tk.E)
        self.LabelAdresse = tk.Label(self, text=personne.adresse)
        self.LabelAdresse.grid(row = 1, column = 1)
        for i in range(2):
            tk.Button(self,text='modifier', 
                      command = lambda i=i:self.modification(i)).grid(row=i, column=2,sticky = tk.W)
        
        tk.Label(self, text="type classe").grid(row= 2, sticky= tk.E)
        typeClasse =['elem', 'moyen']
        self.choixtypeClasse = tk.StringVar()
        self.choixtypeClasse.set(self.personne.typeClasse)
        for i in range(2):
            self.radioTypeClasse = tk.Radiobutton(self,text = typeClasse[i],
                                                  variable=self.choixtypeClasse,
                                                  value = typeClasse[i],
                                                  command=self.changerType)
        
            self.radioTypeClasse.grid(row = 2, column = i+1)
        
        
        if typePersonne == 'etudiant':
            tk.Label(self, text='déja formé par').grid(row= 3, sticky= tk.E)
            tk.Label(self, text= personne.getContrainteFormateur()).grid(row = 3, column = 1)
            tk.Label(self, text='a déjà été en binôme avec').grid(row= 4, sticky= tk.E)
            tk.Label(self, text= personne.getBinome()).grid(row = 4, column = 1)

            tk.Label(self, text='a le permis').grid(row= 5, sticky= tk.E)
            tk.Label(self, text= bool(personne.permis)).grid(row = 5, column = 1)
            for i in range(2,4):
                tk.Button(self,text='ajouter', command = lambda i=i:self.modification(i)).grid(row=i+1, column=2,sticky = tk.W)
                tk.Button(self,text='supprimer', command = lambda i=i:self.modification(i,1)).grid(row=i+1, column=3)
            tk.Button(self,text='changer', command = self.changer).grid(row= i+2, column= 2)
            tk.Button(self, text='n->n+1', command=lambda: self.changerAnnee('etudiant',lambda x:x+1)).grid(row=i+3, column = 2,sticky = tk.W)
            tk.Button(self, text='n->n-1', command=lambda: self.changerAnnee('etudiant',lambda x:x-1)).grid(row=i+4, column = 2,sticky = tk.W)
        elif typePersonne == 'formateur':
        
            tk.Label(self, text='gare proche').grid(row= 3, sticky= tk.E)
            tk.Label(self, text= bool(personne.gare)).grid(row = 3, column = 1)
        
            tk.Button(self,text='changer', command = self.changerG).grid(row= i+2, column= 2,sticky = tk.W)
            tk.Button(self, text='n->n+1', command=lambda: self.changerAnnee('formateur',lambda x:x+1)).grid(row=i+4, column = 2,sticky = tk.W)
            tk.Button(self, text='n->n-1', command=lambda: self.changerAnnee('formateur',lambda x:x-1)).grid(row=i+5, column = 2,sticky = tk.W)
            tk.Label(self, text="prioritaire").grid(row= i+3, sticky= tk.E)
            prioritaire =['oui', 'non','zzzz']
            self.choixPrioritaire = tk.StringVar()
            self.choixPrioritaire.set(self.personne.prioritaire)
            for j in range(2):
                self.radioPrio = tk.Radiobutton(self,text = prioritaire[j],
                                                  variable=self.choixPrioritaire,
                                                  value = prioritaire[j],
                                                  command=self.changerPrio)
        
                self.radioPrio.grid(row = i+3, column = j+1)
        self.buttonValide = tk.Button(self, text="valider saisie", command= self.validerSaisie)
        self.buttonValide.grid(row = 10, column = 1)
        
        self.bind("<Return>", self.validerSaisie)
    
    def quit(self):
        self.update()
        self.destroy()
    
    def changerAnnee(self,typePersonne, fun):

        self.personne.numStage = fun(self.personne.numStage)

        
    def modification(self, i,j=0):
        if i == 0:
            self.gen = GeneriqueTopLevelSimple(self,champ=['nouveau nom',self.validerNom])
            self.gen.bind("<Return>", self.validerNom)
        elif i == 1:
            self.gen= GeneriqueTopLevelSimple(self,champ=['nouvelle adresse',self.validerAdresse])
            self.gen.bind("<Return>", self.validerAdresse)
        elif i == 2 and j == 0:
            self.gen = GeneriqueTopLevelListe(self, champ=['ajouter formateur',self.validerAjoutFormateur],
                                              selection='multiple')
            self.pasDejaFormateur = [form for form in self.root.LF if form not in self.personne.getContrainteFormateur()]
            self.gen.genbListe.delete(0, tk.END)
            self.gen.bind("<Return>", self.validerAjoutFormateur)
            for form in self.pasDejaFormateur:
                self.gen.genbListe.insert(tk.END,form.name)
        
        elif i == 2 and j == 1:
            self.gen = GeneriqueTopLevelListe(self, champ=['supprimer formateur',self.validerSupprFormateur],selection='multiple')
            self.dejaFormateur = [form for form in self.root.LF if form in self.personne.getContrainteFormateur()]
            self.gen.genbListe.delete(0, tk.END)
            self.gen.bind("<Return>", self.validerSupprFormateur)
            for form in self.dejaFormateur:
                self.gen.genbListe.insert(tk.END,form.name)
                
        
        elif i == 3 and j == 0:
            self.gen = GeneriqueTopLevelListe(self, champ=['ajouter binome',self.validerAjoutBinome],selection='multiple')
            self.pasDejaBinome = [etu for etu in self.root.LE if etu not in self.personne.getBinome() and etu != self.personne]
            self.gen.genbListe.delete(0, tk.END)
            self.gen.bind("<Return>", self.validerAjoutBinome)
            for etu in self.pasDejaBinome:
                self.gen.genbListe.insert(tk.END,etu.name)
        
        elif i == 3 and j == 1:
            self.gen = GeneriqueTopLevelListe(self, champ=['supprimer binome',self.validerSupprBinome],selection='multiple')
            self.dejaBinome = [etu for etu in self.root.LE if etu in self.personne.getBinome()]
            self.gen.genbListe.delete(0, tk.END)
            self.gen.bind("<Return>", self.validerSupprBinome)
            for etu in self.dejaBinome:
                self.gen.genbListe.insert(tk.END,etu.name)
        
        
    
    def validerAjoutFormateur(self,event=None):
        index = self.gen.genbListe.curselection()
        if len(index) > 0:
            for i in index:
                self.personne.addContrainteFormateur(self.pasDejaFormateur[i])
        self.gen.destroy()
        self.updateVu()
    
    def validerSupprFormateur(self,event=None):
        index = self.gen.genbListe.curselection()
        if len(index) > 0:
            for i in index:
                self.personne.supprContrainteFormateur(self.dejaFormateur[i])
        self.gen.destroy()
        self.updateVu()
        
    def validerAjoutBinome(self,event=None):
        index = self.gen.genbListe.curselection()
        if len(index) > 0:
            for i in index:
                self.personne.addBinome(self.pasDejaBinome[i])
        self.gen.destroy()
        self.updateVu()
    
    def validerSupprBinome(self,event=None):
        index = self.gen.genbListe.curselection()
        if len(index) > 0:
            for i in index:
                self.personne.supprBinome(self.dejaBinome[i])
        self.gen.destroy()
        self.updateVu()
        
    
    def changer(self):
        self.personne.changerPermis()
        self.updateVu()
    
    def changerG(self):
        self.personne.changerGare()
        self.updateVu()
    
    def changerType(self):
        typeClasse = self.choixtypeClasse.get()
        self.personne.typeClasse = typeClasse
        
    def changerPrio(self):
        prio = self.choixPrioritaire.get()
        self.personne.prioritaire = prio
        self.personne.getDistance = dict()
    
    def validerSaisie(self,event=None):
        self.root.updateAffichage()
        self.destroy()
    
    def validerNom(self,event=None):
        x = self.gen.entreeGen.get()
        self.personne.name = x.strip()
        self.gen.destroy()
        self.updateVu()
        
    def validerAdresse(self,event=None):
        x = self.gen.entreeGen.get()
        x = x.strip()
        try:
            self.personne.changerAdresse(x)
            self.gen.destroy()
            self.updateVu()
        except ValueError:
            showerror(message="pas d'erreurs possibles normalement")
        
    
    
    def updateVu(self):
        tempP = self.personne
        tempR = self.root
        tempV = self.typePersonne
        self.destroy()
        self.__init__(tempR, tempP,self.numStage, tempV)
    
class GeneriqueTopLevelSimple(tk.Toplevel):
    def __init__(self, root, champ= []):
        tk.Toplevel.__init__(self)
        self.root = root
        descr, fun = champ
        tk.Label(self, text=descr).pack()
        self.entreeGen= tk.Entry(self)
        self.entreeGen.pack()
        tk.Button(self, text='valider', command= fun).pack()
        self.bind("<Return>", fun)
            

class GeneriqueTopLevelListe(tk.Toplevel):
    def __init__(self, root, champ= [],selection = None):
        tk.Toplevel.__init__(self)
        self.root = root
        descr,fun = champ
        tk.Label(self, text=descr).pack()
        self.genScrollbar = tk.Scrollbar(self, orient= tk.VERTICAL)
        if selection == None:
            self.genbListe = tk.Listbox(self, height = 20, width= 50,
                                        yscrollcommand= self.genScrollbar.set)
        else: 
            self.genbListe = tk.Listbox(self, height = 20, width= 50,
                                        yscrollcommand= self.genScrollbar.set, selectmode = 'multiple')
        self.genScrollbar.config(command=self.genbListe.yview)
        self.genScrollbar.pack(side=tk.RIGHT, fill= tk.Y, padx=5,pady=5)
        self.genbListe.pack(side= tk.TOP)
        tk.Button(self, text="ok", command= fun).pack()
        self.bind("<Return>", fun)

        

class Saisie(tk.Toplevel):
    
    def __init__(self,root, typePersonne):
        tk.Toplevel.__init__(self)
        self.root = root
        self.geometry('300x100+300+200')
        self.title('Nouveau ' + typePersonne)
        self.typePersonne = typePersonne
        tk.Label(self, text = 'Nom').grid(row = 0, sticky = tk.E)
        self.entryNom = tk.Entry(self)
        self.entryNom.grid(row = 0, column = 1)
        tk.Label(self, text = 'Adresse').grid(row = 1, sticky = tk.E)
        self.entryAdresse = tk.Entry(self)
        self.entryAdresse.grid(row = 1, column = 1)
        
        tk.Label(self, text = 'Type Classe').grid(row = 2, sticky = tk.E)
        typeClasse =['elem', 'moyen']
        self.choixtypeClasse = tk.StringVar()
        self.choixtypeClasse.set(typeClasse[0])
        for i in range(2):
            self.radioTypeClasse = tk.Radiobutton(self,text = typeClasse[i],
                                                  variable=self.choixtypeClasse,
                                                  value = typeClasse[i])
        
            self.radioTypeClasse.grid(row = 2, column = i+1)
        
        
        
        
        self.buttonValide = tk.Button(self, text="valider saisie", command = self.valide)
        self.buttonValide.grid(row = 3, column = 1)
        self.bind("<Return>", self.valide)
    
    def valide(self,event=None):
        adresse = self.entryAdresse.get()
        nom = self.entryNom.get()
        typeClasse = self.choixtypeClasse.get()
        ok = False
        if nom and adresse:
            nom = nom.strip()
            adresse = adresse.strip()
            try:
                ok = True
            except ValueError:
                    showerror(message="l'adresse à la forme x y où x y sont des nombres")
        else:
            showerror(message= 'il manque une donnée')
        if ok:
            if self.typePersonne == 'etudiant':
                nouveauEtudiant = cP.Etudiant(nom, adresse,typeClasse,self.root.numStage)
                self.root.ajouterEtudiant(nouveauEtudiant)
            elif self.typePersonne == 'formateur':
                nouveauFormateur = cP.Formateur(nom, adresse,typeClasse,self.root.numStage)
                self.root.ajouterFormateur(nouveauFormateur)
            self.destroy()
 
    
    
def start():          
    root = tk.Tk(None, None, "Projet tifemme huhu")
    app = Application(root)
    app.mainloop()
    
if __name__ == '__main__':
    start()




