if __name__ is not None and "." in __name__:
    from .jsbachParser import jsbachParser
    from .jsbachVisitor import ExprVisitor
else:
    from jsbachParser import jsbachParser
    from jsbachVisitor import jsbachVisitor
class TreeVisitor(jsbachVisitor):
    def __init__(self):
        self.nivell = 0
        self.ts = {}
        
    def visitDeclFunc(self, ctx):
        return
    
    def visitCallFunc(self, ctx):
        return
    
    def visitReadStmt(self, ctx):  
        return
    
    def visitWriteStmt(self, ctx):
        return
    
    def visitSentenceIf(self, ctx):
        return 
    
    def visitSentenceAssigs(self, ctx):
        return 
    
    def visitSentenceWhile(self, ctx):
        return 
    
    def visitListStmt(self, ctx):
        return 
    
    def visitListConst(self, ctx):
        return 
    
    def visitListDecl(self, ctx):
        return 
    
    def visitListSizeStmt(self, ctx):
        return 
    
    def visitListGet(self, ctx):
        return
    
    def visitPlayStmt(self, ctx):
        return 
    
    def visitRelExp(self, ctx):
        return 

    def visitExpr(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            print("  " * self.nivell +
                  jsbachParser.symbolicNames[l[0].getSymbol().type] +
                  '(' +l[0].getText() + ')')
        else:  # len(l) == 3
            if l[1].getSymbol().type == jsbachParser.MUL: 
                print('  ' *  self.nivell + 'MUL(*)')
                self.nivell += 1
                self.visit(l[0])
                self.visit(l[2])
                self.nivell -= 1
                
            elif l[1].getSymbol().type == jsbachParser.DIV:
                print('  ' *  self.nivell + 'DIV(/)')
                self.nivell += 1
                self.visit(l[0])
                self.visit(l[2])
                self.nivell -= 1
                
            elif l[1].getSymbol().type == jsbachParser.MOD:
                print('  ' *  self.nivell + 'MOD(%)')
                self.nivell += 1
                self.visit(l[0])
                self.visit(l[2])
                self.nivell -= 1
                
            elif l[1].getSymbol().type == jsbachParser.SUB:
                print('  ' *  self.nivell + 'SUB(-)')
                self.nivell += 1
                self.visit(l[0])
                self.visit(l[2])
                self.nivell -= 1
                    
            elif l[1].getSymbol().type == jsbachParser.ADD:
                print('  ' *  self.nivell + 'ADD(+)')
                self.nivell += 1
                self.visit(l[0])
                self.visit(l[2])
                self.nivell -= 1
           
           
