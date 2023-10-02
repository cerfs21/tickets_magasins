## Conversion de fichiers de tickets csv en fichiers JSON
https://github.com/cerfs21/tickets_magasins

### Le processus de traitement proposé est le suivant :
1) Récupération de la liste des fichiers csv dans le répertoire relatif ./Data
2) En itérant sur les éléments de cette liste de fichiers :
   * lecture ligne à ligne de chaque fichier csv
   * conversion de chaque ligne en ticket-dictionnaire (fonction ad-hoc)
   * ajout de chaque ticket-dictionnaire obtenu, d'une part dans une liste contenant tous les tickets, d'autre part dans une liste contenant les tickets émis par un magasin donné 
3) Pour la liste contenant tous les tickets-dictionnaires :
   * conversion de la liste en document JSON
   * écriture du document JSON dans un 'fichier complet'
   * vérification de conformité au format JSON du fichier obtenu (fonction ad-hoc)
4) En itérant sur les éléments du dictionnaire des magasins :
   * conversion en document JSON de la liste des tickets-dictionnaires du magasin considéré
   * enregistrement du document JSON dans un fichier magasin selon la nomenclature fournie
   * vérification de conformité au format JSON du fichier magasin (fonction ad-hoc).

### Les principaux objets manipulés sont les suivants :
- __ticket_magasin__ : dictionnaire dont les clés reprennent l'ordre et la nomenclature attendus
   * magasin (id_magasin dans le fichier d'origine)
   * timestamp (date + heure dans le fichier d'origine)
   * client (id_client dans le fichier d'origine)
   * id_ticket (idem fichier d'origine)
   * articles
- __articles__ : liste de dictionnaires dont chacun est un (objet) 'article' acheté
- __article__ (acheté) : dictionnaire dont les clés reprennent l'ordre et la nomenclature attendus
   * produit
   * catégorie
   * prix_u (prix unitaire)
   * qte (quantité)
- __dict_magasins__ (parcouru à l'étape 4 ci-dessus) : dictionnaire des magasins avec key = id_magasin et value = liste de tickets d'un magasin
- __ticket2dict__ : fonction de conversion d'un ticket (fourni en argument) tiré d'un fichier csv en dictionnaire 'ticket_magasin'
- __verification_json__ : fonction de vérification de conformité au format JSON d'un fichier (fourni en argument).

### Le traitement ci-dessus donne lieu aux contrôles suivants :
1) décompte du nombre de lignes dans chaque fichier csv (lignes vides incluses)
2) décompte du nombre de tickets valides traités dans chaque fichier csv
3) détection de lignes vides dans les fichiers sources
4) détection d'emplacements vides dans la zone article d'un ticket csv (sur une ligne non vide d'un fichier source)
5) vérification de conformité au format JSON (voir plus haut)
6) pas de détection des doublons : les tickets sont convertis et copiés sans contrôle sur les valeurs (hors exclusion des chaînes vides).

### Résultats obtenus
Les livrables sont conformes à l'attendu :
- 1 fichier JSON contenant l'ensemble des tickets valides tirés des fichiers csv fournis
- 11 fichiers JSON contenant chacun les tickets émis par un seul magasin
- La nomenclature fournie en exemple est respectée
- La vérification de conformité au format JSON est concluante pour les 12 fichiers produits (cf. fonction verification_json)

Le script affiche sur la sortie standard le décompte de lignes et de tickets pour chaque fichier csv, ainsi que le résultat de la vérification de conformité JSON pour les 12 fichiers résultats.

On note la présence de lignes vides dans tous les fichiers, qui se traduit par un nombre de tickets inférieur au nombre de lignes du fichier csv d'origine : cf. contrôle 3.

Le contrôle 4 a été mis en place suite à la découverte de champs vides pour certaines lignes des fichiers fournis. 

Le temps d'exécution constaté pour la totalité du script est inférieur à 2s.