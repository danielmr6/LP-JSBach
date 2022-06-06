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
        self.__notes = { 'A0' : 1 , 'B0' : 2, 
                        'C1' : 3 , 'D1' : 4, 'E1' : 5, 'F1' : 6, 'G1' : 7, 'A1': 8, 'B1' : 9,
                        'C2' : 10 , 'D2' : 11, 'E2' : 12, 'F2' : 13, 'G2' : 14, 'A2': 15, 'B2' : 16,
                        'C3' : 17 , 'D3' : 18, 'E3' : 19, 'F3' : 20, 'G3' : 21, 'A3': 22, 'B3' : 23,
                        'C4' : 24 , 'D4' : 25, 'E4' : 26, 'F4' : 27, 'G4' : 28, 'A4': 29, 'B4' : 30,
                        'C5' : 31 , 'D5' : 32, 'E5' : 33, 'F5' : 34, 'G5' : 35, 'A5': 36, 'B5' : 37,
                        'C6' : 38 , 'D6' : 39, 'E6' : 40, 'F6' : 41, 'G6' : 42, 'A6': 43, 'B6' : 44,
                        'C7' : 45 , 'D7' : 46, 'E7' : 47, 'F7' : 48, 'G7' : 49, 'A7': 50, 'B7' : 51,
                        'C8' : 52 }
        
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
        octave = {'0' : ",,," , '1' : ",," , '2' : "," , 
                  '3' :  "", '4' : "'" , '5' : "''" , '6' : "'''" , 
                  '7' : "''''" , '8' : "'''''" }

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
    def existsInTs(self, word:str):
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
    def insertTop(self, dic : dict):
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
        if nameFuncIni != None and nameFuncIni != 'Main':
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
                        new_dic = {'nom' : self.nameFuncInit, 'parametres' : self.dataFunc[self.nameFuncInit]['parametres'].copy(), 
                                   'ts' : self.dataFunc[self.nameFuncInit]['ts'].copy()}
                        self.stack.insertTop(new_dic)
                        self.visit(self.dataFunc[self.nameFuncInit]['codi'])
                        self.stack.removeTop()
                    else:
                        raise Exception('El nombre de paràmetres no és correcte')
                else:
                    raise Exception('No està definit el mètode' + self.nameFuncInit)
    
        return self.sheetMusic

    def visitDeclFunc(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        if (n == 4):
            nameFunc = l[0].getText()
            posCode = 2
            blockCode = l[posCode]
            self.dataFunc[nameFunc] = {'nom' : nameFunc, 'parametres': [], 'codi': blockCode, 'ts' : {}}
        else:
            nameFunc = l[0].getText()
            parameters = []
            tsAux = {}
            for child in range(1, n-3):
                    parameters.append(l[child].getText())
                    tsAux[l[child].getText()] = 0
            posCode = n-2
            blockCode = l[posCode]
            self.dataFunc[nameFunc] = {'nom' : nameFunc, 'parametres' : parameters, 'codi' : blockCode, 'ts' : tsAux}
           
    def visitCallFunc(self, ctx):
        l = list(ctx.getChildren())
        nParams = len(l)-1
        name_func = l[0].getText()
        new_dic = {'nom' : name_func, 'parametres' : list(self.dataFunc[name_func]['parametres']), 
                   'codi' : self.dataFunc[name_func]['codi'], 'ts': self.dataFunc[name_func]['ts'].copy()}

        if name_func in self.dataFunc.keys():
            nParams_saved = len(self.dataFunc[name_func]['parametres'])
            if nParams == nParams_saved:
                for i in range(0, nParams_saved):
                    value_param = self.visit(l[i+1])
                    nomPar = new_dic['parametres'][i]
                    new_dic['ts'][nomPar] = value_param
                self.stack.insertTop(new_dic)
                self.visit(new_dic['codi'])
                self.stack.removeTop()                
            else:
                raise Exception('Crida al mètode ' + name_func + ' amb nombre de paràmetres incorrecte')
            
        else:
            raise Exception('Crida a procediment no definit')

    def visitReadStmt(self, ctx):
        l = list(ctx.getChildren())
        info = input()
        key = l[1].getText()
        self.stack.getInfoFunc()['ts'][key] = int(info)
        

    def visitWriteStmt(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        res = ''
        for child in range(1,n):
            value = self.visit(l[child])
            isInteger = isinstance(value, int)
            isList = isinstance(value, list)
            if isInteger:
                if value >= 0:
                    res += ' ' + str(value)       
                    
            elif isList:
                res += ' ' + '['
                n = len(value)
                for i in range(0,n):
                    if i == n-1:
                        res += str(value[i])
                    else:
                        res += str(value[i]) + ','
                res += ']'
                
            elif  self.notes.isNoteValid(value):
                res += ' ' +  value
                
            else: 
                res += ' ' + l[child].getText()[1:-1]
        print(res)

    def visitSentenceIf(self, ctx):
        l = list(ctx.getChildren())
        condition = self.visitRelExp(l[1])
        if condition:
            return self.visit(l[3])
        elif len(l) == 9:
            return self.visit(l[7])

    def visitAssigs(self, ctx):
        l = list(ctx.getChildren())
        key = l[0].getText()
        if self.visit(l[2]) == '{':
            value = self.visitListConst(l[2])
        else:
            value = self.visit(l[2])
            
        self.stack.getInfoFunc()['ts'][key] = value
        return value

    def visitSentenceWhile(self, ctx):
        l = list(ctx.getChildren())
        while (True):
            condition = self.visitRelExp(l[1])
            if not condition:
                break
            self.visit(l[3])

    def visitListConst(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        values_aux = []
        if n >= 1:
            if l[1].getSymbol().type == jsbachParser.NUM:
                for i in range(1, n-1):
                    values_aux.append(self.visitNum(l[i]))
            else:
                for i in range(1, n-1):
                    values_aux.append(self.visitNote(l[i]))
        return values_aux

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
            
        
    def visitListCutStmt(self, ctx):
        l = list(ctx.getChildren())
        index = self.visit(l[3])-1
        if index >= 0:
            name_list = l[1].getText()
            if self.stack.existsInTs(name_list):
                list_info = self.stack.getInfoFunc()['ts'][name_list]
                if len(list_info) >= 1 and index <= (len(list_info)-1):
                    list_info.pop(index)
                    self.stack.getInfoFunc()['ts'][name_list] = list_info
                else:
                    raise Exception('No existeix el element i-èsim a la llista')
            else:
                raise Exception('No existeix cap llista amb el nom ' + name_list)
        else:
            raise Exception('Índex erroni: el valor mínim ha de ser 1!')
        
            

    def visitListSize(self, ctx):
        l = list(ctx.getChildren())
        name_list = l[1].getText()
        if self.stack.existsInTs(name_list):
            return len(self.stack.getInfoFunc()['ts'][name_list])
        else:
            raise Exception('No existeix cap llista amb el nom ' + name_list)
        
    def visitListGet(self, ctx):
        l = list(ctx.getChildren())
        index = self.visit(l[2])-1
        if index >= 0:
            name_list = l[0].getText()
            if self.stack.existsInTs(name_list):
                list_info = self.stack.getInfoFunc()['ts'][name_list]
                if len(list_info) >= 1 and index <= (len(list_info)-1):
                    return list_info[index]
                else:
                    raise Exception('No existeix el element i-èsim a la llista')
            else:
                raise Exception('No existeix cap llista amb el nom ' + name_list)  
        else:
            raise Exception('Índex erroni: el valor mínim ha de ser 1!')
        
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
                            raise Exception('El valor no està en un rang vàlid per ser nota')
                            
            else:   
                self.sheetMusic.append(list_notes)
        else:
            raise Exception('No existeix la llista amb nom' + name_var)
        
    def visitPlayLists(self, ctx):
        l = list(ctx.getChildren())
        list_notes = self.visitListConst(l[1])
        for i in list_notes:
            self.sheetMusic.append(i)
        
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
                result = (exprL-exprR)
                if self.notes.rangAccepted(result):
                    return self.notes.getNote(result)
                else:
                    raise Exception('El valor de la nota no està en un rang valid')
                
            elif l[1].getSymbol().type == jsbachParser.ADD:
                result = (exprL+exprR)
                if self.notes.rangAccepted(result):
                    return self.notes.getNote(result)
                else:
                    raise Exception('El valor de la nota no està en un rang valid')
        else:
            if l[1].getSymbol().type == jsbachParser.SUB:
                return int(exprL - exprR)
            elif l[1].getSymbol().type == jsbachParser.ADD:
                return int(exprL + exprR)

    def visitParentesis(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    def visitVarId(self, ctx):
        if self.stack.existsInTs(ctx.getText()):
            var = self.stack.getInfoFunc()['ts'][ctx.getText()]
            return var
        else:
            raise Exception('La variable ' + ctx.getText() +
                            ' no està al diccionari')

    def visitNote(self, ctx: jsbachParser.NoteContext):
        length = len(ctx.getText())
        if length == 1: 
            #Si la nota no té la octava explícitament, li afegim el valor de la quarta octava.
            nou_str = ctx.getText() + '4'
            return nou_str
        else:
            return ctx.getText()

    def visitNum(self, ctx: jsbachParser.NumContext):
        return int(ctx.getText())

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
                    raise Exception('El valor de la nota no està en un rang valid')
            elif l[1].getSymbol().type == jsbachParser.DIV:
                if exprR != 0:
                    result = exprL / exprR
                    if self.notes.rangAccepted(result):
                        return self.notes.getNote(result)
                    else:
                        raise Exception('El valor de la nota no està en un rang valid')
                else:
                    raise Exception('No es pot dividir per zero!')
                
            elif l[1].getSymbol().type == jsbachParser.MOD:
                result = exprL % exprR
                if self.notes.rangAccepted(result):
                    return self.notes.getNote(result)
                else:
                    raise Exception('El valor de la nota no està en un rang valid')
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
    print(tree.toStringTree(recog=parser))

    notes = visitor.visit(tree)


    cjtnotes = Notes()
    generator_file = open('generador.lily', 'r')
    start = ''
    for line in generator_file:
        start = start + '\n' + line
        
    lilyFile = open(program_name + '.lily', 'a')
    lilyFile.write(start + '\n')

    
    for note in notes:
        lilyFile.write("%s " % cjtnotes.changeToLilyFormat(note))

    lilyFile.write("\n }\n")
    lilyFile.write(" \layout {" "}\n")
    lilyFile.write(" \midi { " "}\n")
    lilyFile.write("}")
    lilyFile.close()
 

    subprocess.call(shlex.split('lilypond ' + program_name + '.lily'))
    subprocess.call(shlex.split('timidity -Ow -o ' + program_name + '.wav ' + program_name + '.midi'))
    subprocess.call(shlex.split('ffmpeg -i ' + program_name + '.wav -codec:a libmp3lame -qscale:a 2 ' + program_name + '.mp3'))


    remove(program_name + '.lily')
    remove(program_name + '.midi')
    remove(program_name + '.wav')
    
    
if __name__ == '__main__':
    main()
