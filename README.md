# El doble intèrpret de JSBach

Aquesta pàgina descriu la pràctica de GEI-LP (edició 2021-2022 Q2). La nostra tasca ha sigut implementar un doble intèrpret per a un llenguatge de programació musical anomenat JSBach. La sortida d'aquest doble intèrpret és una partitura i uns fitxers de so que reproduiràn la melodia descrita pel compositor.

Cal aclarir que diem que és un *doble* intèrpret perquè funciona en el sentit informàtic (interpreta un programa) i en el sentit musical (interpreta una peça de música).

## Tecnologies utilitzades 
Tal i com s'explicava a l'enunciat:

- Per realitzar la pràctica he utilitzat Python3 i ANTLR4.
- Per generar les partitures, he fet servir el programa Lilipond. 
- Per generar els WAV i MP3, els programes Timidity++ i ffmpeg.

## Instal·lació  

Amb l'objectiu de poder dur a terme la implementació de la gramàtica i l'intèrpret, vaig instal·lar `ANTLR` seguint els passos mencionats a les transparències del laboratori i, finalment, executant aquesta comanda per evitar problemes de incompatibilitat:
```bash
pip install antlr4-python3-runtime==4.7.1
```

# Introducció al llenguatge: JSBach

JSBach és un llenguatge de programació orientat a la composició algorísmica. Amb JSBach s'utilitzen construccions imperatives per generar composicions que donen lloc a partitures que poden ser desades en diferents formats digitals.

Normalment quan es comença a programar el primer que es fa és fer un petit codi que escriu per pantalla el missatge `Hello World` . En aquesta pràctica el primer programa que hem analitzat ha sigut l'anomenat *Hallo Bach*, dividit en dues instruccions. 

```
~~~ Kleines Program in JSBach ~~~

Main |:
    <!> "Hallo Bach"
    <:> {B A C}
:|
```
La primera instrucció del programa `<!> "Hallo Bach"` és una instrucció d'escriptura (*write*). La segona instrucció del programa `<:> {B A C}` és una instrucció de reproducció (*play*). Aquesta instrucció és molt important perquè afegeix la nota o la llista de notes donades a la partitura.  

## Gràmatica


## Intèrpret

En aquesta secció parlaré dels aspectes més importants  relacionats amb el desenvolupament de l'intèrpret en el fitxer `jsbach.py`. 

Primerament, hi ha definit el mètode `main()` que llegeix l'entrada en funció dels paràmetres que es passen. Si es passa més d'un es llegeix el fitxer com a segon paràmetre i s'interpeta, en cas contrari es llegeix des de la terminal.

En relació amb els visitadors, he afegit un visitador anomenat `EvalVisitor`, el qual hereda del visitor `jsbachVisitor`. Aquest últim s'ha generat després d'executar la següent comanda per terminal:

```bash 
antlr4 -Dlanguage=Python3 -no-listener -visitor jsbach.g4
```
Això permet compilar la gràmatica i generar els fitxers:
- `jsbachLexer.py` i `jsbachLexer.tokens` 
- `jsbachParser.py` i `jsbach.tokens`
 
A més de generar la plantilla del visitor mencionat anteriorment: `jsbachVisitor.py`.

Una vegada entrem dins del visitador, tenim la constructora que inicialitza les diferents estructures de dades. (EXPLICAR EN DETALLE CUANDO SE ACABE)

A continuació, tenim el mètode `visitRoot(self,ctx)`. La seva funció principal és visitar tots els fills i guardar totes les dades de les funcions, ja que a l'arrel de la gramàtica tenim amb màxima prioritat les declaracions de funcions (JSBach és procedural). 

Seguidament, es comprova si està definida la funció `Main` al programa en JSBach, si està declarada es visita directament el seu codi i, en cas de que no estigués definida, es llençaria una excepció.


## Invocació de l'intèrpret

Per invocar l'intèrpret es fa amb la comanda `python3 jsbach.py` tot
passant-li com a paràmetre el nom del fitxer que conté el codi font
(l'extensió dels fitxers per programes en JSBach és `.jsb`). Per exemple:

```bash
python3 jsbach.py musica.jsb
```

Si es vol començar des d'un procediment diferent del `Main`, es pot donar el seu nom com a paràmetre. Per exemple:

```bash
python3 jsbach.py musica.jsb Hanoi
```

Si el programa s'executa correctament, es generaran els fitxers
`musica.pdf` amb la partitura en format PDF,
`musica.midi` amb la música en format MIDI,
`musica.wav` amb la música en format WAV,
i
`musica.mp3` amb la música en format MP3.



# Lliurament

Els diferents fitxers que conformen la versió final de la pràctica són:

- Un fitxer `README.md` que documenta el projecte.

- Un fitxer `jsbach.g4` amb la gramàtica del LP.

- Un fitxer `jsbach.py` amb el programa de l'intèrpret que inclou els corresponents visitadors.



# Referències

- ANTLR en Python: https://gebakx.github.io/Python3/compiladors.html#1

- Lilypond: https://lilypond.org

- Timidity++: https://en.wikipedia.org/wiki/TiMidity%2B%2B

- ffmpeg: https://www.ffmpeg.org/

- Comunicació amb processos: https://recursospython.com/guias-y-manuales/subprocess-creacion-y-comunicacion-con-procesos/