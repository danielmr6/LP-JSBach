import sys
import shlex
import subprocess
from os import remove
from antlr4 import *
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser

if __name__ is not None and "." in __name__:
    from .jsbachParser import jsbachParser
    from .jsbachVisitor import jsbachVisitor
else:
    from jsbachParser import jsbachParser
    from jsbachVisitor import jsbachVisitor

'''
Classe Notes.

Aquesta clase representa les diferents notes possibles que poden aparèixer a un programa en JSBach. El seu comportament principal
és assegurar que tots els valors siguin els que toquin i permetre obtenir el valor enter donada una nota, i viceversa. A més,
la classe Notes s'encarrega de canviar el format de les notes que ve donat en el codi a notes en format lily, amb l'objectiu de
poder generar els fitxers '*.lily', '*.wav', '*.midi' i, finalment, la partitura definitiva en pdf i la peça musical en format '.mp3'.
'''


class Notes:
    '''
    Constructora de la classe Notes.

    Es crea el diccionari amb totes les notes possibles des de la octava 0 (amb A0 i B0) fins la 8 (C8). Les claus del diccionari són els noms
    de les notes i els valors són el nombre enter que representa la nota corresponent. Totes les notes que apareixin al programa sense número
    són sinònims de C4 (Do central), D4, E4, F4, G4, A4, B4.
    '''

    def __init__(self):
        self.__notes = {
            'A0': 1, 'B0': 2,
            'C1': 3, 'D1': 4, 'E1': 5, 'F1': 6, 'G1': 7, 'A1': 8, 'B1': 9,
            'C2': 10, 'D2': 11, 'E2': 12, 'F2': 13, 'G2': 14, 'A2': 15, 'B2': 16,
            'C3': 17, 'D3': 18, 'E3': 19, 'F3': 20, 'G3': 21, 'A3': 22, 'B3': 23,
            'C4': 24, 'D4': 25, 'E4': 26, 'F4': 27, 'G4': 28, 'A4': 29, 'B4': 30,
            'C5': 31, 'D5': 32, 'E5': 33, 'F5': 34, 'G5': 35, 'A5': 36, 'B5': 37,
            'C6': 38, 'D6': 39, 'E6': 40, 'F6': 41, 'G6': 42, 'A6': 43, 'B6': 44,
            'C7': 45, 'D7': 46, 'E7': 47, 'F7': 48, 'G7': 49, 'A7': 50, 'B7': 51,
            'C8': 52}

    '''
    Mètode: isNoteValid(self, note: str)

    Paràmetres:
        note : str -> Valor com a string que pot arribar a ser una nota vàlida (o no).

    Retorna: Bool

    Comportament:
        Retorna cert si el valor de note està dins de la llista de noms de les notes.
        En cas contrari, retorna fals.

    '''

    def isNoteValid(self, note: str):
        return (note in self.__notes.keys())

    '''
    Mètode: getInt(self, note: str)

    Paràmetres:
        note : str -> Valor com a string que pot arribar a ser una nota vàlida (o no).

    Retorna: Int

    Comportament:
        Retorna el valor enter associat a la nota que es passa com a paràmetre si és una nota vàlida.
        En cas contrari, retorna una excepció.

    '''

    def getInt(self, note: str):
        if self.isNoteValid(note):
            return self.__notes[note]
        else:
            raise Exception('La nota ' + note + ' no és vàlida')

    '''
    Mètode: getNote(self, num: int)

    Paràmetres:
        num : int -> Valor enter que està dins del rang de nombres que poden representar una nota.

    Retorna: Int

    Comportament:
        Retorna la nota associada al número quan es troba que el nombre passat com a paràmetre coincideix amb un dels valors que estan al diccionari.
        Si no troba cap nombre coincident, retorna None.
    '''

    def getNote(self, num: int):
        for key in self.__notes.keys():
            if self.__notes[key] == num:
                return key
        return None

    '''
    Mètode: rangAccepted(self, num: int)

    Paràmetres:
        num : int -> Valor enter que pot estar (o no) dins del rang de valors acceptats per representar una nota.

    Retorna: Bool

    Comportament:
        Retorna cert si el nombre està dins del rang de valors vàlids per representar una nota.
        En cas contrari, retorna fals.
    '''

    def rangAccepted(self, num: int):
        return (num >= 1 and num <= 52)

    '''
    Mètode: changeToLilyFormat(self, note: str)

    Pre:
        Totes les notes que es passen com a paràmetre  tenen el nombre que diu en quina octava està.

    Paràmetres:
        note : str -> Valor passat com a string que representa una nota vàlida dins del diccionari.

    Retorna: Str

    Comportament:
       Retorna la nota passada com a paràmetre, però en format lily, és a dir, les lletres en minúscules i
       depenent de quina octava sigui, s'afegeixen comes en cas de ser les octaves més greus o apòstrofs en
       cas de ser les més agudes.
    '''

    def changeToLilyFormat(self, note: str):
        octave = {'0': ",,,", '1': ",,", '2': ",",
                  '3': "", '4': "'", '5': "''", '6': "'''",
                  '7': "''''", '8': "'''''"}

        return (note[0].lower() + octave[note[1]])


