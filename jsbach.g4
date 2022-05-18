grammar jsbach;

root : stmt* EOF ;


stmt 
    : comment
    | declFunc
    | callFunc
    | assigs 
    | sentenceIf
    | sentenceWhile
    | listStmt
    | playStmt
    | readStmt
    | writeStmt
    | expr
    ;


/****************COMENTARIS****************/
comment : COM (ID*) COM ;



/****************PROCEDIMENTS****************/
declFunc : ID+ L_LMT(stmt*)R_LMT ; //Primer tenim l'ID inicial que representa el nom de la funció, després 0 o més ID (paràmetres).

callFunc : ID (ID | expr )* ;


/****************LECTURA****************/
readStmt : READ ID ;


/****************ESCRIPTURA****************/
writeStmt : WRITE (ID | expr)+ ; 


/****************CONDICIONAL****************/
sentenceIf : IF relExp L_LMT stmt* R_LMT (ELSE L_LMT stmt* R_LMT)? ;


/*****************ASSIGNACIÓ****************/
assigs : <assoc=right> ID ASSIG expr ;


/****************ITERACIONS****************/
sentenceWhile : WHILE relExp  L_LMT stmt* R_LMT ;


/****************LLISTES****************/
listStmt
    : listAddStmt 
    | listCutStmt 
    | listDecl
    | listGet
    | listSizeStmt
    ;

listConst : '{' (expr)* '}' ;

listDecl : ID ASSIG listConst ;

listAddStmt: ID LIST_ADD (expr) ;

listCutStmt: LIST_CUT ID L_KEY (expr) R_KEY ;

listSizeStmt: LIST_SIZE ID ;

listGet : ID L_KEY (expr) R_KEY ; 


/****************NOTES****************/
playStmt
    : PLAY '{' (expr+) '}' 
    | PLAY ID
    ;


/****************EXPRESSIONS****************/

relExp 
    : expr (EQ | DIF | LST | GRT | GREQ | LSEQ) expr 
    | expr
    ;

expr 
    : L_LMT expr R_LMT
    | expr (DIV | MUL | MOD) expr 
    | expr (ADD | SUB) expr  
    | (ID | NUM | NOTE)
    ;


/****************Especificació de JSBach****************/

/*Operadors relacionals*/
//Retornen 0 com a valor fals i 1 com a valor cert
EQ : '='; 
DIF : '/='; 
LST : '<' ;
GRT : '>' ; 
GREQ : '>=' ;
LSEQ :  '<=';

/*Condicionals i iteracions*/
IF : 'if' ;
WHILE : 'while' ;
ELSE : 'else' ;

/*Assignació*/
ASSIG : '<-' ;

/*Lectura*/
READ : '<?>' ;

/*Escriptura*/ 
WRITE : '!' ;

/*Limitadors*/ 
L_LMT : '|:' ;
R_LMT : ':|' ;

/*Definicions bàsiques*/
NUM  : (DIGIT)+ ;
DIGIT   : '0'..'9' ;
ID  : [a-zA-Z] ;

/*Notes*/
PLAY : '<:>' ;
NOTE : ('A' .. 'G' | '0' .. '8') ; 

/*Operadors amb llistes*/
LIST_ADD : '<<' ;
LIST_CUT : '8<' ;
LIST_SIZE : '#' ;
L_KEY : '[' ;
R_KEY : ']' ;
COM : '~~~' ;

/**************** Operadors aritmètics ****************/
ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;
MOD : '%' ;

/****************Definició de skip****************/
WS      : [ \t\r\n]+ -> skip ;


/******DUDAS*****/

/*
    1. Como solucionamos recursividad por la izquierda en expr y otras?
*/