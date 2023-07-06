import random
from time import sleep
import os
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
from ia import *


class TarotException(Exception):
    pass

class CoupImpossibleException(TarotException):
    pass

class ErrorDefausse(TarotException):
    pass


class Carte:

    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur
    
    #methode pour comparer deux cartes
    def __lt__(self, other):
        pass
    
    def __gt__(self, other):
        pass
    

    def __eq__(self, other):
        return self.couleur == other.couleur and self.valeur == other.valeur


class Jeu:
    def __init__(self, nb_joueurs, nb_cartes):
        self.nb_joueurs:int = nb_joueurs
        self.nb_cartes:int = nb_cartes
        self.mains:list[list[tuple[str, int]]] = [[] for _ in range(nb_joueurs)]
        self.creer_paquet()
        self.melanger_paquet()
        self.gagnant_actuel:int = None
        self.ancien_plis:list = []
        self.preneur:int = None
        self.ancien_plis_couleur:dict[str, int] = {"Coeur":0, "Carreau":0, "Trefle":0, "Pique":0, "Atout":0, "Excuse":0}
        self.joueur_physique:int = 0
        self.qui_tour:int = 0
        self.pts:list[int] = [0 for _ in range(nb_joueurs)]
        self.bouts:list[int] = [0 for _ in range(nb_joueurs)]



    def creer_paquet(self):
        self.paquet = []
        for couleur in ["Coeur", "Carreau", "Trefle", "Pique"]:
            for valeur in range(1, 15):
                self.paquet.append((couleur, valeur))
        for i in range(1, 22):
            self.paquet.append(("Atout", i))
            
        self.paquet.append(("Excuse", 0))
            

    def melanger_paquet(self):
        random.shuffle(self.paquet)

    
    def trier_mains(self):
        for i in range(self.nb_joueurs):
            self.mains[i].sort(key=lambda x: x[1])
            self.mains[i].sort(key=lambda x: x[0])
            

    def distribuer_cartes(self):
        for _ in range(self.nb_cartes):
            for i in range(self.nb_joueurs):
                if len(self.paquet) > 6:
                    carte = self.paquet.pop(0)
                    self.mains[i].append(carte)
                else:
                    return

    def afficher_mains(self):
        txt = ""
        for i in range(self.nb_joueurs):
            
            txt += Fore.RESET + f"Main du joueur {i}:"
            for carte in self.mains[i]:
                txt += self.traitement_couleur_carte(carte)
            txt += "\n"

        print(txt)
        return txt


    def afficher_main_joueur(self, joueur):
        txt = "Main du joueur"
        main = self.mains[joueur]
        for carte in main:
            txt += self.traitement_couleur_carte(carte)
        print(txt)
        return txt

    def traitement_couleur_carte(self, carte):
        match carte[0]:
                case "Coeur":
                    return Fore.RED + f" {carte[1]}♥"
                case "Carreau":
                    return Fore.MAGENTA + f" {carte[1]}♦"
                case "Trefle":
                    return Fore.BLUE + f" {carte[1]}♣"
                case "Pique":
                    return Fore.GREEN + f" {carte[1]}♠"
                case "Atout":
                    return Fore.YELLOW + f" {carte[1]}"
                case "Excuse":
                    return Fore.YELLOW + f" Excuse"

    
    def gestion_chien(self, i):
        print("Chien : ")
        self.afficher_paquet()
        while self.paquet != []:
            self.mains[i].append(self.paquet.pop())
        self.afficher_main_joueur(i)
        couleur = input("Couleur -> ")
        valeur = int(input("Valeur -> "))
        carte = (couleur, valeur)
        for _ in range (6):
            while carte not in self.mains[i]:
                print("\nPas dans la main", carte)
                self.afficher_main_joueur(i)
                couleur = input("Couleur -> ")
                valeur = int(input("Valeur -> "))
                carte = (couleur, valeur)
            self.mains[i].remove(carte)
            if (i != 6):
                self.afficher_main_joueur(i)
                couleur = input("Couleur -> ")
                valeur = int(input("Valeur -> "))
                carte = (couleur, valeur)  


    def afficher_paquet(self):
        for carte in self.paquet:
            print(carte)

    def afficher_cartes(self, cartes, debut_txt=""):
        txt = debut_txt
        for carte in cartes:
            txt += self.traitement_couleur_carte(carte)
        return txt

            
    def jouer_carte(self, i:int, plis_actuel:list = []):
        print("")
        self.afficher_main_joueur(i)
        if plis_actuel != []:
            coup_possible = self.liste_coup_possible(i, plis_actuel)
            print(self.afficher_cartes(coup_possible ,"Les coups possibles sont: "))
        couleur = input("Couleur (Coeur, Pique, Trefle, Carreau, Atout, Excuse) -> ")
        valeur = int(input("Valeur -> "))
        carte = (couleur, valeur)
        while carte not in self.mains[i]:
            print("Pas dans la main")
            couleur = input("Couleur -> ")
            valeur = int(input("Valeur -> "))
            carte = (couleur, valeur)
        return carte
    
    def actualiser_ancien_plis_couleur(self, plis_actuel):
        for carte in plis_actuel:
            if carte[0] == "Atout":
                self.ancien_plis_couleur["Atout"] += 1
            else:
                self.ancien_plis_couleur[carte[0]] += 1
    


    def manche_rayan(self):
        plis_actuel = []
        for i in range(self.nb_joueurs):
            joueur_actuel = (self.qui_tour + i) % self.nb_joueurs
            if i == 0:
                self.gagnant_actuel = joueur_actuel

            if joueur_actuel == self.joueur_physique:
                txt = "Plis actuel: " + self.afficher_cartes(plis_actuel)
                print(txt)
                carte = self.jouer_carte(joueur_actuel, plis_actuel)
                #carte = simulation_coup(self, joueur_actuel, plis_actuel) #pour faire jouer une ia qui test tout 
            else:
                carte_ia = self.coup_possible_smart(joueur_actuel, plis_actuel)
                if carte_ia == None:
                    print("Erreur IA nous allons joueur un coup aleatoire")
                    carte = random.choices(self.liste_coup_possible(joueur_actuel, plis_actuel))
                else: carte = carte_ia[0]

            if not self.verif_coup(joueur_actuel, carte, plis_actuel):
                print("\n")
                self.afficher_mains()
                print("\n")
                print("Votre coup etais", carte)
                print("le plis etait", plis_actuel)
                print("Nous etions le joueur ", joueur_actuel)
                raise CoupImpossibleException()

            plis_actuel.append(carte)
            self.mains[joueur_actuel].remove(carte)
            self.gagnant_actuel = (plis_actuel.index(self.carte_gagnante(plis_actuel)) + self.qui_tour) % self.nb_joueurs
        
        self.actualiser_ancien_plis_couleur(plis_actuel)
        self.ancien_plis.append(plis_actuel)
        self.actualiser_pts()
        self.qui_tour = self.gagnant_actuel

    def actualiser_pts(self):
        dernier_plis = self.ancien_plis[-1]
        for carte in dernier_plis:
            i = self.gagnant_actuel 
            if carte[0] == "Atout":
                if carte[1] == 1 or carte[1] == 21:
                    self.pts[i] += 4.5
                    self.bouts[i] += 1
                else:
                    self.pts[i] += 0.5
            elif carte[0] == "Excuse":
                self.pts[i] += 4.5
                self.bouts[i] += 1
            elif carte[1] > 10:
                self.pts[i] += carte[1] - 9.5
            else:
                self.pts[i] += 0.5
        pass 
        
    def calcul_points(self, carte):
        if carte[0] != "Atout" and carte[1] > 10:
            return carte[1] - 9.5
        elif carte[0] == "Atout" and (carte[1] == 21 or carte[1] == 1):
            return 4.5
        elif carte[0] == "Excuse":
            return 4.5
        else :
            return 0.5
    
    def liste_atout_joueur(self, joueur):
        liste_atout = []
        for carte in self.mains[joueur]:
            if carte[0] == "Atout":
                liste_atout.append(carte[1])
        liste_atout.sort()
        return liste_atout
    
    def verif_coup(self, joueur, carte, plis_actuel):
        """verifie si le coup est possible"""
        if carte not in self.mains[joueur]:
            return False
        if plis_actuel == []:
            return True
        
        couleur = plis_actuel[0][0]
        if couleur == "Excuse":
            if len(plis_actuel) == 1:
                return True
            couleur = plis_actuel[1][0]
        
        if couleur == "Atout":
            if carte[0] == "Excuse":
                return True
            if carte[0] == "Atout":
                carte_gagnante = self.carte_gagnante(plis_actuel)
                if carte_gagnante[1] < carte[1]:#cas ou on joue un atout plus fort
                    return True
                else:
                    if self.liste_atout_joueur(joueur)[-1] > carte_gagnante[1]:
                        return False
                    else:
                        return True
            else:
                if self.possede_atout(joueur):
                    return False
                else:
                    return True
        else:
            if carte[0] == couleur:
                return True
            else:
                if self.possede_couleur(joueur, couleur):
                    return False
                if self.possede_atout(joueur) and carte[0] != "Atout":
                    return False
                return True


    #%% partie IA 
    
    def liste_coup_possible(self, joueur, plis_actuel):
        """renvoie la liste des coups possible"""
        liste_coup = []
        for carte in self.mains[joueur]:
            if self.verif_coup(joueur, carte, plis_actuel):
                liste_coup.append(carte)
        return liste_coup

    
    def coup_possible_smart(self, joueur, plis_actuel):
        """
        joue un coup "intelligent" en gerant les cas particuliers
        
        on va renvoyer une evalution de la carte jouée
        0 : meilleur coup possible
        1 : coup possible mais on peut perdre le plis
        2 : coup risqué
        3 : A ameliorer

        Args:
            joueur (int): joueur actuel
            plis_actuel (list): plis en cours

        Returns:
            tuple: (carte, evaluation) 
        """
        if plis_actuel == []:
            #premier coup
            return (self.defausse(joueur), 2)
        else:
            couleur = plis_actuel[0][0]
            if couleur == "Atout":
                if ("Atout", 1) in plis_actuel and ("Atout", 21) in plis_actuel:
                    return (self.atout_le_plus_bas(plis_actuel, joueur), 0)
                elif ("Atout", 1) in plis_actuel:
                    atout_fort = self.atout_le_plus_fort(plis_actuel, joueur)
                    if self.verif_plus_fort_atout(atout_fort, plis_actuel):
                        return (atout_fort, 1)
                    else:
                        return (self.atout_le_plus_bas(plis_actuel, joueur), 0)
                elif ("Atout", 21) in plis_actuel:
                    if self.preneur_a_la_main(joueur, plis_actuel):
                        return (self.atout_le_plus_bas(plis_actuel, joueur, petit=True), 0)#petit compris
                else:
                    return (self.atout_le_plus_bas(plis_actuel, joueur), 1)
            else:
                if self.possede_couleur(joueur, couleur):
                    carte_forte = self.carte_la_plus_haute(joueur, plis_actuel, couleur)
                    
                    #on possede la carte la plus forte jouable mais il peut y avoir plus fort dans les mains ou de l'atout
                    if carte_forte[1] == 14 and self.ancien_plis_couleur[couleur] == 0:
                        return (carte_forte, 0)
                    else:#cas a traiter absolument
                        if self.preneur_deja_jouer(joueur, plis_actuel):
                            if self.preneur_a_la_main(joueur, plis_actuel):
                                if self.carte_gagnante(plis_actuel)[1] > carte_forte[1]:
                                    #on joue le plus bas ce cas est bete si nos pote peuvent recup la main
                                    return (self.carte_la_plus_basse(joueur, plis_actuel, couleur), 1)
                                else:#on recup la main
                                    return (carte_forte, 0)
                            else:#on mets du point 
                                return (carte_forte, 0)
                        else:
                            return (self.carte_la_plus_basse(joueur, plis_actuel, couleur), 1)
                else:
                    return (self.atout_le_plus_bas(plis_actuel, joueur), 1)

    def signalisation(self, joueur, preneur):
        '''
        Renvoie une carte qui permet une signalisation FFT : si dame ou roi dans la main alors on joue à l'entame une carte de la meme couleur entre 1 et 5
        '''
        if (preneur != joueur):
            couleur = ["Trefle", "Carreau", "Coeur", "Pique"]
            for c in couleur:
                if ((13, c) in self.mains[joueur] or (14, c) in self.mains[joueur]):
                    for i in range(1, 6):
                        if ((i, c) in self.mains[joueur]):
                            return (i, c)
        return "Pas de signalisation"
    
    def carte_la_plus_basse(self, joueur, plis_actuel, couleur):
        """ renvoie la carte la plus basse jouable dans la couleur demandée"""
        min = 15
        carte_min = None
        for carte in self.mains[joueur]:
            if carte[0] == couleur and carte[1] < min:
                min = carte[1]
                carte_min = carte
        if carte_min == None:
            return self.defausse(joueur)
        return carte_min

    def carte_la_plus_haute(self, joueur, plis_actuel, couleur):
        """renvoie la carte la plus haute jouable dans la couleur demandée"""
        max = 0
        carte_max = None
        for carte in self.mains[joueur]:
            if carte[0] == couleur and carte[1] > max:
                max = carte[1]
                carte_max = carte
        if carte_max == None:
            return self.defausse(joueur)
        return carte_max
       
    def verif_plus_fort_atout(self, atout_fort, plis_actuel):
        """ verifie si on possede l'atout le plus fort jouable"""
        if atout_fort == ("Atout", 21):
            return True
        else:
            for carte in plis_actuel:
                if carte[0] == "Atout" and carte[1] > atout_fort[1]:
                    return False
            for plis in self.ancien_plis:
                for carte in plis:
                    if carte[0] == "Atout" and carte[1] > atout_fort[1]:
                        return False
            return True


    def preneur_deja_jouer(self, joueur, plis_actuel):
        """ verifie si le preneur a deja joué"""
        if plis_actuel == []:
            return False
        else:
            nb_cartes_jouer = len(plis_actuel)
            verif = ((self.preneur - nb_cartes_jouer) % self.nb_joueurs)
            if verif > joueur:
                return True
            return False
    
    def carte_gagnante(self, plis_actuel):
        carte_gagnante = plis_actuel[0]
        for carte in plis_actuel:
            if carte[0] == carte_gagnante[0] and carte[1] > carte_gagnante[1]:
                carte_gagnante = carte
            elif carte[0] == "Atout" and carte_gagnante[0] != "Atout":
                carte_gagnante = carte
        return carte_gagnante
    
    def preneur_a_la_main(self, joueur, plis_actuel):
        if plis_actuel == []:
            return False
        else:
            carte_gagnante = self.carte_gagnante(plis_actuel)
            index_carte_gagnante = plis_actuel.index(carte_gagnante)
            if index_carte_gagnante == ((self.preneur - len(plis_actuel)) % self.nb_joueurs):
                return True
            return False

    def atout_le_plus_bas(self, plis_actuel, joueur, petit=False):
        """renvoie l'atout le plus bas jouable"""
        if plis_actuel == []:#premier coup
            min = 22
            carte_min = None
            for carte in self.mains[joueur]:
                if carte[0] == "Atout" and carte[1] < min:
                    if carte[1] == 1 and petit == False:
                        continue
                    min = carte[1]
                    carte_min = carte
            if carte_min == None:
                if ("Atout", 1) in self.mains[joueur]:
                    return ("Atout", 1)
                return self.defausse(joueur)
            return carte_min
        else:
            couleur = plis_actuel[0][0]
            if couleur == "Atout":#si la couleur demandée est un atout
                if ("Excuse", 0) in self.mains[joueur]:#on priorise l'excuse
                    return ("Excuse", 0)
                min_jouable = plis_actuel[0][1]
                for carte_jouer in plis_actuel:
                    if carte_jouer[1] > min_jouable and carte_jouer[0] == "Atout":
                        min_jouable = carte_jouer[1]
                carte_min = None
                min = 22
                for carte in self.mains[joueur]:
                    if carte[0] == "Atout" and carte[1] < min and carte[1] > min_jouable:
                        min = carte[1]
                        carte_min = carte
                if carte_min != None:#si on a une carte plus forte que celle jouée on la joue
                    return carte_min
                else:#si on a pas de carte plus forte que celle jouée on joue la plus faible
                    min = 22
                    for carte in self.mains[joueur]:
                        if carte[0] == "Atout" and carte[1] < min:
                            if carte_min is not None and carte_min[1] == 1 and petit == False:
                                continue
                            min = carte[1]
                            carte_min = carte
                    if carte_min == None:
                        if ("Atout", 1) in self.mains[joueur]:
                            return ("Atout", 1)
                        return self.defausse(joueur)
                    return carte_min
                
            else:#si la couleur demandée n'est pas un atout
                if couleur in self.mains[joueur]:#si le joueur a la couleur demandée
                    min = 15
                    carte_min = None
                    for carte in self.mains[joueur]:
                        if carte[0] == couleur and carte[1] < min:
                            min = carte[1]
                            carte_min = carte
                    return carte_min
                else:#si le joueur n'a pas la couleur demandée on joue l'atout min
                    carte_min = None
                    min = 22
                    for carte in self.mains[joueur]:
                        if carte[0] == "Atout" and carte[1] < min:
                            if carte_min is not None and carte_min[1] == 1 and not petit:
                                continue
                            min = carte[1]
                            carte_min = carte
                    if carte_min != None:#si il nous reste des atouts on joue le plus petit
                        return carte_min
                    else:#on defausse ou petit
                        if ("Atout", 1) in self.mains[joueur]:
                            return ("Atout", 1)
                        return self.defausse(joueur)
                

    def defausse(self, joueur):
        """ 
        renvoie la carte la plus basse de la couleur la plus fréquente dans la main du joueur
        attention il peut defausser de l'atout si c'est la couleur la plus frequente
        """
        couleur_la_plus_frequente = self.couleur_la_plus_frequente(joueur)
        min = 100
        carte_min = None
        for carte in self.mains[joueur]:
            if carte[0] == couleur_la_plus_frequente and carte[1] < min and not (carte[0] == "Atout" and carte[1] == 1):
                min = carte[1]
                carte_min = carte
        if carte_min == None:
            if ("Atout", 1) in self.mains[joueur]:
                if self.mains[joueur] == [("Atout", 1)]:
                    return ("Atout", 1)
                else:
                    for carte in self.mains[joueur]:
                        if not (carte[0] == "Atout" and carte[1] == 1):
                            return carte
            
            print("erreur defausse, La mains du joueur etait", self.mains[joueur], "\nC'etait le joueur", joueur)
            raise ErrorDefausse()
        return carte_min

    def possede_couleur(self, joueur, couleur):
        """ verifie si le joueur possede la couleur demandée"""
        for carte in self.mains[joueur]:
            if carte[0] == couleur:
                return True
        return False
    
    def possede_atout(self, joueur):
        """ verifie si le joueur possede un atout"""
        for carte in self.mains[joueur]:
            if carte[0] == "Atout":
                return True
        return False

    def couleur_la_plus_frequente(self, joueur):
        """ renvoie la couleur la plus fréquente dans la main du joueur"""
        dico = {"Coeur":0, "Carreau":0, "Trefle":0, "Pique":0, "Atout":0, "Excuse":0}
        for carte in self.mains[joueur]:
            dico[carte[0]] += 1
        max = 0
        couleur_max = None
        for couleur in dico:
            if dico[couleur] > max:
                max = dico[couleur]
                couleur_max = couleur
        return couleur_max
    

    def verif_plus_fort_normal(self, carte_fort, plis_actuel, couleur):
        """ verifie si on possede la carte la plus forte jouable dans la couleur demander"""
        if carte_fort[1] == 14:
            return True
        else:
            for carte in plis_actuel:
                if carte[0] == couleur and carte[1] > carte_fort[1]:
                    return False
            for plis in self.ancien_plis:
                for carte in plis:
                    if carte[0] == couleur and carte[1] > carte_fort[1]:
                        return False
            return True


    def atout_le_plus_fort(self, plis_actuel, joueur):
        """ renvoie l'atout le plus fort jouable"""
        if self.possede_atout(joueur):
            max = 0
            carte_max = None
            for carte in self.mains[joueur]:
                if carte[0] == "Atout" and carte[1] > max:
                    max = carte[1]
                    carte_max = carte
            return carte_max
        else:
            return self.defausse(joueur)

    
    

