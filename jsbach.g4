grammar jsbach;

/*
Com JSBach és un llenguatge procedural, el que posem a l'arrel de la gràmatica és que el programa 
estarà format per una o més declaracions de funcions, on dintre de cadascuna podrem dividir les parts del codi
corresponent.
*/
root : declFunc+ EOF ;


/****************PROCEDIMENTS****************/

/*
La declaració d'una funció no és una altra cosa que el propi nom que és el primer token, seguit de 0 o més 
identificadors, els quals representen els possibles paràmetres que pot tenir la funció. A continuació, es presenta
el cos que és un conjunt d'instruccions, delimitat per els limitadors quan es declara una nova funció.
*/
declFunc : FNC_NAME (ID)* L_LMT conjStmt R_LMT ;


/**************** CONJUNT D'INSTRUCCIONS****************/
/*
El conjunt d'instruccions és tot el que es pot trobar dins d'un codi d'una funció en JSBach. En aquest cas, he posat 
que pot haver un conjunt d'instruccions buit, ja que es pot donar el cas d'haver una funció que no té res de codi dins.
*/
conjStmt : stmt* ;

/*
Una instrucció és un conjunt de dades escrites en una seqüència estructurada de tal manera  que l'intèrpret pugui realitzar
unes operacions determinades. A continuació s'explica en més profunditat cadascuna d'elles.
*/
stmt 
    : (callFunc | assigs | sentenceIf | sentenceWhile | listStmt | playStmt | readStmt | writeStmt)
    | (expr | relExp)
    ;


/*
La crida a una funció ve determinada pel nom de la funció, el qual ha de començar per una lletra majúscula per poder fer 
la distinció entre el nom d'una funció i una variable del codi. Seguidament, es poden donar 0 o més expressions, les quals 
conformen els possibles paràmetres de la funció corresponent.
*/
callFunc : FNC_NAME (expr | listSize | listGet)* ;



/****************LECTURA****************/
/*
La lectura d'un valor que ens ve donat per l'entrada està formada pel primer token que té el significat de llegir, tal i com 
s'explica a l'especificació, i seguidament rep un ID, just en aquesta variable és on es guardarà el valor de la entrada.
*/
readStmt : READ ID;


/****************ESCRIPTURA****************/

/*
La gramàtica d'escriptura d'un valor ve definida pel token d'escriptura, seguit de 0 o més tokens, els quals poden ser una cadena
o una expressió. Una cadena està formada per les cometes '"', després tota la informació que es vulgui donar excepte: \n, \r i |t, 
i per finalitzar les cometes '"' que tanquen la cadena.
*/
writeStmt : WRITE (listGet | listSize | expr | CADENA)* ; 


/*****************ASSIGNACIÓ****************/
/*
Una assignació està formada pel primer token que es un ID, la variable on es guardarà la informació, seguida del token d'assignar i després
l'expressió, que conté el valor el qual es vol guardar.
*/
assigs : ID ASSIG expr 
    | ID ASSIG (listConst | listGet | listSize)
    ;

/****************CONDICIONAL****************/
/*
La gramàtica del condicional ve donada primer de tot pel token if, després la sentència te la expressió de relació, la qual 
retorna 1 si és certa, en cas contrari retorna el valor 0. A continuació tenim els limitadors amb el conjunt d'instruccions 
que s'executarien en cas de ser cert, i a la part final, tenim la gramàtica del else que pot estar o no al codi, aquest és el 
motiu pel qual he posat l'interrogant, per determinar si és un if o un if - else.
*/ 
sentenceIf : IF relExp L_LMT conjStmt R_LMT (ELSE L_LMT conjStmt R_LMT)? ;


/****************ITERACIONS****************/
/*
La gramàtica del bucle while ve donada pel token while, seguida de la condició, mentra la expressió de relació sigui certa, 
s'executaran el conjunt d'instruccions que estan dins del limitador del while.
*/
sentenceWhile : WHILE relExp  L_LMT conjStmt R_LMT ;


/****************LLISTES****************/
listStmt
    : listAddStmt 
    | listCutStmt 
    ;

listConst : '{' (NUM | NOTE)* '}' ;

listAddStmt: ID LIST_ADD (expr) ;

listCutStmt: LIST_CUT ID L_KEY (listSize | expr) R_KEY;

listSize: LIST_SIZE ID ;

listGet : ID L_KEY (expr | listSize) R_KEY ; 


/****************NOTES****************/
playStmt
    : PLAY listConst #PlayLists 
    | PLAY ID #PlayId
    ;


/****************EXPRESSIONS****************/

relExp 
    : (expr) (EQ | DIF | LST | GRT | GREQ | LSEQ) (expr) 
    | NUM
    ;

expr 
    : LPAR expr RPAR #Parentesis
    | expr (DIV | MUL | MOD) expr #DivMulMod
    | expr (ADD | SUB) expr  #AddSub
    | NOTE #Note
    | NUM #Num
    | ID #VarId
    ;


/****************Especificació de JSBach - TOKENS****************/

/*****************Assignació*****************/
ASSIG : '<-' ;

/*****************Lectura*****************/
READ : '<?>' ;

/*****************Escriptura*****************/ 
WRITE : '<!>' ;

/*****************Operadors relacionals*****************/
EQ : '='; 
DIF : '/='; 
LST : '<' ;
GRT : '>' ; 
GREQ : '>=' ;
LSEQ :  '<=';


/*****************Limitadors*****************/ 
L_LMT : '|:' ;
R_LMT : ':|' ;
L_KEY : '[' ;
R_KEY : ']' ;
LPAR : '(' ;
RPAR : ')' ;

/*****************Condicionals i iteracions*****************/
IF : 'if' ;
WHILE : 'while' ;
ELSE : 'else' ;


/*****************Definicions elementals*****************/
NUM  : (DIGIT)+ ;
DIGIT   : ('0'..'9') ;
FNC_NAME : [A-Z\u0080-\u00FF]([a-zA-Z\u0080-\u00FF] | '_')+;
ID  : [a-z\u0080-\u00FF]([a-zA-Z\u0080-\u00FF] | '_')* ;

/*****************Notes*****************/
PLAY : '<:>' ;
NOTE : ('A' .. 'G') ('0' .. '8')* ; 

/*****************Operadors amb llistes*****************/
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

/****************Definició d'una cadena****************/
CADENA : '"' (~('"' | '\n' | '\r' | '\t'))* '"';


/****************Definició de skip****************/
WS     : [ \t\r\n]+ -> skip ;
NL : (('\r\n')) ;

COMMENT : '~~~' (('*' NL) | ('*' ~('\n' | '\r')) | NL | ~( '\n' | '\r' | '*'))* '~~~' -> skip ;
