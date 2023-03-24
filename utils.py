import os
#lire les trames sur un fichier 
def read_file(file: str):
    with open(file) as f:
        tmp = [line.split(' ') for line in f.read().splitlines()]
    nb_octet_prec = 0 #compte le nombre d'octet de la ligne precedente
    nb = 0
    for l ,line in enumerate(tmp) :
        nb = 0 
        for ind, i in enumerate(line) :
            if i == '':
                nb += 1
            if nb >= 3 :
                tmp[l] = tmp[l][:ind]
                break
        tmp[l].remove('')
        tmp[l].remove('')
    trames = [[]] 
    offset_prec ="0000"  #contient l'offset de la ligne precedente
    trame = 0
    for ind_line, line in enumerate(tmp, 1):
        #line[0] -> offset de la ligne courante codé sur 4 chiffres hexa
        if(len(line[0]) != 4):
            print("Erreur de Syntaxe: offset incorrect sur la ligne :",ind_line)
            return []

        if int(line[0], base = 16) != nb_octet_prec + int(offset_prec, base = 16) :
            if int(line[0],16) == 0 and offset_prec != "0000" :
                trame += 1
                trames.append([])
            else:
                print("\tTrame incomplete, erreur sur la ligne :",ind_line-1)
                return []
        offset_prec = line[0]
        nb_octet_prec = len(line)-1 #nombre d'octet sans l'offset
        trames[trame].append(line[1:])
    trames = [sum(trame, []) for trame in trames] # trames contient chaque trame dans une liste
    return trames

def hex_to_bin(hex: str, nb_bit = 4):
    return bin(int(hex, 16))[2:].zfill(nb_bit)

def hex_to_dec(hex: str):
    hex = ''.join(hex)
    return int(hex, base = 16)

def effacer() :
    os.system("cls")
    os.system("clear")

def affiche_entete() :
    return  " 			    *-------------------------------------------------------------------------------------*\n"\
		    "  		            |		V I S U A L I S A T E U R 	D E    T R A F I C    R E S E A U         |\n"\
			"		            *_____________________________________________________________________________________*\n\n"

def affiche(liste) : 
    print ("    *-------------------------------------------------*\n"\
           "    |    Liste de tous les ports et IP des trames     | \n"\
           "    *_________________________________________________*")
    for (ip, port) in liste : 
        print("    *-------------------------------*\n"\
              "    |{}\t :  {}".format(ip,port))
    print("    *-------------------------------*")


def demande(liste_ip_http, liste_ip_sans_http, liste) : 
    while(True):
        print("************************* M E N U **************************")
        print("*     - Afficher toutes les trames sans filtre.   (Entrez 1)")
        print("*     - Filtrer une adresse IP.                   (Entrez 2)")
        print("*     - Filtrer que les requetes http.            (Entrez 3)")
        print("*     - Filtrer que les trames tcp (sans http).   (Entrez 4)")
        print("*     - Afficher la liste des IP et leurs ports.  (Entrez 5)")
        print("*     - Effacer l'ecran du terminal               (entrez q)")
        print("*     - QUITTER                                   (Entrez 0)")
        choix = input("Choix : ")
        print("\n")
        if choix == '5' : 
            affiche(liste)
        if choix == '1' or choix == '2' or choix == '0' or choix == 'q': 
            return choix
        elif  choix == '3' :
            return demande_http(liste_ip_http)
        elif choix == '4':
            return demande_tcp(liste_ip_sans_http)
def demande_http(list_ip) :
    while(True) : 
        print("*************************** Votre choix ? :***************************")
        print("|   - Afficher toutes les trames http.               (Entrez 3 1)    |")
        print("|   - Filtrer une adresse IP parmi les trames http.  (Entrez 3 2)    |")
        print("|   - Afficher la liste des IP et leurs ports.       (Entrez  1 )    |")
        print("|   - Effacer l'ecran du terminal                    (entrez  q )    |")
        print("|   - RETOUR AU MENU                                 (Entrez  r )    |")
        choix = input("Choix : ")
        print("\n")
        if choix == '3 1' or choix == '3 2' or choix == 'r' : 
            return choix
        if choix == '1' : 
            affiche(list_ip)
        if choix == 'q':
            effacer()
            print(affiche_entete())

def demande_tcp(list_ip) :
    while(True) : 
        print("************************** Votre choix ? :***********************************")
        print("*   - Afficher toutes les trames tcp sans http.               (Entrez 4 1)  *")
        print("*   - Filtrer une adresse IP parmi les trames tcp sans http.  (Entrez 4 2)  *")
        print("*   - Afficher la liste des IP et leurs ports.                (Entrez  1 )  *")
        print("*   - Effacer l'ecran du terminal                             (entrez  q )  *")   
        print("*   - RETOUR AU MENU                                          (Entrez  r )  *")
        choix = input("Choix : ")
        print("\n")
        if choix == '4 1' or choix == '4 2' or choix == 'r': 
            return choix
        if choix == '1' : 
            affiche(list_ip)
        if choix == 'q':
            effacer()
            print(affiche_entete())