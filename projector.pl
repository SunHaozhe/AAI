/*---------------------------------------------------------------*/
/* Telecom Paristech - J-L. Dessalles 2012                       */
/*            http://teaching.dessalles.fr                       */
/*---------------------------------------------------------------*/

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%  Deliberative reasoning & Argumentation %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

/*-------------------------------------------------|
|* Domain knowledge                               *|
|* Dialogue: 'projector'                          *|
|*------------------------------------------------/

	Original dialogue:
	==================
	R1-	Et tu peux pas le mettre la, le projo ?
	S1-	Je l'ai mis la parce que j'osais pas le poser sur ton bureau. 
		Et la, je vais projeter sur la  poignee. Ca va etre bien !
	R2-	Mets des bouquins en dessous, va. Mais tu peux pas l'incliner ?
	S2-	Ca va deformer l'image.


	English translation:
	===================
	R1-	Can't you put the projector here ?
	S1-	I put it there because I didn't dare to put it on your desk. 
		And here, I'll project on the handle. That will be nice! 
	R2-	Put books underneath. But can't you tilt it ?
	S2-	It will distort the image.                                     
	                                                                      */


	/*------------------------------------------------*/
	/* Domain knowledge starts here                   */
	/*------------------------------------------------*/
	
	/* pay attention to the fact that the following
	   lines are not Prolog clauses, but will be interpreted
	   by the programme. 
	   The only Prolog predicates are:
	   - initial_situation
	   - action
	   - default
	   - preference
	   - incompatible
	   -  <===	(physical effects)
	   -  <---	(results of actions)- 
	 */ 
	
	% initial facts
	%initial_situation(on(books, desk)).
	initial_situation(-on(image, doors)).
	initial_situation(on(projector, shelves)).	% implies: on(image, doors)


	% actions
	action(remove(_Object,_From)).
	action(move(_Object,_To)).
	action(put_underneath(_Object1,_Object2)).
	action(tilt(_Object)).

	% default predicates: these predicates are true unless proven false
	%default(-on(_Object,_Place)).
	default(horizontal(_)).
	default(stable(_)).
	default(clear(_Loc)).
	default(physical(_)).
	default(-distorted(_)).

	% logical clauses
	incompatible([physical(image)]).
	%incompatible([clear(L), on(_,L)]).
	
	% actions
	on(Object, To) <--- move(Object, To).
	-on(Object, From) <--- remove(Object, From).
	-horizontal(projector) <--- put_underneath(books,projector).
	-horizontal(P) <--- tilt(P).

	% prerequisites
	move(Object, To) <=== clear(To) + physical(Object).
	remove(Object, From) <=== on(Object, From).
	tilt(P) <=== horizontal(P).
	put_underneath(_, P) <=== horizontal(P).
	
	% physical laws
	-clear(desk) <=== on(books, desk).
	-stable(projector) <=== on(projector, shelves).
	on(image,door) <=== on(projector, shelves).
	on(image,door) <=== on(projector, desk).
	on(image,handle) <=== on(projector, desk) + horizontal(projector).
	distorted(image) <=== -horizontal(projector).
	-on(image,handle) <=== on(projector, shelves).

	% preferences (termes positifs seulement)
	preference(stable(projector), 40).
	preference(on(image,door), 30).
	preference(on(image,handle), -20).
	preference(distorted(image), -10).

	