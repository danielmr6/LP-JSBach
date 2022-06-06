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
        
    def isNoteValid(self, note: str):
        return (note in self.__notes.keys())
    
    def getInt(self, note: str):
        if self.isNoteValid(note):
            return self.__notes[note]
        else:
            raise Exception('La nota ' + note + ' no és vàlida')
        
    def getNote(self, num: int):
        for key in self.__notes.keys():
            if self.__notes[key] == num:
                return key
        return None
    
    def rangAccepted(self, num: int):
        return (num >= 1 and num <= 52)
    
    def changeFormat(self, note: str):
        octava = {'0' : ",,," , '1' : ",," , '2' : "," , 
                  '3' :  "", '4' : "'" , '5' : "''" , '6' : "'''" , 
                  '7' : "''''" , '8' : "'''''" }

        return (note[0].lower() + octava[note[1]])



class Heap:
    
    def __init__(self):
        self.__stack = list()  
        self.__nomFuncio = ''
        
    def getNameFunc(self):
        self.__nomFuncio = self.__stack[0]['nom']
        return self.__nomFuncio
    
    def existsInTs(self, word:str):
        return (word in self.__stack[0]['ts'].keys())

    def getInfoFunc(self):
        return self.__stack[0]
        
    def removeTop(self):
        return self.__stack.pop(0)
    
    def insertTop(self, dic : dict):
        self.__stack.insert(0, dic)
        
    def isEmpty(self):
        return self.__stack == []
    
    



