~~~ Kleines Program in JSBach ~~~

Main |: 
    x <- 1+2
    <!> x
    y <- (x + 3)
    <!> y
    
    while x < 7 |:
    	x <- x + 1
    :|
    
    <!> "Acabem While"
    <!> "La x es " x
    src <- { A B C D E F G }
    <!> "El primer element es " src[1]
    <!> "El darrer element es " src[7]
    <!> "El nombre d'elements es " #src
    
    <!> src
    src << A5
    <!> src
    8< src[1]
    <!> src
    
    src <- { 31 42 52 48 40 35 29 }
    <!> src
    <!> "El primer element es " src[1]
    <!> "El darrer element es " src[7]
    <!> "El nombre d'elements es " #src
    
    <!> src
    src << 8
    <!> src
    8< src[1]
    <!> src
    
    <:> src
    
    
    Altra x
:|

Altra n |:
	<!> n "->" n
:|




