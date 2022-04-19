from lang.JavaParserVisitor import JavaParserVisitor
from lang.JavaParser import JavaParser
from antlr4 import *
import ast

class ASTVisitor(JavaParserVisitor):
    path = [] # Path down the tree, containing all nodes with bodies
    python_ast = ast.parse('')
    # Visit a parse tree produced by JavaParser#compilationUnit.
    def visitCompilationUnit(self, ctx):
         # AST root
        self.path.append(self.python_ast.body)
        self.visitChildren(ctx)
        self.path.pop() # Nodes are removed from path after all children are visited

        ast.fix_missing_locations(self.python_ast) # Add line numbers

        #Save file
        python_code = ast.unparse(self.python_ast)
        python_dump = ast.dump(self.python_ast, indent=4)
        #print(python_dump)
        with open("translation.py", "w") as output:
            output.write(python_code)
            output.close()
        with open("translation_dump.txt", "w") as output:
            output.write(python_dump)
            output.close()

    # Visit a parse tree produced by JavaParser#classDeclaration.
    def visitClassDeclaration(self, ctx):
        # CLASS
        # EG: public class hello{}
        child_count = int(ctx.getChildCount())
        if child_count >3:
            # extends, implements, or permits
            # c0 = ctx.getChild(0)  # class
            c1 = ctx.identifier().getText()  # class name
            c2 = ctx.getChild(2).getText()  #  extends/implements/permits
            if c2 == 'extends':
                c3 = ctx.getChild(3).getChild(0).getText()  # extends class name
            # implements/permits not implemented

            node = ast.ClassDef(name=c1,bases=[ast.Name(id=c3, ctx=ast.Load())],keywords=[],body=[],decorator_list=[])
        else:
            c1 = ctx.getChild(1).getText()  # class name
            node = ast.ClassDef(name=c1,bases=[],keywords=[],body=[],decorator_list=[])
        self.path[-1].insert(len(self.path[-1]), node) # Insert node to AST
        self.path.append(self.path[-1][-1].body) # Add node body to path
        self.visitChildren(ctx)
        self.path.pop()

    # Visit a parse tree produced by JavaParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx):
        # METHOD
        # EG: public static void main(String[] args){ }
        # c0 = ctx.getChild(0).getText() # return type
        c1 = ctx.identifier().getText() # method name
        # c2 = ctx.getChild(2).getText() # parameters
        # c3 = ctx.getChild(3).getText() # method body

        cX = ctx.formalParameters().formalParameterList() # parameter List
        argList = []

        for i in cX.getChildren():
            if i.getText() == ",":
                continue
            argList.append(i.variableDeclaratorId().getText()) # Every parameter is added to the list
        for j in range(len(argList)):
            argList[j] = ast.arg(arg=argList[j])
        node = ast.FunctionDef(name=c1,args=[ast.arguments(
            posonlyargs=[],args=argList,kwonlyargs=[],kw_defaults=[],defaults=[]
        )],body=[],decorator_list=[],returns=[])
        self.path[-1].insert(len(self.path[-1]), node)
        self.path.append(self.path[-1][-1].body)
        self.visitChildren(ctx)
        self.path.pop()

    # Visit a parse tree produced by JavaParser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx):
        # VARIABLE OUTSIDE METHOD
        # EG: int hello = 5
        ASTVisitor.variableDeclaration(self, ctx)
        self.visitChildren(ctx)
    # Visit a parse tree produced by JavaParser#localVariableDeclaration.
    def visitLocalVariableDeclaration(self, ctx):
        # VARIABLE INSIDE METHOD
        # EG: int hello = 5
        ASTVisitor.variableDeclaration(self, ctx)
        self.visitChildren(ctx)

    # Shared functionality for FieldDeclaration, LocalVariableDeclaration
    def variableDeclaration(self, ctx):
        c0 = ctx.getChild(0)  # Type
        c1 = ctx.getChild(1)  # LHS = RHS
        c10 = c1.getChild(0).getChild(0).identifier().getText() # LHS
        #c11 = c1.getChild(0).getChild(1).getText() # =
        c12 = c1.getChild(0).getChild(2).getText() # RHS
        literal = False
        arrayList = False # Methods not implemented
        dataType = c0.getChild(0).getText().lower()

        methodCalls = ASTVisitor.searchChildren(self, ctx, 96) # RULE_methodCall = 96
        if methodCalls:
            print(methodCalls[0].getText())
        if hasattr(c0.getChild(0).getChild(0), 'IDENTIFIER'):
            if str(c0.getChild(0).getChild(0).IDENTIFIER()) == "ArrayList":
                arrayList = True
        if c0.LBRACK() or c1.getChild(0).getChild(0).LBRACK() or arrayList == True: # type, or name contains '[]', or is ArrayList Technical debt solution
            # Array or ArrayList
            eltsList = []
            if c1.getChild(0).getChild(2).getChild(0).getChild(0).getChildCount() == 0: # Technical debt solution
                literal = True
            if literal: # literal
                dataType = c0.getChild(0).getText().lower()
                if c1.getChild(0).getChild(2).getChild(0).getChild(1).getRuleIndex() == 108: # RULE_creator Technical debt solution
                    # new arrayList
                    eltsList = []
                else:
                    # new array
                    for value in c1.getChild(0).getChild(2).getChild(0).getChildren():
                        data = value.getText()
                        if data == "{" or data == "}" or data == ",":
                            continue
                        convertedData = ASTVisitor.convertDataType(self, dataType, data)
                        eltsList.append(ast.Constant(convertedData))
                node = ast.Assign(
                    targets=[ast.Name(id=c10,ctx=ast.Store())],
                    value=ast.List(elts=eltsList,ctx=ast.Load()))
            else: # identifier
                node = ast.Assign(
                    targets=[ast.Name(id=c10,ctx=ast.Store())],
                    value=ast.Name(id=c12, ctx=ast.Load()))
        else:
            c12T = c1.getChild(0).getChild(2).getChild(0).getChild(0).getChild(0) # identifier / literal
            #if c12T.getRuleIndex() == 51: # RULE_literal Technical debt solution
            #    literal = True
            if literal: # literal
                c12 = ASTVisitor.convertDataType(self, dataType, c12)
                node = ast.Assign(
                    targets=[ast.Name(id=c10, ctx=ast.Store())],
                    value=ast.Constant(value=c12))
            else: # c12T.getRuleIndex() == 80: # RULE_identifier indentifier
                node = ast.Assign(
                    targets=[ast.Name(id=c10, ctx=ast.Store())],
                    value=ast.Name(id=c12, ctx=ast.Load()))
        self.path[-1].insert(len(self.path[-1]), node)
    def convertDataType(self, dataType, data):
        if dataType == "byte":
            converted = int(data)
        elif dataType == "short":
            converted = int(data)
        elif dataType == "int":
            converted = data
            converted = int(data)
        elif dataType == "long":
            if data[-1].lower() == "l":
                data = data[:-1] # remove "l"
            converted = int(data)
        elif dataType == "float":
            if data[-1].lower() == "f":
                data = data[:-1] # remove "f"
            converted = float(data)
        elif dataType == "double":
            if data[-1].lower() == "d":
                data = data[:-1] # remove "d"
            converted = float(data)
        elif dataType == "char":
            converted = str(data[1:-1]) # remove speech marks
        elif dataType == "string":
            converted = str(data[1:-1])
        elif dataType == "boolean":
            converted = bool(data)
        else:
            converted = 0
        return converted

    def searchChildren(self, ctx, ruleIndex): # Returns highest order instance of child matching rule
        unsearched = []
        matched = []
        for child in ctx.getChildren():
            unsearched.append(child)
        while len(unsearched) > 0:
            if hasattr(unsearched[0], 'getRuleIndex'):
                if unsearched[0].getRuleIndex() == ruleIndex:
                    matched.append(unsearched[0])
                for child in unsearched[0].getChildren():
                    unsearched.append(child)
            unsearched.pop(0)
        return matched