class EvalVisitor(jsbachVisitor):
    '''
    Constuctora del visitador EvalVisitor. 
    El primer paràmetre defineix el nom de la funció inicial que es vol executar en començar el programa, i el segon paràmetre
    és la llista de paràmetres de la funció corresponent (si en té). Si no es passa cap nom, per defecte el programa començarà per la funció Main.
    '''

    def __init__(self, nomFuncioIni: str, parametres: list):
        self.stack = Heap()
        self.notes = Notes()
        if nomFuncioIni != None and nomFuncioIni != 'Main':
            self.nomFuncioInicial = nomFuncioIni
            self.parametresIni = parametres
        else:
            self.nomFuncioInicial = 'Main'
            self.parametresIni = []
        '''
        dadesFunc = 
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
        self.dadesFunc = {}
        
        '''
        La partitura que es genera al final de l'execució del programa és una llista que conté totes les notes 
        musicals vàlides que s'afegeixin al llarg de tot el codi.
        '''
        self.partitura = []

  
    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        for i in range(0, n):
            self.visit(l[i])
        
        if self.nomFuncioInicial == 'Main':
            if 'Main' in self.dadesFunc.keys():
                copiaDic = self.dadesFunc['Main']
                self.stack.insertTop(copiaDic)
                self.visit(self.dadesFunc['Main']['codi'])
                self.stack.removeTop()
            else:
                raise Exception('No està definida la funció Main()')
        else:
                if self.nomFuncioInicial in self.dadesFunc.keys():
                    nParams = len(self.dadesFunc[self.nomFuncioInicial]['parametres'])
                    if len(self.parametresIni) == nParams:
                        nou_dic = {'nom' : self.nomFuncioInicial, 'parametres' : self.dadesFunc[self.nomFuncioInicial]['parametres'].copy(), 
                                   'ts' : self.dadesFunc[self.nomFuncioInicial]['ts'].copy()}
                        self.stack.insertTop(nou_dic)
                        self.visit(self.dadesFunc[self.nomFuncioInicial]['codi'])
                        self.stack.removeTop()
                    else:
                        raise Exception('El nombre de paràmetres no és correcte')
                else:
                    raise Exception('No està definit el mètode' + self.nomFuncioInicial)
    
        return self.partitura

    def visitDeclFunc(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        if (len(l) == 4):
            nomFunc = l[0].getText()
            posCodi = 2
            blocCodi = l[posCodi]
            self.dadesFunc[nomFunc] = {'nom' : nomFunc, 'parametres': [], 'codi': blocCodi, 'ts' : {}}
        else:
            nomFunc = l[0].getText()
            parametres = []
            tsAux = {}
            for child in range(1, n-3):
                    parametres.append(l[child].getText())
                    tsAux[l[child].getText()] = 0
            posCodi = n-2
            blocCodi = l[posCodi]
            self.dadesFunc[nomFunc] = {'nom' : nomFunc, 'parametres' : parametres, 'codi' : blocCodi, 'ts' : tsAux}
           
  
  
    def visitCallFunc(self, ctx):
        l = list(ctx.getChildren())
        numParams = len(l)-1
        nomF = l[0].getText()
        nou_dic = {'nom' : nomF, 'parametres' : list(self.dadesFunc[nomF]['parametres']), 
                   'codi' : self.dadesFunc[nomF]['codi'], 'ts': self.dadesFunc[nomF]['ts'].copy()}

        if nomF in self.dadesFunc.keys():
            nparGuardats = len(self.dadesFunc[nomF]['parametres'])
            if numParams == nparGuardats:
                for i in range(0, nparGuardats):
                    valorParametre = self.visit(l[i+1])
                    nomPar = nou_dic['parametres'][i]
                    nou_dic['ts'][nomPar] = valorParametre
                self.stack.insertTop(nou_dic)
                self.visit(nou_dic['codi'])
                self.stack.removeTop()                
            else:
                raise Exception('Crida al mètode ' + nomF + ' amb nombre de paràmetres incorrecte')
            
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
            valor = self.visit(l[child])
            esEnter = isinstance(valor, int)
            esLlista = isinstance(valor, list)
            if esEnter:
                if valor >= 0:
                    res += ' ' + str(valor)       
                    
            elif esLlista:
                res += ' ' + '['
                n = len(valor)
                for i in range(0,n):
                    if i == n-1:
                        res += str(valor[i])
                    else:
                        res += str(valor[i]) + ','
                res += ']'
                
            elif  self.notes.isNoteValid(valor):
                res += ' ' +  valor
                
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
        n = len(l)
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
        valorsAux = []
        if n >= 1:
            if l[1].getSymbol().type == jsbachParser.NUM:
                for i in range(1, n-1):
                    valorsAux.append(self.visitNum(l[i]))
            else:
                for i in range(1, n-1):
                    valorsAux.append(self.visitNote(l[i]))
        return valorsAux

    def visitListAddStmt(self, ctx):
        l = list(ctx.getChildren())
        noml = l[0].getText()
        element = self.visit(l[2])
        if self.stack.existsInTs(noml):
            llista = self.stack.getInfoFunc()['ts'][noml]
            llista.append(element)
            self.stack.getInfoFunc()['ts'][noml] = llista
        else:
            raise Exception('No existeix cap llista amb el nom ' + noml)  
            
        
    def visitListCutStmt(self, ctx):
        l = list(ctx.getChildren())
        noml = l[1].getText() 
        index = self.visit(l[3])-1
        if index >= 0:
            nomllista = l[1].getText()
            if self.stack.existsInTs(nomllista):
                llista = self.stack.getInfoFunc()['ts'][nomllista]
                if len(llista) >= 1 and index <= (len(llista)-1):
                    llista.pop(index)
                    self.stack.getInfoFunc()['ts'][nomllista] = llista
                else:
                    raise Exception('No existeix el element i-èsim a la llista')
            else:
                raise Exception('No existeix cap llista amb el nom ' + noml)
        else:
            raise Exception('Índex erroni: el valor mínim ha de ser 1!')
        
            

    def visitListSize(self, ctx):
        l = list(ctx.getChildren())
        nomllista = l[1].getText()
        if self.stack.existsInTs(nomllista):
            return len(self.stack.getInfoFunc()['ts'][nomllista])
        else:
            raise Exception('No existeix cap llista amb el nom ' + nomllista)
        
    def visitListGet(self, ctx):
        l = list(ctx.getChildren())
        index = self.visit(l[2])-1
        if index >= 0:
            noml = l[0].getText()
            if self.stack.existsInTs(noml):
                llista = self.stack.getInfoFunc()['ts'][noml]
                if len(llista) >= 1 and index <= (len(llista)-1):
                    return llista[index]
                else:
                    raise Exception('No existeix el element i-èsim a la llista')
            else:
                raise Exception('No existeix cap llista amb el nom ' + noml)  
        else:
            raise Exception('Índex erroni: el valor mínim ha de ser 1!')
        
    def visitPlayId(self, ctx):
        l = list(ctx.getChildren())
        nomll = l[1].getText()
        if self.stack.existsInTs(nomll):
            llistaNotes = self.stack.getInfoFunc()['ts'][nomll]
            if isinstance(llistaNotes, list):
                for i in llistaNotes:
                    if self.notes.isNoteValid(i):
                        self.partitura.append(i)
                    else:
                        if isinstance(i, int) and self.notes.rangAccepted(i):
                            if self.notes.isNoteValid(self.notes.getNote(i)):
                                self.partitura.append(self.notes.getNote(i))
                        else:
                            raise Exception('El valor no està en un rang vàlid per ser nota')
                            
            else:   
                self.partitura.append(llistaNotes)
        else:
            raise Exception('No existeix la llista amb nom' + nomll)
        
    def visitPlayLists(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        llista = self.visitListConst(l[1])
        for i in llista:
            self.partitura.append(i)
        
    def visitRelExp(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            numero = int(l[0].getText())
            if numero > 0:
                return 1
            elif numero == 0:
                return 0
        else:
            opL = self.visit(l[0])
            opR = self.visit(l[2])
            if self.notes.isNoteValid(opL):
                opL = self.notes.getInt(opL)
            
            if self.notes.isNoteValid(opR):
                opR = self.notes.getInt(opR)
        
            tipus = l[1].getSymbol().type
            if tipus == jsbachParser.EQ:
                return int(opL == opR)
            elif tipus == jsbachParser.DIF:
                return int(opL != opR)
            elif tipus == jsbachParser.LST:
                return int(opL < opR)
            elif tipus == jsbachParser.GRT:
                return int(opL > opR)
            elif tipus == jsbachParser.LEQ:
                return int(opL <= opR)
            elif tipus == jsbachParser.GEQ:
                return int(opL >= opR)
            else:
                raise Exception('Operador ' + tipus +
                                'no està definit a JSBach')

    def visitAddSub(self, ctx):
        l = list(ctx.getChildren())
        exprL = self.visit(l[0])
        exprR = self.visit(l[2])
        esNotaL = self.notes.isNoteValid(exprL)
        esNotaR = self.notes.isNoteValid(exprR)
        if esNotaL or esNotaR:
            if esNotaL:
                exprL = self.notes.getInt(exprL)
            elif esNotaR:
                exprR = self.notes.getInt(exprR)
            else:
                exprL = self.notes.getInt(exprL)
                exprR = self.notes.getInt(exprR)
                
            if l[1].getSymbol().type == jsbachParser.SUB:
                resultat = (exprL-exprR)
                if self.notes.rangAccepted(resultat):
                    return self.notes.getNote(resultat)
                else:
                    raise Exception('El valor de la nota no està en un rang valid')
                
            elif l[1].getSymbol().type == jsbachParser.ADD:
                resultat = (exprL+exprR)
                if self.notes.rangAccepted(resultat):
                    return self.notes.getNote(resultat)
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
        llargada = len(ctx.getText())
        if llargada == 1: 
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
        esNotaL = self.notes.isNoteValid(exprL)
        esNotaR = self.notes.isNoteValid(exprR)
        if esNotaL or esNotaR:
            if esNotaL:
                exprL = self.notes.getInt(exprL)
            elif esNotaR:
                exprR = self.notes.getInt(exprR)
            else:
                exprL = self.notes.getInt(exprL)
                exprR = self.notes.getInt(exprR)
            
            if l[1].getSymbol().type == jsbachParser.MUL:
                resultat = exprL * exprR
                if self.notes.rangAccepted(resultat):
                    return self.notes.getNote(resultat)
                else:
                    raise Exception('El valor de la nota no està en un rang valid')
            elif l[1].getSymbol().type == jsbachParser.DIV:
                if exprR != 0:
                    resultat = exprL / exprR
                    if self.notes.rangAccepted(resultat):
                        return self.notes.getNote(resultat)
                    else:
                        raise Exception('El valor de la nota no està en un rang valid')
                else:
                    raise Exception('No es pot dividir per zero!')
                
            elif l[1].getSymbol().type == jsbachParser.MOD:
                resultat = exprL % exprR
                if self.notes.rangAccepted(resultat):
                    return self.notes.getNote(resultat)
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

    if len(sys.argv) > 1:
        if sys.argv[1].endswith('.jsb'):
            nomPrograma = sys.argv[1].split('.')[0]
            input_stream = FileStream(sys.argv[1], encoding='utf-8')
            if len(sys.argv) == 2:
                visitor = EvalVisitor(None, None)
            elif len(sys.argv) > 2:
                params = []
                nomFuncioInit = sys.argv[2]
                for i in range(3, len(sys.argv)):
                    params.append(sys.argv[i])
                visitor = EvalVisitor(nomFuncioInit, params)
        else:
            raise Exception('El fitxer no és un programa en JSBach')

    else:
        input_stream = InputStream(input('jsbach  '))
        visitor = EvalVisitor(None, None)

    lexer = jsbachLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = jsbachParser(token_stream)
    tree = parser.root()
    print(tree.toStringTree(recog=parser))

    notes = visitor.visit(tree)


    cjtnotes = Notes()
    fitxerBase = open('generador.lily', 'r')
    inici = ''
    for linea in fitxerBase:
        inici = inici + '\n' + linea
        
    lilyFile = open(nomPrograma + '.lily', 'a')
    lilyFile.write(inici + '\n')

    
    for note in notes:
        lilyFile.write("%s " % cjtnotes.changeFormat(note))

    lilyFile.write("\n }\n")
    lilyFile.write(" \layout {" "}\n")
    lilyFile.write(" \midi { " "}\n")
    lilyFile.write("}")
    lilyFile.close()
 

    subprocess.call(shlex.split('lilypond ' + nomPrograma + '.lily'))
    subprocess.call(shlex.split('timidity -Ow -o ' + nomPrograma + '.wav ' + nomPrograma + '.midi'))
    subprocess.call(shlex.split('ffmpeg -i ' + nomPrograma + '.wav -codec:a libmp3lame -qscale:a 2 ' + nomPrograma + '.mp3'))


    remove(nomPrograma + '.lily')
    remove(nomPrograma + '.midi')
    remove(nomPrograma + '.wav')
    
    
if __name__ == '__main__':
    main()
