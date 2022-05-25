# Generated from jsbach.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .jsbachParser import jsbachParser
else:
    from jsbachParser import jsbachParser

# This class defines a complete generic visitor for a parse tree produced by jsbachParser.

class jsbachVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by jsbachParser#root.
    def visitRoot(self, ctx:jsbachParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#declFunc.
    def visitDeclFunc(self, ctx:jsbachParser.DeclFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#callFunc.
    def visitCallFunc(self, ctx:jsbachParser.CallFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#conjStmt.
    def visitConjStmt(self, ctx:jsbachParser.ConjStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#stmt.
    def visitStmt(self, ctx:jsbachParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#readStmt.
    def visitReadStmt(self, ctx:jsbachParser.ReadStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#assigs.
    def visitAssigs(self, ctx:jsbachParser.AssigsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#writeStmt.
    def visitWriteStmt(self, ctx:jsbachParser.WriteStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#sentenceIf.
    def visitSentenceIf(self, ctx:jsbachParser.SentenceIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#sentenceWhile.
    def visitSentenceWhile(self, ctx:jsbachParser.SentenceWhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#listStmt.
    def visitListStmt(self, ctx:jsbachParser.ListStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#listConst.
    def visitListConst(self, ctx:jsbachParser.ListConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#listDeclStmt.
    def visitListDeclStmt(self, ctx:jsbachParser.ListDeclStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#listAddStmt.
    def visitListAddStmt(self, ctx:jsbachParser.ListAddStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#listCutStmt.
    def visitListCutStmt(self, ctx:jsbachParser.ListCutStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#listSize.
    def visitListSize(self, ctx:jsbachParser.ListSizeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#listGet.
    def visitListGet(self, ctx:jsbachParser.ListGetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#playStmt.
    def visitPlayStmt(self, ctx:jsbachParser.PlayStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#relExp.
    def visitRelExp(self, ctx:jsbachParser.RelExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by jsbachParser#expr.
    def visitExpr(self, ctx:jsbachParser.ExprContext):
        return self.visitChildren(ctx)



del jsbachParser