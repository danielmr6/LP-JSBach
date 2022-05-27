grammar jsbach;

root : declFunc+ EOF ;


/****************PROCEDIMENTS****************/
declFunc : ID L_LMT conjStmt R_LMT ;

callFunc : ID (ID | expr )* ;


/**************** CONJUNT D'INSTRUCCIONS****************/
conjStmt : stmt* ;

stmt 
    : (callFunc | assigs | sentenceIf | sentenceWhile | listStmt | playStmt | readStmt | writeStmt)
    | (expr | relExp)
    ;

/*****************ASSIGNACIÓ****************/
assigs : ID ASSIG expr ;

/****************LECTURA****************/
readStmt : READ ID ;


/****************ESCRIPTURA****************/
writeStmt : WRITE (ID | expr | CADENA)* ; 


/****************CONDICIONAL****************/
sentenceIf : IF relExp L_LMT stmt* R_LMT (ELSE L_LMT conjStmt R_LMT)? ;


/****************ITERACIONS****************/
sentenceWhile : WHILE relExp  L_LMT conjStmt R_LMT ;


/****************LLISTES****************/
listStmt
    : listAddStmt 
    | listCutStmt 
    | listDeclStmt
    | listGet
    | listSize
    ;

listConst : '{' (expr)* '}' ;

listDeclStmt : ID ASSIG listConst ;

listAddStmt: ID LIST_ADD (expr) ;

listCutStmt: LIST_CUT ID L_KEY (expr) R_KEY ;

listSize: LIST_SIZE ID ;

listGet : ID L_KEY (expr) R_KEY ; 


/****************NOTES****************/
playStmt
    : PLAY '{' (expr+) '}' 
    | PLAY ID
    ;


/****************EXPRESSIONS****************/

relExp 
    : expr (EQ | DIF | LST | GRT | GREQ | LSEQ) expr 
    | (TRUE | FALSE | expr)
    ;

expr 
    : LPAR expr RPAR #Parents
    | expr (DIV | MUL | MOD) expr #DivMulMod
    | expr (ADD | SUB) expr  #AddSub
    | (listSize | listGet) #Lists
    | NOTE #Note
    | NUM #Num
    | ID #VarId
    ;


/****************Especificació de JSBach****************/

/*Assignació*/
ASSIG : '<-' ;

/*Lectura*/
READ : '<?>' ;

/*Escriptura*/ 
WRITE : '<!>' ;

/*Operadors relacionals*/
EQ : '='; 
DIF : '/='; 
LST : '<' ;
GRT : '>' ; 
GREQ : '>=' ;
LSEQ :  '<=';
TRUE : '1' ;
FALSE : '0' ;


/*Limitadors*/ 
L_LMT : '|:' ;
R_LMT : ':|' ;
L_KEY : '[' ;
R_KEY : ']' ;
LPAR : '(' ;
RPAR : ')' ;
TXT : '"' ;

/*Condicionals i iteracions*/
IF : 'if' ;
WHILE : 'while' ;
ELSE : 'else' ;


/*Definicions bàsiques*/
NUM  : (DIGIT)+ ;
DIGIT   : '0'..'9' ;
ID  : [a-zA-Z]+ ;

/*Notes*/
PLAY : '<:>' ;
NOTE : ('A' .. 'G') ('0' .. '8')? ; 

/*Operadors amb llistes*/
LIST_ADD : '<<' ;
LIST_CUT : '8<' ;
LIST_SIZE : '#' ;
COM : '~~~' ;

/**************** Operadors aritmètics ****************/
ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;
MOD : '%' ;

CADENA : '"' (~('"' | '\n' | '\r' | '\t'))*'"';


/****************Definició de skip****************/
WS     : [ \t\r\n]+ -> skip ;
NL : (('\r\n')) ;

COMMENT : '~~~' (('*' NL) | ('*' ~('\n' | '\r')) | NL | ~( '\n' | '\r' | '*'))* '~~~' -> skip ;

/******DUBTES*****/

/*
    1. Recursivitat per l'esquerra?
    2. Write, If, While, visitor de expressió o es fa un altre a part?
    4. Pila de diccionaris
*/