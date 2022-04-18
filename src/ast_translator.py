from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from lang.JavaLexer import JavaLexer
from lang.JavaParser import JavaParser
from lang.JavaParserVisitor import JavaParserVisitor
from pprint import pformat


class AstTranslator:
    def execute(input_source):
        parser = JavaParser(CommonTokenStream(JavaLexer(FileStream(input_source, encoding="utf-8"))))
        tree = parser.compilationUnit()
        JavaParserVisitor().visit(tree)
    if __name__ == '__main__':
        target_file_path = 'testfile.java'
        execute(target_file_path)