grammar jsbach;

root : stmt* EOF ;


stmt : 

    ;
selectStmt : 'if' expr stmt | 'if' expr stmt 'else' stmt;

iterStmt : 'while' expr 'do' stmt
    | <assoc=right> ID ASSIG expr 
    ;

condSmt : expr opRel expr;

expr : <assoc=right> expr POW expr 
    | expr (DIV | MUL) expr 
    | expr (ADD | SUB) expr  
    | LFTLMT expr RGTLMT 
    | relTerm
    ;
/******Operadors relacionals******/

boolExp : boolExp 'or' boolTerm | boolTerm;
boolTerm : boolTerm 'and' boolFactor | boolFactor;
boolFactor : 'not' boolFactor | ( boolExp ) | relExp;

relExp : relTerm opRel relTerm | relTerm ;


//Retornen 0 com a valor fals i 1 com a valor cert
opRel : '=' | '/=' | '<' | '>' | '>=' | '<=';

relTerm : (ID | NUM);



/******Especificació de JSBach******/
ASSIG : '<-' ;
RD : '<?>' ;
WR : '!' ;
PLAY : '<:>' ;

LFTLMT : '|:' ;
RGTLMT : ':|' ;

COM : '~~~' ;
/*
Falta: 
    -Invocació de procediments
    -Condicional amb if i potser else
    -Iteracio amb while 
    -Gramatica de llistes i notes: Afegit(<<) i tall de llistes (8<)

*/





/****** Operadors aritmètics ******/
ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;
MOD : '%' ;

/****** Definicions bàsiques ******/
DIGIT   : '0'..'9' ;
ID  : [a-zA-Z] ;

NUM  : (DIGIT)+ ;

WS      : [ \t\n]+ -> skip ;
