grammar Test;
prog: ID+;
ID: [a-z]+;
WS: [ \t\r\n]+ -> skip;
