import copy
import random

def simulation_coup(Jeu ,joueur:int, plis_actuel:list[tuple[str, int]]):
    """
    Fonction qui simule tous les coups possibles et retourne le meilleur coup possible en comparant 
    le nombre de pts gagné par le preneur et les defenseurs
    elle renverra le coups qui rapportent le plus de pts ou en font perdre le moins 

    Args:
        Jeu (Jeu): la classe jeu
        joueur (int): _description_
        plis_actuel (list[tuple[str, int]]): _description_

    Returns:
        tuple[str, int]: Le coup juger le plus otpimal
    """
    dico_bon_coup:dict[int, tuple[str, int]] = {}
    pts_depart = Jeu.pts
    for carte_test in Jeu.liste_coup_possible(joueur, plis_actuel):#on test tout les coups possible
        Jeu_copier = copy.deepcopy(Jeu)#on copie le jeu pour ne pas le modifier
        plis_actuel_copier = plis_actuel.copy()#ide pour ne pas modifier le plis actuel
        Jeu_copier.mains[joueur].remove(carte_test)#on enleve la carte de la main du joueur
        plis_actuel_copier.append(carte_test)#on ajoute la carte au plis actuel
        Jeu_copier.gagnant_actuel = (plis_actuel_copier.index(Jeu_copier.carte_gagnante(plis_actuel_copier)) + Jeu_copier.qui_tour) % Jeu_copier.nb_joueurs

        while len(plis_actuel_copier) != (Jeu_copier.nb_joueurs - 1):#on va jouer les autres coups pour terminer le plis 
            joueur_actuelle = (Jeu_copier.qui_tour + len(plis_actuel_copier)) % Jeu_copier.nb_joueurs
            carte_ia = Jeu_copier.coup_possible_smart(joueur_actuelle, plis_actuel_copier)
            if carte_ia == None:#cas qui arrive rarement mais qui peut arriver
                print("Erreur IA nous allons joueur un coup random")#nous allons jouer un coup random possible
                carte = random.choices(Jeu_copier.liste_coup_possible(joueur_actuelle, plis_actuel_copier))
            else: carte = carte_ia[0]

            plis_actuel_copier.append(carte)
            Jeu_copier.mains[joueur_actuelle].remove(carte)
            Jeu_copier.gagnant_actuel = (plis_actuel_copier.index(Jeu_copier.carte_gagnante(plis_actuel_copier)) + Jeu_copier.qui_tour) % Jeu_copier.nb_joueurs
        
        #on a fini le plis
        Jeu_copier.ancien_plis.append(plis_actuel_copier)
        Jeu_copier.actualiser_pts()
        pts_preneur = 0
        pts_defenseur = 0
        for j in range(len(Jeu_copier.pts)):#on calcule les pts gagnés par le preneur et les defenseurs
            if j == Jeu_copier.preneur:
                pts_preneur += (Jeu_copier.pts[j] - pts_depart[j])
            else:
                pts_defenseur += (Jeu_copier.pts[j] - pts_depart[j])
        #on rajoute le coup au dico avec les pts gagné en positif si on gagne et negatif si on perds 
        if pts_preneur > pts_defenseur:
            if joueur == Jeu_copier.preneur:
                dico_bon_coup[pts_preneur] = carte_test
            else:
                dico_bon_coup[-1 * pts_preneur] = carte_test
        else:
            if joueur == Jeu_copier.preneur:
                dico_bon_coup[-1 * pts_defenseur] = carte_test
            else:
                dico_bon_coup[pts_defenseur] = carte_test
    
    for cle in dico_bon_coup.keys():#on renvoie le coups maximal du dico
        if cle == max(dico_bon_coup.keys()):
            return dico_bon_coup[cle]
        
        
