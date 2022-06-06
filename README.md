# El doble intèrpret de JSBach

Aquesta pàgina descriu la pràctica de GEI-LP (edició 2021-2022 Q2). La meva tasca ha sigut implementar un doble intèrpret per a un llenguatge de programació musical anomenat JSBach. La sortida d'aquest doble intèrpret és una partitura i uns fitxers de so que reproduiran la melodia descrita pel compositor.

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

Al fitxer `jsbach.g4` està inclosa tota la gramàtica relacionada amb JSBach i els comentaris de cada apartat. Tot i que el fitxer conté diferents explicacions comentant que és cada cosa, és important aclarir diferents temes:
- Els noms de les funcions han de començar sí o sí per una lletra majúscula. A més, han de tenir un altre caràcter com a mínim per poder donar un nom més representatiu a la funció.
- Al ser un llenguate procedural, l'arrel de la gramàtica és la declaració de funcions, ja que en el codi tot conjunt d'instruccions ha d'estar dins d'una funció.
- Dintre d'una cadena de text, he permès que es pugui introduir qualsevol caràcter o símbol excepte els següents:
  - `'\n'`: Salt de línia.
  - `'\r'`: Un return.
  - `'\t'`: Una tabulació de 4 espais.
  - `'"'` : Evitem que es pugui ficar dins d'una cadena perquè sino donaria errors pel fet de tancar i obrir les cadenes de manera irregular.
- Les expressions booleanes sempre retornen un número. Si és 0, el seu significat és fals, i en cas de ser més gran a 0, el significat del valor resultant de la expressió serà cert.
- He pensat que era més adient separar les expressions normals de les expressions sobre llistes per tenir una idea més clara de que era cada cosa.

## Intèrpret

En aquesta secció parlaré dels aspectes més importants  relacionats amb el desenvolupament de l'intèrpret en el fitxer `jsbach.py`. 

Primerament, hi ha definit el mètode `main()` que llegeix l'entrada en funció dels paràmetres que es passen:

- Un argument: Es llegeix el fitxer i es comprova la seva extensió sigui '.jsb'. A partir d'aquí, s'interpeta el programa. Començarà per defecte pel mètode Main del programa, en cas de no haver Main es llençarà l'excepció.
- Dos arguments: El primer és el programa. I en aquest segon cas, el segon argument ha de ser el nom de la funció per la qual es vol començar a executar i no ha de tenir paràmetres.
- Més de dos arguments: El segon argument ha de ser el nom de la funció per la qual es vol començar a executar i la resta són els valors dels paràmetres de la funció.

En relació amb els visitadors, he afegit un visitador anomenat `EvalVisitor`, el qual hereda del visitor `jsbachVisitor`. Aquest últim s'ha generat després d'executar la següent comanda per terminal:

```bash 
antlr4 -Dlanguage=Python3 -no-listener -visitor jsbach.g4
```
Això permet compilar la gràmatica i generar els fitxers:
- `jsbachLexer.py` i `jsbachLexer.tokens` 
- `jsbachParser.py` i `jsbach.tokens`
 
A més de generar la plantilla del visitor mencionat anteriorment: `jsbachVisitor.py`.

Una vegada entrem dins del visitador, tenim la constructora que inicialitza les diferents estructures de dades. Com el fitxer ja té els diferents comentaris que documenten el programa, aquí només vull destacar  els aspectes a tenir en compte del meu intèrpret:
- Es poden reproduir `<:>` (play) llistes d'enters, sempre i quan els valors d'aquests estiguin dins del rang de les notes (entre 1 i 52).
- Quan es fan operacions amb notes, sempre es comprova que el valor resultant estigui dins del rang acceptable, en cas de no estar es llença una excepció.


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

- pep8: https://peps.python.org/pep-0008/

- Comunicació amb processos: https://recursospython.com/guias-y-manuales/subprocess-creacion-y-comunicacion-con-procesos/