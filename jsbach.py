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
    
class MyVisitor(jsbachVisitor):
    def __init__(self):
        self.nivell = 0
        self.ts = {}
        
    def visitComment(self, ctx):
        pass
        
    def visitDeclFunc(self, ctx):
        pass
    
    def visitCallFunc(self, ctx):
        pass
    
    def visitReadStmt(self, ctx):  
        pass
    
    def visitWriteStmt(self, ctx):
        try:
            l = list(ctx.getChildren())
            print(l[1].getText())
        except Exception:
            print("Exception: Nothing to write about!")
            
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
        pass 

    def visitExpr(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            return int(l[0].getText())
        else:  # len(l) == 3
            if l[1].getSymbol().type == jsbachParser.MUL: 
                return (int(l[0].getText()) * int(l[2].getText()))
                
            elif l[1].getSymbol().type == jsbachParser.DIV:
                try: 
                    return (int(l[0].getText()) / int(l[2].getText()))
                except ZeroDivisionError:
                    print("Exception: Division by zero!")
                    
            elif l[1].getSymbol().type == jsbachParser.MOD:
                return (int(l[0].getText()) % int(l[2].getText()))
                
            elif l[1].getSymbol().type == jsbachParser.SUB:
                return (int(l[0].getText()) - int(l[2].getText()))
                    
            elif l[1].getSymbol().type == jsbachParser.ADD:
                return (int(l[0].getText()) + int(l[2].getText()))
            else:
                return (l[2].getText())
           



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
    
    visitor = MyVisitor()
    visitor.visit(tree)


if __name__ == '__main__':
    main()
