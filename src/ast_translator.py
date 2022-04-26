from antlr4 import FileStream, CommonTokenStream
from lang.JavaLexer import JavaLexer
from lang.JavaParser import JavaParser
from lang.ASTVisitor import ASTVisitor
from antlr4.tree.Trees import Trees

class AstTranslator:
    def execute(input_source):   
        parser = JavaParser(CommonTokenStream(JavaLexer(FileStream(input_source, encoding="utf-8"))))
        tree = parser.compilationUnit()
        ASTVisitor().visit(tree)
        print(Trees.toStringTree(tree, None, parser))
    if __name__ == '__main__':
        target_file_path = 'java-runtime/testfile.java'
        execute(target_file_path)