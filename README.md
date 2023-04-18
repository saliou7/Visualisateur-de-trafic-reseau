*******************************************************************
         |              Pour executer le programme                         |
         *******************************************************************          
	 - Il faut installer python ensuite executer le fichier exec.py suivi du fichier (*.txt) contenant les trames.
		commande : python exec.py <"nom du fichier contenant les trames">
         - Le resultat de la visualisation sera affiché sur le terminal et aussi dans un fichier nommé "flow_graph.txt"
         
	 - Un fihcier contenant des trames est fourni pour le tester utiliser la commande : 
		" python exec.py trames.txt "
         ******************************************************************
         |              Type de trame compatible avec le visualisateur    |
         ******************************************************************
         - Toutes types de trames est acceptées (Que ça soit les trames avec ascii ou sans ) mais ne sont analysées
                que celles ayant un type ipV4 et dont les protocoles sont (tcp , http), les autres sont ignorées.

         - Toute trame incomplete sera notifié d'un message indiquant la ligne du fichier incomplete sur le terminal et
                empêchera la visualisation des autres trames.
	 
	 - Pour tester plusieurs trames, il faut toutes les mettres dans un seul fichier, ne pas mettre
		d'espace entre les trames et ne pas mettre un saut de ligne pour la derniere trame, pour
		resumer il ne faut laisser aucune ligne vide.

	 *******************************************************************
         |              Deroulement du visualisateur                       |
         *******************************************************************
         - Dés que le programme est lancé un menu proposant plusieurs options s'affiche, choisissez donc l'option que
                vous voulez, vous pouvez choisir l'option QUITTER pour fermer le programme.
