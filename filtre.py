from utils import *
from visualiseur import *

def filtre_general(trames) : 
    trame_http = []
    trame_sans_http = []
    list_ip = []
    for trame in trames :
        #-----liste des trames ----#
        ip_src, port_src, ip_dest, port_dest = ip_machines_et_ports(trame)
        if (ip_src, port_src) not in list_ip:
            list_ip.append((ip_src,port_src))
        if (ip_dest, port_dest) not in list_ip:
            list_ip.append((ip_dest,port_dest))
        #-------------------------------------    
        res, val = isHttp(trame) 
        if res == 0 and val == 0 : 
            continue
        elif val == 1 :
            trame_sans_http.append(trame)
        else :
            trame_http.append(trame)
    return trame_http, trame_sans_http, list_ip
            

def isHttp(trame) : 
    taille = len(trame)
    if taille < 54 : 
        return (0,0)
    type = ''.join(trame[12:14])
    if type != '0800' :
        return (0,0)
    ip_entete = hex_to_dec(trame[14][1])*4
    l = ip_entete - 20 #taille des options
    tcp_entete = hex_to_dec(trame[l+46][0])*4
    tcp_option = tcp_entete - 20
    if len(trame[l+tcp_option+54:]) <= 0 :
        return (0, 1)
    if taille < 64 :
        return (0,0)
    if trame[l+tcp_option+54] == '47' or trame[l+tcp_option+54] == '48' :
        return 1,0
    return (0,0)

def ip_machines_et_ports(trame) : 

    if len(trame)  < 40 : 
        return ('0.0.0.0',0,'0.0.0.0',0)
    
    type = ''.join(trame[12:14])
    if type != '0800' : 
        return ('0.0.0.0',0,'0.0.0.0',0)

    #verification du protocole
    protocole = trame[23]
    if protocole != "06" : 
        return ('0.0.0.0',0,'0.0.0.0',0)

    #ip source 
    ip_src = trame[26:30]
    ip_src = '.'.join([str(hex_to_dec(octet)) for octet in ip_src])

    #ip destination
    ip_dest = trame[30:34]
    ip_dest = '.'.join([str(hex_to_dec(octet)) for octet in ip_dest])

    #taille entête ip
    ip_entete = hex_to_dec(trame[14][1])*4

    l = ip_entete - 20 #taille des options

    #port source et destination 
    src_port = hex_to_dec(trame[l+34:l+36])
    dest_port = hex_to_dec(trame[l+36:l+38])
    return (ip_src, src_port, ip_dest, dest_port)

def liste_ip_port(trames) :
    list_ip = []
    for trame in trames : 
        ip_src, port_src, ip_dest, port_dest = ip_machines_et_ports(trame)
        if (ip_src, port_src) not in list_ip:
            list_ip.append((ip_src,port_src))
        if (ip_dest, port_dest) not in list_ip:
            list_ip.append((ip_dest,port_dest))
    return list_ip

def filtre(ip:str, port:str, trames) : 
    filtre = list()
    for trame in trames : 
        ip_s, port_s, ip_d, port_d = ip_machines_et_ports(trame)
        if ip_s == ip and str(port_s) == port or ip_d == ip and str(port_d) == port : 
            filtre.append(trame)
    if len(filtre) == 0 : 
        print("Oups ! saisie incorrect")
    return filtre

def lister_toutes_les_ip(trames, fichier) : 
    
    liste = liste_ip_port(trames)
    tmp_l =[]
    debut = True
    ajout = True
    for addr,port in liste :
        if (addr, port) in tmp_l : 
            continue 
        debut = True
        tmp_l.append((addr, port))
        
        for ind, trame in enumerate(trames, 1) : 
            ip_s, s_p, ip_d, d_p = ip_machines_et_ports(trame)
            if (ip_s == addr and s_p == port) or (ip_d == addr and d_p == port) :
                if debut : 
                    info, tab = visualiseur(trame,ind) 
                    tmp_l.append((ip_s, s_p))
                    tmp_l.append((ip_d, d_p))
                info, tmp = visualiseur(trame, ind)
                
                if debut and info != False and len(tab) != 0:
                    debut = False 
                    print("\n{}                                                                                             {}\n".format(tab[0],tab[1]))
                    fichier.write("\n{}                                                                                            {}\n".format(tab[0],tab[1]))
                if info != False and len(tab) != 0:    
                    print("            {}".format(info))
                    fichier.write("            {}\n".format(info))
                    if (tmp[0] == tab[0]) :
                        print("  {}\t|------------------------------------------------------------------------------------------------------>|{}\n".format(tab[2],tab[3]))
                        fichier.write("  {}\t|------------------------------------------------------------------------------------------------------->|{}\n\n".format(tab[2],tab[3]))
                    else :
                        print("  {}\t|<------------------------------------------------------------------------------------------------------|{}\n".format(tab[2],tab[3]))
                        fichier.write("  {}\t<--------------------------------------------------------------------------------------------------------|{}\n\n".format(tab[2],tab[3]))
        print("\n")
