from antlr4 import *
from jsbach import MyVisitor
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
input_stream = InputStream(input('? '))
lexer = jsbachLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = jsbachParser(token_stream)

tree = parser.root()
print(tree.toStringTree(recog=parser))

visitor = MyVisitor()
visitor.visit(tree)
