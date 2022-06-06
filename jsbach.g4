grammar jsbach;

/*
Com JSBach és un llenguatge procedural, el que posem a l'arrel de la gràmatica és que el programa 
estarà format per una o més declaracions de funcions, on dintre de cadascuna podrem dividir les parts del codi
corresponent en instruccions.
*/
root : declFunc+ EOF ;


/****************PROCEDIMENTS****************/

/*
La declaració d'una funció no és una altra cosa que el propi nom que és el primer token, seguit de 0 o més 
identificadors, els quals representen els possibles paràmetres que pot tenir la funció. A continuació, es presenta
el cos que és un conjunt d'instruccions, delimitat per els limitadors quan es declara una nova funció.
*/
declFunc : FNC_NAME (ID)* L_LMT conjStmt R_LMT ;


/****************CONJUNT D'INSTRUCCIONS****************/
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
o una expressió, a més de la consulta d'un valor d'una llista i el nombre d'elements que té. Una cadena està formada per les cometes '"', 
després tota la informació que es vulgui donar excepte: \n, \r i |t, i per finalitzar les cometes '"' que tanquen la cadena.
*/
writeStmt : WRITE (listGet | listSize | expr | CADENA)* ; 


/*****************ASSIGNACIÓ****************/
/*
Una assignació està formada pel primer token que es un ID, el nom de la variable on es guardarà la informació, seguida del token d'assignació i després
l'expressió, que conté el valor el qual es vol guardar. L'expressió pot ser la consulta d'un valor o nombre d'elements d'una llista, la constructora d'una
llista o directament una expressió bàsica.
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

/*
Una instrucció del tipus llista pot ser esborrar l'i-èsim element o afegir l'element al final de la llista.
*/
listStmt
    : listAddStmt 
    | listCutStmt 
    ;

/*
La constructora d'una llista està formada pels dos símbols que representen la creació de la llista i dintre tenim
els possibles valors que poden conformar una llista, és a dir, un número o una nota. 
*/
listConst : LCOR (NUM | NOTE)* RCOR ;

/*
Per afegir un element a una llista tenim la gramàtica següent. Primer tenim l'ID que representa el nom de la llista,
seguidament tenim l'operador d'afegir un element a una llista en JSBach, i finalment tenim l'expressió, que conté el 
valor de l'element que es vol incloure al final de la llista. La idea per afegir un element seria: nomLlista << expressió.
*/
listAddStmt: ID LIST_ADD (expr) ;


/*
Per eliminar un element d'una llista tenim la gramàtica següent. Es pot observar que el primer de tot és l'operador 
de tisores (tallar/eliminar un element), i a continuació tenim l'id que representa el nom de la llista, seguit de
els limitadors i dins d'aquests l'expressió que indica l'índex de l'element que es vol esborrar. 
La idea seria aquesta: 8< nomLlista[expressió]
*/
listCutStmt: LIST_CUT ID L_KEY (listSize | expr) R_KEY;

/*
Aquesta instrucció retorna el nombre d'elements que té la llista amb nom ID. Està formada pel operador que indica 
que es vol consultar el tamany de la llista amb nom ID. La idea seria: #nomLlista
*/
listSize: LIST_SIZE ID ;


/*
Aquesta instrucció retorna el valor de l'element i-èsim de la llista. La gramàtica està formada pel nom de la llista,
seguida dels limitadors i dintre d'aquests es troba la expressió o la consulta de tamany de la llista. Un exemple 
seria: lista[expressió] o lista[#lista]
*/
listGet : ID L_KEY (expr | listSize) R_KEY ; 


/****************NOTES****************/

/*
Aquesta instrucció afegeix les notes corresponents a la partitura que després es genera en acabar el programa jsbach. La 
gramàtica pot venir donada de dues maneres: el símbol de play (<:>) seguit de la constructora d'una llista o el símbol 
de play (<:>) seguit d'un ID que representa una o més notes, ja sigui en format NOTE o en format NUM.
*/
playStmt
    : PLAY listConst #PlayLists 
    | PLAY ID #PlayId
    ;


/****************EXPRESSIONS****************/

/*
Arribem finalment a les expressions amb operadors relacionals. 

Per definir una expressió amb operadors relacionals tenim les dues expressions  
i just enmig tenim l'operador corresponent. Aquesta instrucció sempre retornarà un número, si és 1 o més d'1 retornarà 
cert, en cas contrari retorna fals. Uns exemples serien: x <= 10 o y > 5.
*/
relExp 
    : (expr) (EQ | DIF | LST | GRT | GREQ | LSEQ) (expr) 
    | NUM
    ;

/*
Per concluir, tenim les expressions amb operadors aritmètics i altres.
La gramàtica d'una expressió ve donada pels limitadors de parèntesis i l'expressió dins d'aquests, o una expressió amb un operador 
aritmètic i un altra expressió. Per acabar, una expressió pot ser: una nota (NOTE), un nombre (NUM) o una variable (ID). Alguns 
exemples serien: (10/2), C4 - 1, x * 5 o 2 + 2.
*/
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
LCOR : '{' ;
RCOR : '}' ;

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
