from antlr4 import *
from TreeVisitor import TreeVisitor
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
input_stream = InputStream(input('? '))
lexer = jsbachLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = jsbachParser(token_stream)

tree = parser.root()
print(tree.toStringTree(recog=parser))

visitor = TreeVisitor()
visitor.visit(tree)