'''
Classe Heap.

Aquesta clase representa la pila que emmagatzema tota la informació relacionada amb les funcions i les seves variables locals
amb els seus valors corresponents en temps d'execució. La funció principal d'aquesta classe és validar si una variable està
emmagatzemada en memòria o no a la corresponent taula de simbols, i permetre al programador obtenir tota la informació de la
funció que s'està executant. A més a  més, pel fet de ser una pila, permet insertar un element al principi de la pila i eliminar
aquest (l'element que està al top).
'''


class Heap:

    '''
    Constructora de la classe Heap.

    Es crea la pila inicialitzant-la com una llista buida. L'estructura seria la següent:

    self.__stack = [Diccionari de la funció actual, Diccionari amb informació d'una altra funció, ...]

    La definició del diccionari que guarda totes les dades relacionades amb les funcions es presenta una mica més endavant.
    '''

    def __init__(self):
        self.__stack = list()

    '''
    Mètode: existsInTs(self, word: str)

    Pre:
        La pila no està buida.

    Paràmetres:
        word : str -> Valor passat com a string que representa el nom d'una possible variable o paràmetre de la funció.

    Retorna: Bool

    Comportament:
       Retorna cert en cas d'estar el string word dins de la taula de símbols de la funció corresponent.
       En cas contrari, retorna fals.
    '''

    def existsInTs(self, word: str):
        return (word in self.__stack[0]['ts'].keys())

    '''
    Mètode: getInfoFunc(self)

    Pre:
        La pila no està buida.

    Paràmetres:
        Cap.

    Retorna: Dict

    Comportament:
       Retorna tota la informació de la funció que està en execució en aquell moment. Concretament la informació és:
       {
           'nom' : nomFuncio,
           'parametres' : llista amb els noms,
           'codi' : bloc de codi
           'ts' : { 'nomVariable' : valor , ... }
       }
       La taula de símbols 'ts' guarda totes les dades de les variables locals i dels paràmetres de la funció.
    '''

    def getInfoFunc(self):
        return self.__stack[0]

    '''
    Mètode: removeTop(self)

    Pre:
        La pila no està buida.

    Paràmetres:
        Cap.

    Retorna: Dict

    Comportament:
       Elimina el primer element de la pila i el retorna.
    '''

    def removeTop(self):
        return self.__stack.pop(0)

    '''
    Mètode: insertTop(self, dic : dict)

    Paràmetres:
        dic : dict -> Diccionari que guarda la informació d'una funció del programa.

    Retorna: Dict

    Comportament:
       Inserta el diccionari com a primer element de la pila.
    '''

    def insertTop(self, dic: dict):
        self.__stack.insert(0, dic)

    '''
    Mètode: isEmpty(self)


    Paràmetres:
        Cap.

    Retorna: Bool

    Comportament:
       Retorna cert si la pila és buida, en cas contrari retorna fals.
    '''

    def isEmpty(self):
        return self.__stack == []


