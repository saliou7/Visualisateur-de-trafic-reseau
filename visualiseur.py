from utils import *

Type_TCP_option = {"00":1, "01":1, "02":4, "03":3, "04":2, "08":10, "05":10}


def visualiseur(trame , numero) :
    taille_trame = len(trame)
    if taille_trame < 54 : #ip = 20 min, tcp = 20 min, ethernet = 20 + 4 min
        print("     Impossible d'analyser la trame \n"+str(numero))
        return False

    type = ''.join(trame[12:14])
    if type != '0800' : 
        print("     Le type de la trame "+str(numero)+" n'est en pas IPv4\n")
        return False, []

    #verification du protocole
    protocole = trame[23]
    if protocole != "06" : 
        print("     Protocole non accepté pour la trame "+str(numero)+"\n")
        return False, []
    
    #ip source 
    ip_src = trame[26:30]
    ip_src = '.'.join([str(hex_to_dec(octet)) for octet in ip_src])

    #ip destination
    ip_dest = trame[30:34]
    ip_dest = '.'.join([str(hex_to_dec(octet)) for octet in ip_dest])

    #taille entete ip
    ip_len = hex_to_dec(trame[16:18])

    #taille entête ip
    ip_entete = hex_to_dec(trame[14][1])*4

    l = ip_entete - 20 #taille des options
    #----------------#----------------Partie TCP#---------------------------------#
    #port source et destination 
    src_port = hex_to_dec(trame[l+34:l+36])
    dest_port = hex_to_dec(trame[l+36:l+38])

    #Sequence Number and Acknowledgment Number
    syn = hex_to_dec(trame[l+38:l+42])
    ack = hex_to_dec(trame[l+42:l+46])
    
    ##csyn, ack = calc_ack_syn((ip_src,ip_dest),syn,ack)
    #entete tcp
    tcp_entete = hex_to_dec(trame[l+46][0])*4

    #determiner les flag
    flag = []
    dic_tmp = {2:'URG', 3:'ACK', 4:'PSH', 5:'RST', 6:'SYN', 7:'FIN'}
    tmp = hex_to_bin(trame[l+47], 8)
    for i in range(2,8) : #ignorer les deux bits de reserved 
        if tmp[i] == '1' :
            flag.append(dic_tmp[i])


    #calcul du window 
    window = hex_to_dec(trame[l+48:l+50])

    #option du tcp
    tcp_option = tcp_entete - 20
    
    length = len(trame[l+tcp_option+54:])
    if tcp_option > 0 :   
        if len(trame[l+tcp_option+54:]) > 0 : 
            if trame[l+tcp_option+54] == '47' or trame[l+tcp_option+54] == '48' :
                return analyse_http(trame[l+tcp_option+54:]), [ip_src, ip_dest, src_port, dest_port]
        if l > 0 :
            l = l + 1
            tcp_option += 1
        tab_option = analyse_option_tcp(trame[l+54:l+tcp_option+54], tcp_option)
        if ack != 0 :
            return  "{} -> {} [{}] Seq={} Ack={} Win={} Len={} {}".format(src_port,dest_port,", ".join(flag[::-1]),syn,ack, window,length," ".join(tab_option)), [ip_src, ip_dest, src_port, dest_port]
        return  "{} -> {} [{}] Seq={} Win={} Len={} {}".format(src_port,dest_port,", ".join(flag[::-1]),syn, window, length," ".join(tab_option)), [ip_src, ip_dest, src_port, dest_port]
    
    if len(trame[l+tcp_option+54:]) > 0 : 
        if trame[l+tcp_option+54] == '47' or trame[l+tcp_option+54] == '48' :
            return analyse_http(trame[l+tcp_option+54:]), [ip_src, ip_dest, src_port, dest_port]
    
    if ack != 0 : 
        return  "{} -> {} [{}] Seq={} Ack={} Win={} Len={}".format(src_port,dest_port,", ".join(flag[::-1]),syn,ack, window, length), [ip_src, ip_dest, src_port, dest_port]
    return  "{} -> {} [{}] Seq={} Win={} Len={}".format(src_port,dest_port,", ".join(flag[::-1]),syn, window, length), [ip_src, ip_dest, src_port, dest_port]


def analyse_option_tcp(octets_options, taille) :
    i = 0
    options = []
    while i < taille-1 : 
        type = octets_options[i] 

        if type == '02':
            tmp = "MSS="+str(hex_to_dec(octets_options[i+2:i+4]))
            options.append(tmp)

        if type == '03':
            val = octets_options[i+Type_TCP_option[type]-1]
            val = pow(2,hex_to_dec(val))
            tmp = "WS="+str(val)
            options.append(tmp)
        
        if type == '04':
            options.append("SACK_PERM")
        i += Type_TCP_option[type]
    return options

def analyse_http(trame) : 
    tmp = []
    for i in trame : 
        if i == '0d' : 
            return bytes.fromhex(''.join(tmp)).decode('utf-8')
        tmp.append(i)
