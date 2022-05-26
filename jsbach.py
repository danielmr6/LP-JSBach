import sys
from antlr4 import *
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser

if __name__ is not None and "." in __name__:
    from .jsbachParser import jsbachParser
    from .jsbachVisitor import jsbachVisitor
else:
    from jsbachParser import jsbachParser
    from jsbachVisitor import jsbachVisitor
    
class EvalVisitor(jsbachVisitor):
    def __init__(self, nomFuncioIni: str, parametres:list):
        self.nivell = 0
        if nomFuncioIni != None and nomFuncioIni != 'Main':
            self.nomFuncioInicial = nomFuncioIni
            self.parametres = parametres
        else:
            self.nomFuncioInicial = 'Main'
            self.parametres = []
        
        self.ts = {}
        self.pila = []
        self.dadesFunc = {}
        self.partitura = []
        
        '''dadesFunc = 
        { 
        "Main" : { 
                   "parametres" : [] , 
                   "codi" : ...,
                   "taulaSimbols" : 
                   {
                    "nomVariable" : valor ...   
                   }
                }
        }
        Fem un diccionari tenint com a clau el nom de la funcio i com a valor una tupla amb 
        parametres i el codi de la funcio
        
         En DeclFunc guardamos la informacion de la funcion en dadesFunc y el callFunc ejecuta.
         Despues de recorrer todo, miramos si esta el main, si esta llamamos  y pasamos el valor de codi.
         Si no está, excepción.
         '''
    def visitRoot(self, ctx):
        l = list(ctx.getChildren()) 
        n = len(l)
        for i in range(0,n):
            self.visit(l[i])
        
        
        if 'Main' in self.dadesFunc.keys(): 
            if self.nomFuncioInicial == 'Main':
                return self.visit(self.dadesFunc['Main']['codi'])
            else:
                self.visit(self.dadesFunc[self.nomFuncioInicial]['codi'])
                self.visit(self.dadesFunc['Main']['codi'])
        else:
            raise Exception("No està definida la funció Main()")
        
    #Guardar la informació en els diccionaris
    def visitDeclFunc(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        print(n)
        if (len(l) == 4):
            nomFunc = l[0].getText()
            posCodi = 2
            blocCodi = l[posCodi]
            self.dadesFunc[nomFunc] = {'parametres' : [], 'codi' : blocCodi}
            print(self.dadesFunc)
        else:
            nomFunc = l[0].getText()
            parametres = []
            for child in range(1, n):
                #no hem arribat al limitador esquerrà
                if not l[child].getSymbol().type == jsbachParser.L_LMT:
                    parametres.append(l[child].getText())
                else:
                    posCodi = child+1
                    blocCodi = l[posCodi]
            self.dadesFunc[nomFunc] = {'parametres' : parametres, 'codi' : blocCodi}
                        
    
    '''
    Metode quan es crida a una funció que no es el main
    '''        
    def visitCallFunc(self, ctx):
        pass
    
    def visitReadStmt(self, ctx):  
        l = list(ctx.getChildren())
        info = input()
        key = l[0].getText()
        self.ts[key] = info
        return self.ts[key]
        
    def visitWriteStmt(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        res = ""
        for child in range(1, n):
            var = l[child]
            if var.getSymbol().type == jsbachParser.ID:
                if var.getText() in self.ts.keys():
                    res += ' ' + str(self.ts[var.getText()])
                else:
                    raise Exception("No està al diccionari")
                    
            else: 
                res += var.getText()
        print(res)
            
    def visitSentenceIf(self, ctx):
        l = list(ctx.getChildren())
        condition = bool(self.visitRelExp(l[1]))
        if condition:
            return self.visit(l[3])        
        elif len(l) == 9:
            return self.visit(l[7])
         
    
    def visitAssigs(self, ctx):
        l = list(ctx.getChildren())
        key = l[0].getText()
        value  = int(l[2].getText())
        self.ts[key] = value
        
    def visitSentenceWhile(self, ctx):
        l = list(ctx.getChildren())
        while (True):
            condition = bool(self.visitRelExp(l[1]))
            if not condition:
                break
            return self.visit(l[3])
             
    
    def visitListStmt(self, ctx):
        pass 
    
    def visitListConst(self, ctx):
        pass 
    
    def visitListDeclStmt(self, ctx):
        pass 
    
    def visitListAddStmt(self, ctx):
        pass
    
    def visitListCut(self, ctx): 
        pass
    
    def visitListSize(self, ctx):
        pass 
    
    def visitListGet(self, ctx):
        pass
    
    def visitPlayStmt(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        if l[1].getText() == '{':
            i = 2
            while i < n and l[i].getText() != '}': 
                self.partitura.append(l[i].getText())
                i += 1
        print(self.partitura)
    
    def visitRelExp(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            return self.visit(l[0]) != 0
        else:
            opL = self.visit(l[0])
            opR = self.visit(l[2])
            if l[1].getSymbol().type == jsbachParser.EQ:
                return (opL == opR)
            elif l[1].getSymbol().type == jsbachParser.DIF:
                return (opL != opR)
            elif l[1].getSymbol().type == jsbachParser.LST:
                return (opL < opR)
            elif l[1].getSymbol().type == jsbachParser.GRT:
                return (opL > opR)
            elif l[1].getSymbol().type == jsbachParser.GREQ:
                return (opL >= opR)   
            elif l[1].getSymbol().type == jsbachParser.LSEQ:
                return (opL <= opR)
            else:
                raise Exception("Operador relacional invàlid")

    def visitExpr(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            if l[0].getSymbol().type == jsbachParser.NUM:
                return int(l[0].getText())
            elif l[0].getSymbol().type == jsbachParser.NOTE:
                return (l[0].getText())
        else: 
            if l[1].getSymbol().type == jsbachParser.MUL: 
                return self.visit(l[0]) * self.visit(l[2])
                
            elif l[1].getSymbol().type == jsbachParser.DIV:
                try: 
                    return self.visit(l[0]) / self.visit(l[2])
                
                except ZeroDivisionError:
                    print("Exception: Division by zero!")
                    
            elif l[1].getSymbol().type == jsbachParser.MOD:
                return self.visit(l[0]) % self.visit(l[2])
                
            elif l[1].getSymbol().type == jsbachParser.SUB:
                return self.visit(l[0]) - self.visit(l[2])
                    
            elif l[1].getSymbol().type == jsbachParser.ADD:
                return self.visit(l[0]) + self.visit(l[2])
            else:
                return self.visit(l[2])
           
    
def main():
    
    if len(sys.argv) > 1:
        if sys.argv[1].endswith('.jsb'):
            input_stream = FileStream(sys.argv[1])
            if len(sys.argv) == 2:
                visitor = EvalVisitor(None, None)
            elif len(sys.argv) > 2:
                params = []
                nomFuncioInit = sys.argv[2]
                for i in range (3, len(sys.argv)):
                    params.append(sys.argv[i])
                visitor = EvalVisitor(nomFuncioInit, params)
        else:
            raise Exception("El fitxer no és un programa en JSBach")
    
    else:
        input_stream = InputStream(input('jsbach  '))
        visitor = EvalVisitor(None, None)
        
    lexer = jsbachLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = jsbachParser(token_stream)
    tree = parser.root()
    print(tree.toStringTree(recog=parser))
    
    visitor.visit(tree)


if __name__ == '__main__':
    main()
