grammar jsbach;

root : stmt* EOF ;

//block : stmt* ;

stmt 
    : declFunc
    | callFunc
    | assigs 
    | sentenceIf
    | sentenceWhile 
    ;

/*
    Falta por añadir la declaración de función y la llamada a función
*/
declFunc : ID+ L_LMT(stmt*)R_LMT ;

callFunc:  ID (ID* | expr )+ ;
 

readStmt : READ ID ;

writeStmt : WRITE (| ID | expr)+ ;

sentenceIf : IF boolExp L_LMT stmt* R_LMT (ELSE L_LMT stmt* R_LMT)? ;


assigs : <assoc=right> ID ASSIG expr ;


sentenceBlock 
    : L_LMT stmt*  R_LMT 
    | stmt
    ;


sentenceWhile : WHILE boolExp  L_LMT stmt* R_LMT ;

expr 
    : L_LMT expr R_LMT
    | <assoc=right> expr POW expr 
    | expr (DIV | MUL | MOD) expr 
    | expr (ADD | SUB) expr  
    | (ID | NUM)
    ;

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

COM : '~~~' ;
/*
Falta: 
    -Invocació de procediments
    -Gramatica de llistes i notes: Afegit(<<) i tall de llistes (8<)
    -Lectura
    -Escriptura
    -Reproduccio
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
    2. OR y AND tienen que tener la misma prioridad?
    3. 
*/