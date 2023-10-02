# tickets_magasins v1.4

import os
import glob
import json
from datetime import datetime


# convertit une ligne de fichier csv en dictionnaire
def ticket2dict(ligne_fichier):

    # les champs d'une ligne d'un fichier Data sont délimités par un point virgule
    ticket = ligne_fichier.split(";")

    # vérifie que la ligne ne commence pas par une chaîne vide
    if len(ticket[0]) != 0:

        # les méta-informations d'un ticket sont contenues dans ses 5 premiers champs
        ticket_dict = {
                        "magasin": ticket[1],
                        # les champs date et heure sont regroupés comme attendu
                        "timestamp": ticket[0] + " " + ticket[3],
                        "client": ticket[4],
                        "id ticket": ticket[2],
                       }

        # initialise la liste des articles du ticket ainsi que l'index i pointant sur un élément d'un article
        articles = []
        i = 5
        # parcourt les articles jusqu'à épuisement du ticket
        while i < len(ticket):
            # vérifie qu'une zone article ne commence pas par une chaîne vide
            if ticket[i] != "":
                # chaque article acheté est détaillé en 4 champs
                article = {
                        "produit": ticket[i],
                        "categorie": ticket[i + 1],
                        "prix_u": ticket[i + 2],
                        "qte": ticket[i + 3]
                        }
                articles.append(article)
            # incrémente l'index de 4 champs jusqu'au prochain article
            i += 4

        # ajoute la liste des articles au dictionnaire qui contient déjà les méta-informations du ticket
        ticket_dict["articles"] = articles

        return ticket_dict
    else:
        return "ticket vide"


# vérifie la conformité d'un fichier au format JSON
def verification_json(nom_fichier):
    with open(nom_fichier, "r") as fichier_json:
        try:
            verification = json.load(fichier_json)
        except json.JSONDecodeError:
            print("Fichier", nom_fichier, ": erreur de format JSON.")
        else:
            print("Fichier", nom_fichier, ": format JSON respecté.")
    return


# *** Initialisation de certains objets ***

# établit la liste des fichiers sources en scrutant le chemin relatif ./Data
chemin_fichiers_csv = os.getcwd() + "/Data/"
liste_fichiers_csv = []
for chemin in os.scandir(chemin_fichiers_csv):
    if chemin.is_file():
        liste_fichiers_csv.append(chemin)

# initialise la liste qui contiendra tous les tickets (de type dictionnaire)
liste_complete = []

# initialise le dictionnaire des magasins avec key = id_magasin et value = liste de tickets d'un magasin
dict_magasins = {}


# *** Lecteurs des fichiers csv, conversion des tickets en dictionnaires et enregistrement dans des listes ***

# parcourt la liste des fichiers csv pour en extraire et traiter les tickets
for fichier in liste_fichiers_csv:
    print("Traitement du fichier", fichier.name)

    # initialisation des compteurs de lignes et de tickets pour le suivi du traitement
    nombre_lignes = 0
    nombre_tickets = 0

    # ouverture en lecture d'un fichier csv
    with open(fichier, 'r') as source:
        # readline renvoie False lorsqu'il rencontre la fin du fichier
        while ligne := source.readline():
            nombre_lignes += 1

            # vérifie que la ligne du fichier n'est pas vide
            if ligne != "\n":

                # appelle la fonction de conversion d'un ticket en dictionnaire
                ticket_magasin = ticket2dict(ligne)

                if ticket_magasin != "ticket vide":
                    # récupération de l'identifiant magasin qui identifiera une liste de tickets
                    magasin = ticket_magasin["magasin"]
                    # initialisation de la liste de tickets pour un nouveau magasin
                    if magasin not in dict_magasins.keys():
                        dict_magasins[magasin] = []
                    # ajout du ticket (de type dictionnaire) dans la liste du magasin approprié
                    dict_magasins[magasin].append(ticket_magasin)
                    # ajout du ticket dans la liste contenant tous les tickets
                    liste_complete.append(ticket_magasin)
                    nombre_tickets += 1

    print(nombre_lignes, "lignes dans ce fichier")
    print(nombre_tickets, "tickets valides dans ce fichier")
    print()


# *** Écriture des (listes de) dictionnaires dans des fichiers JSON et vérification de conformité au format JSON ***

# Suppression des fichiers JSON qui resteraient de traitements précédents
[os.remove(fichier) for fichier in glob.glob("*.json")]

# Écriture du fichier JSON contenant tous les tickets
with open("fichier_complet.json", "w") as fichier_complet:
    # json.dumps convertit la liste de dictionnaires en document json
    fichier_complet.write(json.dumps(liste_complete, indent=4))
verification_json("fichier_complet.json")

# Écriture des fichiers JSON contenant les tickets émis par chaque magasin
for magasin in dict_magasins:
    nom_fichier_magasin = str(magasin) + "_" + datetime.today().strftime('%Y%m%d%H%M%S') + ".json"
    with open(nom_fichier_magasin, "w") as fichier_magasin:
        # json.dumps convertit la liste de dictionnaires en document json
        fichier_magasin.write(json.dumps(dict_magasins[magasin], indent=4))
    verification_json(nom_fichier_magasin)
