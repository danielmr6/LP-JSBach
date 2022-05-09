grammar jsbach;

root : expr EOF ;

expr : expr DIV expr 
    | expr MUL expr 
    | <assoc=right> expr '^' expr
    | expr ADD expr 
    | expr SUB expr 
    | NUMBER ;

ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;


DIGIT   : '0'..'9' ;
LETTER  : [a-zA-Z] ;

NUMBER  : (DIGIT)+ ;

WS      : [ \t\n]+ -> skip ;
