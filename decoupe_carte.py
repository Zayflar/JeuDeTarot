import cv2
import os

# Charger l'image du jeu de tarot
image = cv2.imread("jeu_de_tarot_complet.png")

# Dimensions de l'image complète et des cartes
largeur_image, hauteur_image = image.shape[1], image.shape[0]
largeur_carte, hauteur_carte = 42, 77

# Créer le dossier de destination
dossier_destination = "cartes_decoupees"
if not os.path.exists(dossier_destination):
    os.makedirs(dossier_destination)

# Définir l'ordre des symboles de carte
ordre_symboles = ["Atout"] * 21 + ["Excuse"] + ["Pique", "Coeur", "Carreau", "Trèfle"]

# Découper les cartes une par une et les enregistrer
cartes = []
for symbole in ordre_symboles:
    for i in range(14):
        x = (i % 14) * largeur_carte
        y = (ordre_symboles.index(symbole) * 14 + i) // 14 * hauteur_carte
        carte = image[y:y+hauteur_carte, x:x+largeur_carte]
        cartes.append(carte)

# Enregistrer les cartes dans le dossier de destination
for i, carte in enumerate(cartes):
    nom_symbole = ordre_symboles[i // 14]
    if nom_symbole == "Atout":
        nom_fichier = os.path.join(dossier_destination, "trefle{}.png".format(i % 14 + 1 ))
    else:
        nom_fichier = os.path.join(dossier_destination, "{}{}.png".format(nom_symbole.lower(), i % 14 + 1))
    cv2.imwrite(nom_fichier, carte)

# Afficher les chemins des cartes enregistrées
for i, symbole in enumerate(ordre_symboles):
    for j in range(14):
        nom_symbole = symbole.lower() if symbole != "Atout" else "atout"
        chemin_carte = os.path.join(dossier_destination, "{}{}.png".format(nom_symbole, j+1))
        #print("Carte {}{} enregistrée sous : {}".format(nom_symbole, j+1, chemin_carte))