class EvalVisitor(jsbachVisitor):
    '''
    Constructora del visitador EvalVisitor.
    El primer paràmetre defineix el nom de la funció inicial que es vol executar en començar el programa, i el segon paràmetre
    és la llista de paràmetres de la funció corresponent (si en té). Si no es passa cap nom, per defecte el programa començarà per la funció Main.
    S'inicialitzen els atributs stack  i notes, el primer serà la pila que gestionarà la informació i el segon serà important per controlar
    tota la part rellevant amb les notes.
    '''

    def __init__(self, nameFuncIni: str, parameters: list):
        self.stack = Heap()
        self.notes = Notes()
        if nameFuncIni is not None and nameFuncIni != 'Main':
            self.nameFuncInit = nameFuncIni
            self.parametersIni = parameters
        else:
            self.nameFuncInit = 'Main'
            self.parametersIni = []
        '''
        dataFunc =
        {
        'Main' : {
                   'nom' = Main
                   'parametres' : llista amb els noms dels paràmetres,
                   'codi' : bloc de codi,
                   'ts' : { 'nomVariable' : valor , ...}
                }
        ...
        }
        Fem un diccionari tenint com a clau el nom de la funcio i com a valor un altre diccionari més intern
        que conté com a clau el camp 'nom', amb el seu respectiu nom de la funció, el camp 'parametres', on es
        guarden els diferents noms, el camp 'codi' on es guarda la referència per visitar el codi de la funció
        i el camp 'ts', el qual guarda tota la informació relacionada amb les variables, els paràmetres i els
        seus valors corresponents.
        '''
        self.dataFunc = {}

        '''
        La partitura que es genera al final de l'execució del programa és una llista que conté totes les notes
        musicals vàlides que s'afegeixin al llarg de tot el codi.
        '''
        self.sheetMusic = []

    '''
    Mètode: visitRoot(self,ctx)

    Retorna:
        Retorna una llista que és la partitura amb les notes del programa interpretat.

    Comportament:

    La seva funció principal és visitar tots els fills i guardar totes les dades de les funcions,
    ja que a l'arrel de la gramàtica tenim amb màxima prioritat les declaracions de funcions (JSBach és procedural).
    Seguidament, es comprova quina és la funció que ha de començar.
        -Si ha de ser el Main, comprova si està definida al programa en JSBach, en cas de que no estigués definida,
        es llença una excepció.
        -Si s'ha de començar per una altra funció que no és el Main, es comprova
        que estigui definit el mètode i que el nombre de paràmetres sigui l'adient,
        en cas de fallar alguna de les dues coses es llença l'excepció.
    Si tot és correcte es guarda tota la informació de la funció a la pila des d'una còpia del diccionari, es visita el codi
    i després fa un remove del top de la pila.
    Finalment, retorna la partitura amb les notes.
    '''

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        for i in range(0, n):
            self.visit(l[i])

        if self.nameFuncInit == 'Main':
            if 'Main' in self.dataFunc.keys():
                copy_dict = self.dataFunc['Main']
                self.stack.insertTop(copy_dict)
                self.visit(self.dataFunc['Main']['codi'])
                self.stack.removeTop()
            else:
                raise Exception('No està definida la funció Main()')
        else:
            if self.nameFuncInit in self.dataFunc.keys():
                nParams = len(self.dataFunc[self.nameFuncInit]['parametres'])
                if len(self.parametersIni) == nParams:
                    new_dic = {'nom': self.nameFuncInit,
                               'parametres': self.dataFunc[self.nameFuncInit]['parametres'].copy(),
                               'ts': self.dataFunc[self.nameFuncInit]['ts'].copy()}
                    self.stack.insertTop(new_dic)
                    self.visit(self.dataFunc[self.nameFuncInit]['codi'])
                    self.stack.removeTop()
                else:
                    raise Exception('El nombre de paràmetres no és correcte')
            else:
                raise Exception(
                    'No està definit el mètode' +
                    self.nameFuncInit)

        return self.sheetMusic

    '''
    Mètode: visitDeclFunc(self, ctx)

    Retorna:
        Res.

    Comportament:
    L'objectiu d'aquest mètode és guardar tota la informació de la funció declarada, concretament
    el nom, els paràmetres, el bloc de codi i la taula de símbols corresponent de la funció. Es
    divideix en dos casos: quan és una funció sense o amb paràmetres. Tota la informació necessària
    es guarda al diccionari dataFunc.
    '''

    def visitDeclFunc(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        if (n == 4):
            nameFunc = l[0].getText()
            posCode = 2
            blockCode = l[posCode]
            self.dataFunc[nameFunc] = {
                'nom': nameFunc,
                'parametres': [],
                'codi': blockCode,
                'ts': {}}
        else:
            nameFunc = l[0].getText()
            parameters = []
            tsAux = {}
            for child in range(1, n - 3):
                parameters.append(l[child].getText())
                tsAux[l[child].getText()] = 0
            posCode = n - 2
            blockCode = l[posCode]
            self.dataFunc[nameFunc] = {
                'nom': nameFunc,
                'parametres': parameters,
                'codi': blockCode,
                'ts': tsAux}

    '''
    Mètode: visitCallFunc(self, ctx)

    Retorna:
        Res.
    Comportament:
    L'objectiu d'aquest mètode és assegurar-se que la funció està definida i es crida bé,
    i a partir d'aquí es fa una còpia del diccionari de la funció, i en la còpia s'actualitzen
    els paràmetres amb els seus valors a la taula de símbols. Una vegada està tot, insertem
    la còpia del diccionari  a la pila, visitem el codi i eliminem la còpia afegida, és a dir,
    fem un pop del primer element.
    '''

    def visitCallFunc(self, ctx):
        l = list(ctx.getChildren())
        nParams = len(l) - 1
        name_func = l[0].getText()
        new_dic = {
            'nom': name_func,
            'parametres': list(
                self.dataFunc[name_func]['parametres']),
            'codi': self.dataFunc[name_func]['codi'],
            'ts': self.dataFunc[name_func]['ts'].copy()}

        if name_func in self.dataFunc.keys():
            nParams_saved = len(self.dataFunc[name_func]['parametres'])
            if nParams == nParams_saved:
                for i in range(0, nParams_saved):
                    value_param = self.visit(l[i + 1])
                    nomPar = new_dic['parametres'][i]
                    new_dic['ts'][nomPar] = value_param
                self.stack.insertTop(new_dic)
                self.visit(new_dic['codi'])
                self.stack.removeTop()
            else:
                raise Exception(
                    'Crida al mètode ' +
                    name_func +
                    ' amb nombre de paràmetres incorrecte')

        else:
            raise Exception('Crida a procediment no definit')

    '''
    Mètode: visitReadStmt(self, ctx)

    Retorna:
        Res.
    Comportament:
    L'objectiu d'aquest mètode és llegir la informació que ve donada per la entrada i
    assignar-la a la variable que té com a nom el que s'indica al fer la lectura.
    '''

    def visitReadStmt(self, ctx):
        l = list(ctx.getChildren())
        info = input()
        key = l[1].getText()
        self.stack.getInfoFunc()['ts'][key] = int(info)

    '''
    Mètode: visitWriteStmt(self, ctx)

    Retorna:
        Res.
    Comportament:
    La funció principal d'aquesta funció és escriure la informació que ens ve donada
    després del símbol d'escriure. Cal destacar que es fa la distinció entre si el
    valor és un enter, és una llista, és una nota vàlida o, altrament, és una cadena
    de text. Una vegada s'ha acabat de construir el text final, s'imprimeix per
    pantalla.
    '''

    def visitWriteStmt(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        res = ''
        for child in range(1, n):
            value = self.visit(l[child])
            isInteger = isinstance(value, int)
            isList = isinstance(value, list)
            if isInteger:
                res += ' ' + str(value)

            elif isList:
                res += ' ' + '['
                n = len(value)
                for i in range(0, n):
                    if i == n - 1:
                        res += str(value[i])
                    else:
                        res += str(value[i]) + ','
                res += ']'

            elif self.notes.isNoteValid(value):
                res += ' ' + value

            else:
                res += ' ' + l[child].getText()[1:-1]
        print(res)

    '''
    Mètode: visitSentenceIf(self, ctx)

    Retorna:
        Res.
    Comportament:
    L'objectiu d'aquest mètode és comprovar si la condició booleana es certa o no,
    i en cas de ser cert, haurà d'anar al bloc de codi que li correpon. Si no és
    certa la condició, llavors es comprova si hi ha la sentència else, i si existeix,
    visita la seva part del codi, en cas de no existir, ja no es fa res més.
    '''

    def visitSentenceIf(self, ctx):
        l = list(ctx.getChildren())
        condition = self.visitRelExp(l[1])
        if condition:
            self.visit(l[3])
        elif len(l) == 9:
            self.visit(l[7])

    '''
    Mètode: visitAssigs(self, ctx)

    Retorna:
        Res.
    Comportament:
    El comportament que té aquest mètode és assignar a la variable que té el nom
    en key els valors corresponents. Si és una llista, es visita la constructora
    d'una llista, si és un valor unitari es visita l'expressió. A més, s'actualitza
    el valor de la taula de símbols dins de la pila.
    '''

    def visitAssigs(self, ctx):
        l = list(ctx.getChildren())
        key = l[0].getText()
        if self.visit(l[2]) == '{':
            value = self.visitListConst(l[2])
        else:
            value = self.visit(l[2])
        self.stack.getInfoFunc()['ts'][key] = value

    '''
    Mètode: visitSentenceWhile(self, ctx)

    Retorna:
        Res.
    Comportament:
    Aquesta funció el que fa és visitar el bloc de codi que està dins del cos del
    while mentre la condició sigui certa.
    '''

    def visitSentenceWhile(self, ctx):
        l = list(ctx.getChildren())
        while (True):
            condition = self.visitRelExp(l[1])
            if not condition:
                break
            self.visit(l[3])

    '''
    Mètode: visitListConst(self, ctx)

    Retorna: List

    Comportament:
    L'objectiu d'aquest mètode és construir una llista amb els valors
    que estan entre els limitadors. Els possibles valors d'una llista
    són notes o números. Es retorna la llista una vegada s'han afegit
    tots els valors auxiliars.
    '''

    def visitListConst(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        values_aux = []
        if n >= 1:
            if l[1].getSymbol().type == jsbachParser.NUM:
                for i in range(1, n - 1):
                    values_aux.append(self.visitNum(l[i]))
            else:
                for i in range(1, n - 1):
                    values_aux.append(self.visitNote(l[i]))
        return values_aux

    '''
    Mètode: visitListAddStmt(self, ctx)

    Retorna:
        Res.

    Comportament:
    Aquesta funció comprova si existeix una llista a la taula de símbols
    de la pila amb el nom corresponent, si no existeix llença la excepció.
    En cas d'existir la llista, s'afegeix l'element corresponent i a més
    s'afegeix a la pila la nova llista actualitzada dins de la taula de
    símbols.
    '''

    def visitListAddStmt(self, ctx):
        l = list(ctx.getChildren())
        name_list = l[0].getText()
        elem = self.visit(l[2])
        if self.stack.existsInTs(name_list):
            list_info = self.stack.getInfoFunc()['ts'][name_list]
            list_info.append(elem)
            self.stack.getInfoFunc()['ts'][name_list] = list_info
        else:
            raise Exception('No existeix cap llista amb el nom ' + name_list)

    '''
    Mètode: visitListCutStmt(self, ctx)

    Retorna:
        Res.

    Comportament:
    L'objectiu d'aquest mètode és comprovar si l'índex és vàlid i  que la llista amb el nom
    existeix. En cas d'existir i ser l'índex vàlid, elimina l'element i-èsim de la llista
    i s'actualitza a la pila. En cas contrari, es llença l'excepció necessària.
    '''

    def visitListCutStmt(self, ctx):
        l = list(ctx.getChildren())
        index = self.visit(l[3]) - 1
        if index >= 0:
            name_list = l[1].getText()
            if self.stack.existsInTs(name_list):
                list_info = self.stack.getInfoFunc()['ts'][name_list]
                if len(list_info) >= 1 and index <= (len(list_info) - 1):
                    list_info.pop(index)
                    self.stack.getInfoFunc()['ts'][name_list] = list_info
                else:
                    raise Exception(
                        'No existeix el element i-èsim a la llista')
            else:
                raise Exception(
                    'No existeix cap llista amb el nom ' + name_list)
        else:
            raise Exception('Índex erroni: el valor mínim ha de ser 1!')

    '''
    Mètode: visitListSize(self, ctx)

    Retorna: Int

    Comportament:
    Aquesta funció retorna el nombre d'elements de la llista, però primerament es
    comprova si la llista existeix a la taula de símbols, sinò es llença excepció.
    '''

    def visitListSize(self, ctx):
        l = list(ctx.getChildren())
        name_list = l[1].getText()
        if self.stack.existsInTs(name_list):
            return len(self.stack.getInfoFunc()['ts'][name_list])
        else:
            raise Exception('No existeix cap llista amb el nom ' + name_list)

    '''
    Mètode: visitListGet(self, ctx)

    Retorna: Expressió

    Comportament:
    Aquest mètode comprova si existeix la llista a la taula de símbols
    de la funció en la pila i que l'índex és vàlid, si tot està bé es
    retorna l'i-èsim element de la llista, tenint en compte que en JSBach
    comencen per 1 i en Python per 0.
    '''

    def visitListGet(self, ctx):
        l = list(ctx.getChildren())
        index = self.visit(l[2]) - 1
        if index >= 0:
            name_list = l[0].getText()
            if self.stack.existsInTs(name_list):
                list_info = self.stack.getInfoFunc()['ts'][name_list]
                if len(list_info) >= 1 and index <= (len(list_info) - 1):
                    return list_info[index]
                else:
                    raise Exception(
                        'No existeix el element i-èsim a la llista')
            else:
                raise Exception(
                    'No existeix cap llista amb el nom ' + name_list)
        else:
            raise Exception('Índex erroni: el valor mínim ha de ser 1!')

    '''
    Mètode: visitPlayId(self, ctx)

    Retorna:
        Res.

    Comportament:
    Aquesta funció comprova si existeix la variable a la taula de símbols. En
    cas de ser una llista de notes, es comprova que les notes siguin vàlides i
    s'afegeixen a la partitura, sinò es comprova si és un enter i està en el rang acceptat.
    Si és un número vàlid, s'afegeix a la partitura la nota que està associada a aquell valor,
    en cas de no ser vàlid es llença l'excepció.
    '''

    def visitPlayId(self, ctx):
        l = list(ctx.getChildren())
        name_var = l[1].getText()
        if self.stack.existsInTs(name_var):
            list_notes = self.stack.getInfoFunc()['ts'][name_var]
            if isinstance(list_notes, list):
                for i in list_notes:
                    if self.notes.isNoteValid(i):
                        self.sheetMusic.append(i)
                    else:
                        if isinstance(i, int) and self.notes.rangAccepted(i):
                            self.sheetMusic.append(self.notes.getNote(i))
                        else:
                            raise Exception(
                                'El valor no està en un rang vàlid per ser nota')

            else:
                self.sheetMusic.append(list_notes)
        else:
            raise Exception('No existeix la llista amb nom' + name_var)

    '''
    Mètode: visitPlayLists(self, ctx)

    Retorna:
        Res.

    Comportament:
    L'objectiu d'aquest mètode és anar afegint els valors de la llista a la
    partitura per tal d'aconseguir tenir la partitura amb les notes o nombres
    corresponents.
    '''

    def visitPlayLists(self, ctx):
        l = list(ctx.getChildren())
        list_notes = self.visitListConst(l[1])
        for i in list_notes:
            self.sheetMusic.append(i)

    '''
    Mètode: visitRelExp(self, ctx)

    Retorna: Int

    Comportament:
    Aquesta funció avalua els dos operands amb l'operador per tal de retornar
    un valor com a cert (1 o més gran) o fals (0). Si un operand és una nota,
    es passa al valor enter que està associat a aquella nota per fer la
    comprovació.
    '''

    def visitRelExp(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            number = int(l[0].getText())
            if number > 0:
                return 1
            elif number == 0:
                return 0
        else:
            opL = self.visit(l[0])
            opR = self.visit(l[2])
            if self.notes.isNoteValid(opL):
                opL = self.notes.getInt(opL)

            if self.notes.isNoteValid(opR):
                opR = self.notes.getInt(opR)

            type = l[1].getSymbol().type
            if type == jsbachParser.EQ:
                return int(opL == opR)
            elif type == jsbachParser.DIF:
                return int(opL != opR)
            elif type == jsbachParser.LST:
                return int(opL < opR)
            elif type == jsbachParser.GRT:
                return int(opL > opR)
            elif type == jsbachParser.LEQ:
                return int(opL <= opR)
            elif type == jsbachParser.GEQ:
                return int(opL >= opR)
            else:
                raise Exception('Operador ' + type +
                                'no està definit a JSBach')

    '''
    Mètode: visitAddSub(self, ctx)

    Retorna:
        Nombre o Nota.

    Comportament:
    Aquesta funció retorna la suma de dues expressions. En el cas de
    tenir una nota en algun dels dos operands, el que es fa és passar les notes
    al valor enter que representen, s'operen i si el valor resultant és valid,
    es retorna en format de nota. Si no és valid el resultat es llença una
    excepció. Si cap dels operands és una nota, es retorna el valor resultant de
    l'operació suma o resta.
    '''

    def visitAddSub(self, ctx):
        l = list(ctx.getChildren())
        exprL = self.visit(l[0])
        exprR = self.visit(l[2])
        isNoteL = self.notes.isNoteValid(exprL)
        isNoteR = self.notes.isNoteValid(exprR)
        if isNoteL or isNoteR:
            if isNoteL:
                exprL = self.notes.getInt(exprL)
            elif isNoteR:
                exprR = self.notes.getInt(exprR)
            else:
                exprL = self.notes.getInt(exprL)
                exprR = self.notes.getInt(exprR)

            if l[1].getSymbol().type == jsbachParser.SUB:
                result = (exprL - exprR)
                if self.notes.rangAccepted(result):
                    return self.notes.getNote(result)
                else:
                    raise Exception(
                        'El valor de la nota no està en un rang valid')

            elif l[1].getSymbol().type == jsbachParser.ADD:
                result = (exprL + exprR)
                if self.notes.rangAccepted(result):
                    return self.notes.getNote(result)
                else:
                    raise Exception(
                        'El valor de la nota no està en un rang valid')
        else:
            if l[1].getSymbol().type == jsbachParser.SUB:
                return int(exprL - exprR)
            elif l[1].getSymbol().type == jsbachParser.ADD:
                return int(exprL + exprR)

    '''
    Mètode: visitParentesis(self, ctx)

    Retorna:
        Expressió.

    Comportament:
    L'únic que fa aquesta funció és visitar i retornar l'expressió que està
    entre parèntesis.
    '''

    def visitParentesis(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    '''
    Mètode: visitVarId(self, ctx)

    Retorna:
        Expressió.

    Comportament:
    Donat un nom d'una variable, es comprova si existeix a la taula de símbols
    de la pila, si no existeix es llença l'excepció. En el cas d'estar present a
    la taula, es retorna el valor que té la variable amb aquell nom.
    '''

    def visitVarId(self, ctx):
        if self.stack.existsInTs(ctx.getText()):
            var = self.stack.getInfoFunc()['ts'][ctx.getText()]
            return var
        else:
            raise Exception('La variable ' + ctx.getText() +
                            ' no està al diccionari')

    '''
    Mètode: visitNote(self, ctx)

    Retorna:
        String-

    Comportament:
    Aquesta funció comprova si la nota no té la octava explícitament (això vol dir
    que pertany a la quarta). Si no la té, s'afegeix el valor de la quarta octava
    i es retorna el nou string. Si la té, es retorna directament el string-
    '''

    def visitNote(self, ctx: jsbachParser.NoteContext):
        length = len(ctx.getText())
        if length == 1:
            # Si la nota no té la octava explícitament, li afegim el valor de
            # la quarta octava.
            nou_str = ctx.getText() + '4'
            return nou_str
        else:
            return ctx.getText()

    '''
    Mètode: visitNum(self, ctx)

    Retorna:
        Integer.

    Comportament:
    Aquesta funció retorna el número en forma d'enter.
    '''

    def visitNum(self, ctx: jsbachParser.NumContext):
        return int(ctx.getText())

    '''
    Mètode: visitNum(self, ctx)

    Retorna:
        Integer o Nota.

    Comportament:
    Aquesta funció comprova si algun dels operands és una nota. En el cas de
    tenir una nota en algun dels dos operands, el que es fa és passar les notes
    al valor enter que representen, s'operen i si el valor resultant és valid,
    es retorna en format de nota. Si no és valid el resultat es llença una
    excepció. Si cap dels operands és una nota, es retorna el valor resultant de
    l'operació. Quan és una divisió si l'operand de la dreta és un 0 es llença
    l'excepció.
    '''

    def visitDivMulMod(self, ctx):
        l = list(ctx.getChildren())
        exprL = self.visit(l[0])
        exprR = self.visit(l[2])
        isNoteL = self.notes.isNoteValid(exprL)
        isNoteR = self.notes.isNoteValid(exprR)
        if isNoteL or isNoteR:
            if isNoteL:
                exprL = self.notes.getInt(exprL)
            elif isNoteR:
                exprR = self.notes.getInt(exprR)
            else:
                exprL = self.notes.getInt(exprL)
                exprR = self.notes.getInt(exprR)

            if l[1].getSymbol().type == jsbachParser.MUL:
                result = exprL * exprR
                if self.notes.rangAccepted(result):
                    return self.notes.getNote(result)
                else:
                    raise Exception(
                        'El valor de la nota no està en un rang valid')
            elif l[1].getSymbol().type == jsbachParser.DIV:
                if exprR != 0:
                    result = exprL / exprR
                    if self.notes.rangAccepted(result):
                        return self.notes.getNote(result)
                    else:
                        raise Exception(
                            'El valor de la nota no està en un rang valid')
                else:
                    raise Exception('No es pot dividir per zero!')

            elif l[1].getSymbol().type == jsbachParser.MOD:
                result = exprL % exprR
                if self.notes.rangAccepted(result):
                    return self.notes.getNote(result)
                else:
                    raise Exception(
                        'El valor de la nota no està en un rang valid')
        else:
            if l[1].getSymbol().type == jsbachParser.MUL:
                return int(exprL * exprR)
            elif l[1].getSymbol().type == jsbachParser.DIV:
                if exprR.getText() != '0':
                    return int(exprL / exprR)
                else:
                    raise Exception('No es pot dividir per zero!')

            elif l[1].getSymbol().type == jsbachParser.MOD:
                return int(exprL % exprR)


def main():

    # Lectura de l'entrada

    if sys.argv[1].endswith('.jsb'):
        program_name = sys.argv[1].split('.')[0]
        input_stream = FileStream(sys.argv[1], encoding='utf-8')
        if len(sys.argv) == 2:
            visitor = EvalVisitor(None, None)
        elif len(sys.argv) > 2:
            params = []
            nameFuncInit = sys.argv[2]
            for i in range(3, len(sys.argv)):
                params.append(sys.argv[i])
            visitor = EvalVisitor(nameFuncInit, params)
    else:
        raise Exception('El fitxer no és un programa en JSBach')

    lexer = jsbachLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = jsbachParser(token_stream)
    tree = parser.root()
    # Aquest print escriu per terminal l'arbre de sintaxi abstracta i ha sigut
    # de molta ajuda per dur a terme la pràctica.

    # print(tree.toStringTree(recog=parser))

    # Obtenció de la llista de notes de la partitura
    notes = visitor.visit(tree)

    # Generació de fitxers

    cjt_notes = Notes()
    generator_file = open('generador.lily', 'r')
    start = ''
    for line in generator_file:
        start = start + '\n' + line

    lilyFile = open(program_name + '.lily', 'a')
    lilyFile.write(start + '\n')

    for note in notes:
        lilyFile.write("%s " % cjt_notes.changeToLilyFormat(note))

    lilyFile.write("\n }\n")
    lilyFile.write(" \\layout {" "}\n")
    lilyFile.write(" \\midi { " "}\n")
    lilyFile.write("}")
    lilyFile.close()

    # Generem l'arxiu program_name.wav i program_name.midi
    subprocess.call(shlex.split('lilypond ' + program_name + '.lily'))
    # Generem l'arxiu program_name.pdf
    subprocess.call(shlex.split('timidity -Ow -o ' + program_name + '.wav ' + program_name + '.midi'))
    # Generem l'arxiu program_name.mp3
    subprocess.call(shlex.split('ffmpeg -i ' + program_name + '.wav -codec:a libmp3lame -qscale:a 2 ' + program_name + '.mp3'))

    remove(program_name + '.lily')
    remove(program_name + '.midi')
    remove(program_name + '.wav')


if __name__ == '__main__':
    main()
