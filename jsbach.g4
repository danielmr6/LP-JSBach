grammar jsbach;

root : stmt* EOF ;


stmt 
    : declFunc
    | callFunc
    | assigs 
    | sentenceIf
    | sentenceWhile
    | readStmt
    | writeStmt 
    ;

declFunc : ID+ L_LMT(stmt*)R_LMT ; //Primer tenim l'ID inicial que representa el nom de la funció, després 0 o més ID (paràmetres).

callFunc :  ID (ID* | expr )+ ;
 
readStmt : READ ID ;

writeStmt : WRITE (ID | expr)+ ; 

sentenceIf : IF boolExp L_LMT stmt* R_LMT (ELSE L_LMT stmt* R_LMT)? ;

assigs : <assoc=right> ID ASSIG expr ;


sentenceWhile : WHILE boolExp  L_LMT stmt* R_LMT ;

/****************Definicions de llistes****************/
listAddStmt: ID LIST_ADD ID ;

listCutStmt: LIST_CUT ID L_KEY (ID|NUM) R_KEY ;

listSizeStmt: LIST_SIZE ID ;

/**************** Operadors relacionals ****************/

boolExp 
    : boolExp OR boolTerm 
    | boolTerm
    ;


boolTerm 
    : boolTerm AND boolFactor 
    | boolFactor
    ;


boolFactor 
    : NOT boolFactor 
    | ( boolExp ) 
    | relExp
    ;


relExp 
    : expr (EQ | DIF | LST | GRT | GREQ | LSEQ) expr 
    | expr
    ;

expr 
    : L_LMT expr R_LMT
    | <assoc=right> expr POW expr 
    | expr (DIV | MUL | MOD) expr 
    | expr (ADD | SUB) expr  
    | (ID | NUM)
    ;

//Retornen 0 com a valor fals i 1 com a valor cert
EQ : '='; 
DIF : '/='; 
LST : '<' ;
GRT : '>' ; 
GREQ : '>=' ;
LSEQ :  '<=';

/****************Especificació de JSBach****************/
IF : 'if' ;
WHILE : 'while' ;
ELSE : 'else' ;
NOT : 'not' ;
OR : 'or' ;
AND : 'and' ;

ASSIG : '<-' ;
READ : '<?>' ;
WRITE : '!' ;
PLAY : '<:>' ;
NOTE : ('A' .. 'G' | '0' .. '8') ; //mirar notación inglesa
L_LMT : '|:' ;
R_LMT : ':|' ;

LIST_ADD : '<<' ;
LIST_CUT : '8<' ;
LIST_SIZE : '#' ;
L_KEY : '[' ;
R_KEY : ']' ;
COM : '~~~' ;
/*
Falta: 
    -Reproduccio
    - Play
    - notas y conjunto
    - listas
    -Ambit de visibilitat
*/

/**************** Operadors aritmètics ****************/
ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;
MOD : '%' ;
POW : '^' ;

/**************** Definicions bàsiques ****************/
DIGIT   : '0'..'9' ;
ID  : [a-zA-Z] ;
NUM  : (DIGIT)+ ;
WS      : [ \t\n]+ -> skip ;


/******DUDAS*****/

/*
    1. Como solucionamos recursividad por la izquierda en expr y otras?
    2. OR, AND, NOT no se tienen que añadir en la gramática no?
    3. Definicion de listas: preguntar y consulta?
*/