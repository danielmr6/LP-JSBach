grammar jsbach;

root : block* EOF ;

block : sentence* ;

sentence 
    : assigs 
    | sentenceIf
    | sentenceWhile 
    ;


sentenceIf : 'if' boolExp sentenceBlock ('else' sentenceBlock)? ;


assigs : <assoc=right> ID ASSIG expr ;


sentenceBlock 
    : LFTLMT block RGTLMT 
    | sentence
    ;


sentenceWhile : 'while' boolExp  sentenceBlock ;

expr 
    : <assoc=right> expr POW expr 
    | expr (DIV | MUL) expr 
    | expr (ADD | SUB) expr  
    | relTerm
    ;

/**************** Operadors relacionals ****************/

boolExp 
    : boolExp 'or' boolTerm 
    | boolTerm
    ;


boolTerm 
    : boolTerm 'and' boolFactor 
    | boolFactor
    ;


boolFactor 
    : 'not' boolFactor 
    | ( boolExp ) 
    | relExp
    ;


relExp 
    : relTerm (EQ | DIF | LST | GRT | GREQ | LSEQ) relTerm 
    | relTerm 
    ;


relTerm 
    :  LFTLMT expr RGTLMT
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

/**************** Definicions bàsiques ****************/
DIGIT   : '0'..'9' ;
ID  : [a-zA-Z] ;
NUM  : (DIGIT)+ ;
WS      : [ \t\n]+ -> skip ;