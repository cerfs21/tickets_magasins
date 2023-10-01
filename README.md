## Conversion de fichiers de tickets au format csv en fichiers JSON

La méthode proposée consiste à traiter les fichiers de tickets selon le processus suivant :
1) Récupération de la liste de fichiers dans le répertoire relatif ./Data
2) En itérant sur les éléments de la liste de fichiers :
   * lecture ligne à ligne de chaque fichier Data au format csv
   * analyse de chaque ligne du fichier et conversion en ticket-dictionnaire (fonction ad-hoc)
   * ajout de chaque ticket-dictionnaire obtenu, d'une part dans une liste qui contiendra tous les tickets, d'autre part dans une liste contenant les tickets émis par un magasin donné 
3) Pour la liste contenant tous les tickets-dictionnaires :
   * conversion de la liste en document JSON
   * enregistrement du document JSON dans un 'fichier complet'
   * vérification de conformité du fichier complet au format JSON
4) En itérant sur le dictionnaire des magasins :
   + conversion en document JSON de la liste des tickets-dictionnaires pour un magasin donné
   + enregistrement du document JSON dans un fichier magasin suivant la nomenclature fournie
   + vérification de conformité d'un fichier magasin au format JSON.

Les principaux objets manipulés sont les suivants :
    Ticket : dictionnaire dont les clés sont les suivantes 
        date
        id_magasin
        id_ticket
        heure
        id_client
        liste (de taille variable) d'articles (chaque article est une ligne du ticket physique)
    Ligne d'un ticket : dictionnaire
        produit
        catégorie
        prix unitaire
        quantité

Contrôles intégrés :
- détection de lignes vides dans les fichiers sources
- détection d'emplacements vides (sur une ligne non vide d'un fichier source)
- compteurs de lignes et tickets traités (delta entre compteurs = nombre de lignes vides)
- vérification de conformité au format JSON
- pas de détection des doublons : les tickets sont convertis et copiés sans contrôle sur les valeurs (hors exclusion des chaînes vides)
