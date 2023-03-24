from utils import *
from visualiseur import *
from filtre import *
import sys

print(affiche_entete())
def visualise(file : str) :
    trames = read_file(file)
    trame_http, trame_sans_http, liste_ip = filtre_general(trames)
    while(True) : 
        print("\n")
        choix  = demande(liste_ip_port(trame_http), liste_ip_port(trame_sans_http), liste_ip) # choix du l'utisateur

        info = ""
        tab = []
        fichier = open("flow_graph.txt", "a")

        if(choix == '0') : 
            return 0
        if choix == 'q' :
            effacer()
            print(affiche_entete())

        tmp_trames = []
        if choix == '2' or choix == '3 2' or choix == '4 2': 
            addr_ip = input("Entrez l'adresse IP : ")
            port = input("Entrez le port : ")
            if choix == '2' :
                tmp_trames = filtre(addr_ip, port, trames)
            elif choix == '3 2' :
                tmp_trames = filtre(addr_ip, port, trame_http)
            else: tmp_trames = filtre(addr_ip, port, trame_sans_http)

            if(len(tmp_trames) != 0) : 
                info, tab = visualiseur(tmp_trames[0],1)
                if info != False and len(tab) != 0: 
                    print("\n{}                                                                                             {}\n".format(tab[0],tab[1]))
                    fichier.write("\n{}                                                                                            {}\n".format(tab[0],tab[1]))
        elif choix == '1' or choix == '3 1' or choix == '4 1':
            if choix == '1' :
                lister_toutes_les_ip(trames, fichier)
            elif choix == '3 1':
                lister_toutes_les_ip(trame_http, fichier)
            else: lister_toutes_les_ip(trame_sans_http, fichier)

        for ind, trame in enumerate(tmp_trames,1):
        
            info, tmp = visualiseur(trame,ind)
            
            if (info == False or len(tmp) == 0 or len(tab) == 0 ) and (choix == '2' or choix == '3 2' or choix == '4 2'):
                continue
            if info == False or len(tmp) == 0 :
                continue
            print("            {}".format(info))
            fichier.write("            {}\n".format(info))
            if (choix == '2' or choix == '3 2' or choix == '4 2') and (tmp[0] == tab[0]) :
                
                print("  {}\t|------------------------------------------------------------------------------------------------------>|{}\n".format(tab[2],tab[3]))
                fichier.write("  {}\t|------------------------------------------------------------------------------------------------------->|{}\n\n".format(tab[2],tab[3]))
            elif choix == '2' or choix == '3 2' or choix == '4 2':
                print("  {}\t|<------------------------------------------------------------------------------------------------------|{}\n".format(tab[2],tab[3]))
                fichier.write("  {}\t|<-------------------------------------------------------------------------------------------------------|{}\n\n".format(tab[2],tab[3]))
            else :
                print("  {}\t|------------------------------------------------------------------------------------------------------>|{}\n".format(tmp[2],tmp[3]))
                fichier.write("  {}\t|------------------------------------------------------------------------------------------------------>|{}\n\n".format(tmp[2],tmp[3]))
        fichier.close()

visualise("./"+sys.argv[1])

