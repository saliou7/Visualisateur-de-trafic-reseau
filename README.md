# Visualisateur de trafic réseau
## Présentation
ce programme est un visualisateur des flux de trafic réseau. 
Un flux de trafic fait référence aux trames échangées dans le cadre d’un protocole 
exécuté à l’initiative de deux machines, chacune identifiée par une adresse MAC, 
une adresse IP et éventuellement par un numéro de port. 

## Instructions à suivre
### En entrée : 

Le programme prend en entrée un fichier trace (format texte) contenant les octets 'bruts', tels que capturés sur le réseau. Le fichier peut contenir plusieurs trames Ethernet ordonnées par ordre chronologique (sans préambule ni champ FCS). Voici les spécifications de format du fichier:

* Chaque octet est codé par deux chiffres hexadécimaux.
* Chaque octet est délimité par un espace.
* Chaque ligne commence par l'offset du premier octet situé à la suite sur la même ligne. L'offset décrit la position de cet octet dans la trace.
* Chaque nouvelle trame commence avec un offset de 0 et l'offset est séparé de trois espaces des octets capturés situés à la suite.
* L'offset est codé sur quatre chiffres hexadécimaux.
* Les caractères hexadécimaux peuvent être des majuscules ou minuscules.

###En sortie : 
le programme affiche les trames par ordre chronologique et indique pour chaque trame : 
* l'adresse IP des deux machines impliquées. 
* le numéro de port utilisé
* les informations pertinentes concernant le protocole de la couche la plus haute encapsulée. 
Le programme offre également un ensemble de filtres pour visualiser un des flots réseaux en sélectionnant les adresses IP des machines à l'origine d'un flot et/ou d'un protocole en particulier. Le résultat du visualisateur est affiché sur le terminal et également sauvegardé dans un fichier texte pour faciliter sa lecture.
	
### Autres informations

**Les protocoles pris en charge sont : **
* Ethernet
* IPv4
* TCP
* HTTP.

Pour executer le programme, il faut déja avoir installé python 
``` 
commande : python exec.py <"nom du fichier contenant les trames">
```
- Pour tester plusieurs trames, il faut toutes les mettres dans un seul fichier, ne pas mettre d'espace entre les trames et ne pas mettre un saut de ligne pour la derniere trame.
