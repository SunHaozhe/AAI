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


	% causal clauses
	justice <=== representativitee.
	representativitee <=== proportionnelle.
	confiance_des_electeurs_vis_a_vis_des_institutions <=== proportionnelle.
	comptes_rendus_aux_responsables_politiques <=== proportionnelle.
	perte_de_l_esprit_local <=== comptes_rendus_aux_responsables_politiques.
	necessite_d_une_majorite <=== difficulte_a_gouverner.
	manque_de_confiance_des_electeurs_vis_a_vis_des_institutions <=== perte_de_l_esprit_local.

	% beliefs
	justice <=== proportionnelle.

	% preferences (termes positifs seulement)
	preference(confiance_des_electeurs_vis_a_vis_des_institutions,20).
	preference(manque_de_confiance_des_electeurs_vis_a_vis_des_institutions,-10).
	preference(justice,20).