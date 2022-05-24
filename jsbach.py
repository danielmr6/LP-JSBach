import sys
from this import d
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
    def __init__(self):
        self.nivell = 0
        self.ts = {}
        
    def visitRoot(self, ctx):
        l = list(ctx.getChildren()) 
        print(self.visit(l[0]))
   
    def visitComment(self, ctx):
        pass
        
    def visitDeclFunc(self, ctx):
        pass
    
    def visitCallFunc(self, ctx):
        pass
    
    def visitReadStmt(self, ctx):  
        pass
    
    def visitWriteStmt(self, ctx):
        l = list(ctx.getChildren())
        n = len(l)
        res = ""
        esText = False
        for child in range(1, n):
            var = l[child]
            if var.getSymbol().type == jsbachParser.ID and not esText:
                if var.getText() in self.ts.keys():
                    res += str(self.ts[var.getText()])
                else:
                    print("Exception: No està al diccionari")
                    
            elif var.getSymbol().type == jsbachParser.TXT:
                    res += var.getText()
                    esText = True
        return res
            
    def visitSentenceIf(self, ctx):
        pass 
    
    def visitSentenceAssigs(self, ctx):
        l = list(ctx.getChildren())
        key = l[0].getText()
        value  = int(l[2].getText())
        self.ts[key] = value
        return self.ts
        
    def visitSentenceWhile(self, ctx):
        pass 
    
    def visitListStmt(self, ctx):
        pass 
    
    def visitListConst(self, ctx):
        pass 
    
    def visitListDecl(self, ctx):
        pass 
    
    def visitListSizeStmt(self, ctx):
        pass 
    
    def visitListGet(self, ctx):
        pass
    
    def visitPlayStmt(self, ctx):
        pass 
    
    def visitRelExp(self, ctx):
        l = list(ctx.getChildren())
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
            print("Exception: Invalid relational operator!")

    def visitExpr(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            return int(l[0].getText())
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
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(input('? '))
        
    lexer = jsbachLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = jsbachParser(token_stream)
    tree = parser.root()
    print(tree.toStringTree(recog=parser))
    
    visitor = EvalVisitor()
    visitor.visit(tree)


if __name__ == '__main__':
    main()
