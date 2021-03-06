/*---------------------------------------------------------------*/
/* Telecom Paristech - J-L. Dessalles 2017                       */
/*            http://teaching.dessalles.fr                       */
/*---------------------------------------------------------------*/

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%  Deliberative reasoning & Argumentation %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

/*-------------------------------------------------|
|* Domain knowledge for CAN                       *|
|* Dialogue: 'proportionnelle'                             *|
|*-------------------------------------------------/
	/*------------------------------------------------*/
	/* Domain knowledge starts here                   */
	/*------------------------------------------------*/

	/* pay attention to the fact that the following
	   lines are not Prolog clauses, but will be interpreted by the program. 
	   The only Prolog predicates are:
	   - initial_situation
	   - action
	   - default
	   - preference
	   - belief
	   - incompatible
	   -  <===	(physical effects)
	   -  <---	(results of actions)-	(not used)
	 */ 

	language('French').
	
	
	% initial facts
	initial_situation(-proportionnelle).
	initial_situation(-confiance_des_electeurs_vis_a_vis_des_institutions).


	% defaults
	initial_situation(-proportionnelle).
	initial_situation(-confiance_des_electeurs_vis_a_vis_des_institutions).

	% incompatibilities
	incompatible(proportionnelle,-proportionnelle).
   incompatible(confiance_des_electeurs_vis_a_vis_des_institutions,manque_de_confiance_des_electeurs_vis_a_vis_des_institutions).


	% causal clauses
	proportionnelle <=== passer_proportionnelle.
	-proportionnelle <=== passer_non_proportionnelle.
	justice <=== representativitee.
	representativitee <=== proportionnelle.
	confiance_des_electeurs_vis_a_vis_des_institutions <=== proportionnelle.
	perte_de_l_esprit_local <=== proportionnelle.
	comptes_rendus_aux_responsables_politiques <=== perte_de_l_esprit_local.
	necessite_d_une_majorite <=== difficulte_a_gouverner.
	manque_de_confiance_des_electeurs_vis_a_vis_des_institutions <=== comptes_rendus_aux_responsables_politiques.

	% actions
	action(passer_proportionnelle).
   action(passer_non_proportionnelle).
	
	% beliefs
	justice <=== proportionnelle.

	% preferences (termes positifs seulement)
	preference(confiance_des_electeurs_vis_a_vis_des_institutions,20).
	preference(manque_de_confiance_des_electeurs_vis_a_vis_des_institutions,-10).
	preference(justice,5).

	% dictionnaire

	dictionary(proportionnelle,la proportionnelle est en vigueur)
	dictionary(-proportionnelle,la proportionnelle n est pas en vigueur)
	dictionary(confiance_des_electeurs_vis_a_vis_des_institutions,les electeurs ont confiance en leurs institutions)
	dictionary(-confiance_des_electeurs_vis_a_vis_des_institutions,les electeurs n ont pas confiance en leurs institutions)
	dictionary(justice,le systeme est juste)
	dictionary(-justice,le systeme n est pas juste)
	dictionary(representativitee,le systeme est representatif)
	dictionary(-representativitee,le systeme n est pas representatif)
	dictionary(comptes_rendus_aux_responsables_politiques,les deputes rendent des comptes uniquement a leurs responsables politiques)
	dictionary(-comptes_rendus_aux_responsables_politiques,les deputes ne rendent pas de comptes uniquement a leurs responsables politiques)
	dictionary(perte_de_l_esprit_local,on perd l esprit local)
	dictionary(-perte_de_l_esprit_local,on garde l esprit local)
	dictionary(necessite_d_une_majorite,une majoritee est necessaire)
	dictionary(-necessite_d_une_majorite,une majoritee n est pas necessaire)
	dictionary(difficulte_a_gouverner,il est difficile de gouverner)
	dictionary(-difficulte_a_gouverner,il est facile de gouverner)
	dictionary(manque_de_confiance_des_electeurs_vis_a_vis_des_institutions,les electeurs manquent de confiance dans la legitimite de leurs elus)
	dictionary(-manque_de_confiance_des_electeurs_vis_a_vis_des_institutions,les electeurs ne manquent pas de confiance dans la legitimite de leurs elus)
	dictionary(passer_proportionnelle,on instaure la proportionnelle)
	dictionary(passer_non_proportionnelle,on retire la proportionnelle)
   
