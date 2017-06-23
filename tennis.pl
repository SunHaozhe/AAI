/*---------------------------------------------------------------*/
/* Telecom Paristech - J-L. Dessalles 2017                       */
/*            http://teaching.dessalles.fr                       */
/*---------------------------------------------------------------*/

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%  Deliberative reasoning & Argumentation %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

/*-------------------------------------------------|
|* Domain knowledge for CAN                       *|
|* Dialogue: 'tennis'                             *|
|*-------------------------------------------------/

	Original argumentation:
http://www.lemonde.fr/tennis/video/2017/05/28/roland-garros-pourquoi-les-femmes-jouent-elles-en-3-sets-et-non-en-5_5134920_1616659.html
	==================*/

	

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
	initial_situation(joue_femmes_3_sets).
	initial_situation(joue_hommes_5_sets).
	initial_situation(court_marathon_femmes).
	initial_situation(court_marathon_hommes).
	initial_situation(exemple_femmes_5_sets_1980).
	initial_situation(capable_hommes_5_sets).

	% actions
	action(passer_hommes_3sets).
	action(passer_hommes_5sets).
	action(passer_femmes_3sets).
	action(passer_femmes_5sets).
	
	% defaults
	default(-capable_femmes_5_sets).
	default(-audience_femmes).
	default(endurant_hommes).

	% incompatibilities
	incompatible([egalite_femmes_hommes, joue_hommes_5_sets, joue_femmes_3_sets]).
	incompatible([egalite_femmes_hommes, joue_hommes_3_sets, joue_femmes_5_sets]).
	incompatible([egalite_femmes_hommes, capable_hommes_5_sets, -capable_femmes_5_sets]).
	incompatible([egalite_femmes_hommes, capable_hommes_3_sets, -capable_femmes_3_sets]).
	incompatible([egalite_femmes_hommes, -capable_hommes_5_sets, capable_femmes_5_sets]).
	incompatible([egalite_femmes_hommes, capable_hommes_5_sets, -capable_femmes_5_sets]).
	incompatible([-capable_femmes_5_sets, exemple_femmes_5_sets_1980]).
	incompatible([joue_hommes_5_sets, -endurant_hommes]).
	incompatible([joue_femmes_5_sets, -endurant_femmes]).
	incompatible([-capable_hommes_5_sets, endurant_hommes]).
	incompatible([-capable_femmes_5_sets, endurant_femmes]).
	incompatible([-endurant_hommes, court_marathon_hommes]).
	incompatible([-endurant_femmes, court_marathon_femmes]).
	incompatible([-joue_hommes_5_sets, -joue_hommes_3_sets]).
	incompatible([-joue_femmes_5_sets, -joue_femmes_3_sets]).
	incompatible([joue_hommes_5_sets, joue_hommes_3_sets]).
	incompatible([joue_femmes_5_sets, joue_femmes_3_sets]).

	% causal clauses
	audience_femmes <=== joue_femmes_5_sets.
	audience_hommes <=== joue_hommes_5_sets.
	-audience_femmes <=== joue_femmes_3_sets.
	-audience_hommes <=== joue_hommes_3_sets.
	joue_hommes_3_sets <=== passer_hommes_3sets.
	joue_hommes_5_sets <=== passer_hommes_5sets.
	joue_femmes_3_sets <=== passer_femmes_3sets.
	joue_femmes_5_sets <=== passer_femmes_5sets.
	
	% prerequisites

	passer_hommes_3sets <--- joue_hommes_5_sets.
	passer_hommes_5sets <--- joue_hommes_3_sets.
	passer_femmes_3sets <--- joue_femmes_5_sets.
	passer_femmes_5sets <--- joue_femmes_3_sets.

	
	% beliefs

	% preferences (termes positifs seulement)
	preference(egalite_femmes_hommes, 10).
	preference(audience_femmes, 5).
	preference(audience_hommes, 5).
	preference(joue_hommes_5_sets, 5).
