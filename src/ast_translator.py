from antlr4 import FileStream, CommonTokenStream
from lang.JavaLexer import JavaLexer
from lang.JavaParser import JavaParser
from lang.ASTVisitor import ASTVisitor


class AstTranslator:
    def execute(input_source):   
        parser = JavaParser(CommonTokenStream(JavaLexer(FileStream(input_source, encoding="utf-8"))))
        tree = parser.compilationUnit()
        ASTVisitor().visit(tree)
    if __name__ == '__main__':
        target_file_path = 'testfile.java'
        execute(target_file_path)