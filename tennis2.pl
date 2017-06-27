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
	initial_situation(joue(femmes, '3_sets')).
	initial_situation(joue(hommes, '5_sets')).
	initial_situation(court_marathon(femmes)).
	initial_situation(court_marathon(hommes)).
	initial_situation(exemple(femmes, '5_sets', 1980)).
	initial_situation(capable(hommes, '5_sets')).

	% actions
	action(passer(_, _, _)).
	
	% defaults
	default(-capable(femmes, '5_sets')).
	default(-audience(femmes)).
	default(endurant(hommes)).

	% incompatibilities
	incompatible([egalite(femmes,hommes), joue(hommes, '5_sets'), joue(femmes, '3_sets')]).
	% incompatible([egalite(X,Y), capable(X, A), -capable(Y, A)]).
	incompatible([-capable(X, A), exemple(X, A, _)]).
	incompatible([joue(X, '5_sets'), -endurant(X)]).
	incompatible([-capable(X, '5_sets'), endurant(X)]).
	incompatible([-endurant(X), court_marathon(X)]).
	incompatible([-joue(X, '5_sets'), -joue(X, '3_sets')]).
	incompatible([joue(X, '5_sets'), joue(X, '3_sets')]).


	% causal clauses
	audience(X) <=== joue(X, '5_sets').
	-audience(X) <=== joue(X, '3_sets').
	joue(X, '5_sets') <=== passer(X, '3_sets', '5_sets').
	joue(X, '3_sets') <=== passer(X, '5_sets', '3_sets').
	
	% prerequisites
	passer(X, '3_sets', '5_sets') <--- joue(X, '3_sets').
	passer(X, '5_sets', '5_sets') <--- joue(X, '5_sets').
	
	% beliefs

	% preferences (termes positifs seulement)
	preference(egalite(femmes, hommes), 10).
	preference(audience(femmes), 5).
	preference(audience(hommes), 5).
	% preference(joue(hommes, '5_sets'), 5).
