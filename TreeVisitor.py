if __name__ is not None and "." in __name__:
    from .jsbachParser import jsbachParser
    from .jsbachVisitor import jsbachVisitor
else:
    from jsbachParser import jsbachParser
    from jsbachVisitor import jsbachVisitor
class TreeVisitor(jsbachVisitor):
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
        pass
    
    def visitSentenceIf(self, ctx):
        pass 
    
    def visitSentenceAssigs(self, ctx):
        l = list(ctx.getChildren())
        key = l[0].getText()
        value  = int(l[2].getText())
        self.ts[key] = value
            
    
    
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
                return int(l[0].getText) * int(l[2].getText())
                
            elif l[1].getSymbol().type == jsbachParser.DIV:
                print('  ' *  self.nivell + 'DIV(/)')
                self.nivell += 1
                self.visit(l[0])
                self.visit(l[2])
                self.nivell -= 1
                return int(l[0].getText) / int(l[2].getText())
                
            elif l[1].getSymbol().type == jsbachParser.MOD:
                print('  ' *  self.nivell + 'MOD(%)')
                self.nivell += 1
                self.visit(l[0])
                self.visit(l[2])
                self.nivell -= 1
                return int(l[0].getText) % int(l[2].getText())
                
            elif l[1].getSymbol().type == jsbachParser.SUB:
                print('  ' *  self.nivell + 'SUB(-)')
                self.nivell += 1
                self.visit(l[0])
                self.visit(l[2])
                self.nivell -= 1
                return int(l[0].getText) - int(l[2].getText())
                    
            elif l[1].getSymbol().type == jsbachParser.ADD:
                print('  ' *  self.nivell + 'ADD(+)')
                self.nivell += 1
                self.visit(l[0])
                self.visit(l[2])
                self.nivell -= 1
                return int(l[0].getText) + int(l[2].getText())
           
           