# Utilisation du jeu de tarot





def partie():
    
    print("\n" * 100)
    print("\033[2J")
    print("Bienvenue dans le jeu de tarot")
    nb_joueurs = 4
    ls_points = [None for _ in range(nb_joueurs)]
    jeu = Jeu(nb_joueurs, 18)
    jeu.melanger_paquet()
    jeu.distribuer_cartes()
    jeu.trier_mains()
    jeu.afficher_mains()
    preneur = int(input("Preneur -> "))
    jeu.preneur = preneur

    only_ia = input("game uniquement ia ?(y/n) -> ")
    
    if only_ia == "y":
        jeu.joueur_physique = 10



    pts = [0 for _ in range(nb_joueurs)]
    bouts = [0 for _ in range(nb_joueurs)]
    tour = 0
    
    for i in range(18): #REMETTRE LE BON NOMBRE DE TOURS ~~~ 18
        
        sleep(0.25)
        print("\n" + "-" * LARGEUR_CONSOLE[0])
        #print("\033[2J")#clear console
        print("Manche : ", i)
        
        print("Ancien plis: ")
        for i in range(len(jeu.ancien_plis)):
            print(jeu.afficher_cartes(jeu.ancien_plis[i], "\tPlis " + str(i) + " : "))
        
        jeu.manche_rayan()
        tour = jeu.qui_tour
        pts = jeu.pts
        bouts = jeu.bouts
        
        
        print("Tour : ", tour)
        print("Bouts : ", bouts)
        print("Pts : ", pts)
    
    print("Attaque : ", pts[preneur])
    print("Défense : ", sum(x for x in pts) - pts[preneur])

    bouts_attaque = bouts[preneur]
    points_attaque = pts[preneur]
    if(bouts_attaque == 0 and points_attaque >= 56):
        print("Victoire preneur")
        return True
    elif(bouts_attaque == 1 and points_attaque >= 51):
        print("Victoire preneur")
        return True
    elif(bouts_attaque == 2 and points_attaque >= 41):
        print("Victoire preneur")
        return True
    elif(bouts_attaque == 3 and points_attaque >= 36):
        print("Victoire preneur")
        return True
    else:
        print("Défaite preneur")
        return False


try:
    LARGEUR_CONSOLE = [os.get_terminal_size().columns]
except:
    LARGEUR_CONSOLE = [100]

cpt = 0
for i in range(1):
    cpt += partie()
    print("\n")
    print("-" * LARGEUR_CONSOLE[0])
    print("\n")

print("Nombre de victoire : ", cpt)
