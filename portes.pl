﻿/*---------------------------------------------------------------*/
/* Telecom Paristech - J-L. Dessalles 2012                       */
/*            http://teaching.dessalles.fr                       */
/*---------------------------------------------------------------*/

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%  Deliberative reasoning & Argumentation %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

/*-------------------------------------------------|
|* Domain knowledge for CAN                       *|
|* Dialogue: 'doors'                              *|
|*-------------------------------------------------/
	Original dialogue:
	==================
A1 - Ben moi, j'en bave actuellement parce qu'il faut que je refasse mes portes,
la peinture. Alors j'ai d‚cap‚ … la chaleur. Ca part bien. Mais pas partout.
C'est un travail dingue, hein? 
B1- heu, tu as essay‚ de.  Tu as d‚cap‚ tes portes? 
A2- Ouais, ‡a part trŠs bien … la chaleur, mais dans les coins, tout , les
moulures, c'est infaisable. [plus fort] Les moulures.  
B2- Quelle chaleur? La lampe … souder? 
A3- Ouais, avec un truc sp‚cial.  
B3- Faut une brosse, dure, une brosse m‚tallique.  
A4- Oui, mais j'attaque le bois.  
B4- T'attaques le bois.  
A5- [pause 5 secondes] Enfin je sais pas. C'est un boulot dingue, hein?
C'est plus de boulot que de racheter une porte, hein? 
B5- Oh, c'est pour ‡a qu'il vaut mieux laiss... il vaut mieux simplement poncer,
repeindre par dessus 
A6- Ben oui, mais si on est les quinziŠmes … se dire ‡a 
B6- Ah oui.  
A7- Y a d‚j… trois couches de peinture, hein, dessus.  
B7- Remarque, si elle tient bien, la peinture, l… o— elle est ‚caill‚e, on
peut enduire. De l'enduit … l'eau, ou 
A8- Oui, mais l'‚tat de surface est pas joli, quoi, ‡a fait laque, tu sais,
‡a fait vieille porte.  
	English translation:
	===================
A1-  I have to repeindre my doors. I've burned off the old paint. It worked OK, but not everywhere. It's really tough work! [...] In the corners, all this, the il_y_a_des_moulures, it's not feasible !
[...]
B1- You have to use a wire brush   
A2- Yes, but that wrecks the wood   
B2- It wrecks the wood...   
[pause 5 seconds]
A3- It's crazy! It's more trouble than buying a new door.
B3- Oh, that's why you'd do better just on_ponce and repeindreing them.   
A4- Yes, but if we are the fifteenth ones to think of that   
B4- Oh, yeah...   
A5- There are already three layers of paint   
B5- If the old remaining paint sticks well, you can fill in the peeled spots with filler compound   
A6- Yeah, but the surface won't look great. It'll look like an old door.
	Content to reconstruct:
	=======================
A1- repeindre, burn-off, il_y_a_des_moulures, tough work
B1- wire brush
A2- wood wrecked
A3- tough work
B3- on_ponce
A5- several layers
B5- filler compound
A6- not nice surface
                                                                              */


	/*------------------------------------------------*/
	/* Domain knowledge starts here                   */
	/*------------------------------------------------*/

	/* pay attention to the fact that the following
	   lines are not Prolog clauses, but will be interpreted
	   by the program. 
	   The only Prolog predicates are:
	   - initial_situation
	   - action
	   - default
	   - preference
	   - incompatible
	   -  <===	(physical effects)
	   -  <---	(results of actions)-	(not used)
	 */ 

	language('French').
	
	% initial facts
	initial_situation(-les_portes_sont_belles).
	initial_situation(-l_etat_de_surface_est_bon).
	initial_situation(il_y_a_des_moulures).		%%%%% solution %%%%%
	initial_situation(le_bois_est_tendre).		%%%%% solution %%%%%
	initial_situation(il_y_a_plusieurs_couches).		%%%%% solution %%%%%


	% actions
	action(repeindre).
	action(on_decape).
	action(on_utilise_une_brosse_métallique).
	action(on_ponce).
	action(on_met_de_l_enduit).

	
	% defaults
	default(-le_bois_est_tendre).
	default(-il_y_a_plusieurs_couches).
	default(-on_utilise_une_brosse_métallique).	
	default(-ca_abime_le_bois).		%%%%% solution %%%%%


	% prerequisites


	% causal clauses
	l_etat_de_surface_est_bon <=== on_decape + -ca_abime_le_bois.
	l_etat_de_surface_est_bon <=== on_ponce + -il_y_a_plusieurs_couches + -ca_abime_le_bois.		%%%%% solution %%%%%
	l_etat_de_surface_est_bon <=== on_met_de_l_enduit + -ca_abime_le_bois.		%%%%% solution %%%%%
	les_portes_sont_belles <=== repeindre + l_etat_de_surface_est_bon.

	
	% physical consequences
	c_est_un_travail_dingue <=== on_decape + il_y_a_des_moulures + -on_utilise_une_brosse_métallique.
	ca_abime_le_bois <=== on_utilise_une_brosse_métallique + le_bois_est_tendre.
	-l_etat_de_surface_est_bon <=== ca_abime_le_bois.


	% preferences (termes positifs seulement)
	preference(c_est_un_travail_dingue, -10).
	preference(les_portes_sont_belles, 20).

	% dictionary
	
	dictionary(-les_portes_sont_belles,les portes sont moches)
	dictionary(les_portes_sont_belles,les portes sont belles)
	dictionary(-l_etat_de_surface_est_bon,l etat de la surface est mauvais)
	dictionary(l_etat_de_surface_est_bon,l etat de la surface est bon)
	dictionary(il_y_a_des_moulures,il y a des moulures)
	dictionary(-il_y_a_des_moulures,il n y a pas des moulures)
	dictionary(le_bois_est_tendre,le bois est tendre)
	dictionary(-le_bois_est_tendre,le bois est dur)
	dictionary(il_y_a_plusieurs_couches,il y a plusieurs couches)
	dictionary(-il_y_a_plusieurs_couches,il y a une seule couche)
	dictionary(repeindre,on repeint)
	dictionary(-repeindre,on ne repeint pas)
	dictionary(on_decape,on decape)
	dictionary(-on_decape,on ne decape pas)
	dictionary(on_utilise_une_brosse_métallique,on utilise une brosse metallique)
	dictionary(-on_utilise_une_brosse_métallique,on utilise pas de brosse metallique)
	dictionary(on_ponce,on ponce)
	dictionary(on_ponce,on ne ponce pas)
	dictionary(on_met_de_l_enduit,on met d enduit)
	dictionary(on_met_de_l_enduit,on ne met pas d enduit)
	dictionary(ca_abime_le_bois,cela abime le bois)
	dictionary(-ca_abime_le_bois,cela respecte le bois)
	dictionary(c_est_un_travail_dingue,c est un travail de dingue)
	dictionary(c_est_un_travail_dingue,ce n est pas un travail de dingue)