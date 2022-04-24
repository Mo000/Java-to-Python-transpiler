from lang.JavaParserVisitor import JavaParserVisitor
from lang.JavaParser import JavaParser
from antlr4 import *
import ast

class ASTVisitor(JavaParserVisitor):
    # Visit a parse tree produced by JavaParser#compilationUnit.
    def visitCompilationUnit(self, ctx):
        # packageDeclaration✕ importDeclaration✕ typeDeclaration✕ moduleDeclaration✕ 
        
        python_ast = ast.Module(body=self.visitChildren(ctx), type_ignores=[])
        #print(ast.dump(python_ast))

        #ast.fix_missing_locations(self.python_ast) # Add line numbers
        #Save file
        #python_code = ast.unparse(self.python_ast)
        #python_dump = ast.dump(self.python_ast, indent=4)
        #print(python_dump)
        #with open("translation.py", "w") as output:
        #    output.write(python_code)
        #    output.close()
        #with open("translation_dump.txt", "w") as output:
        #    output.write(python_dump)
        #    output.close()

    # Visit a parse tree produced by JavaParser#classDeclaration.
    def visitClassDeclaration(self, ctx):
        # CLASS✕ identifier✓ classBody✓ typeParameters✕ EXTENDS✓
        # typeType✕ IMPLEMENTS✕ typeList✕ PERMITS✕

        EXTENDS = ctx.EXTENDS()


        classDecTree = []
        className = self.visit(ctx.identifier())
        classBody = self.visit(ctx.classBody())

        if EXTENDS != None:
            classBase = self.visit(ctx.typeType())
            node = ast.ClassDef(name=className,bases=[classBase],keywords=[],body=classBody,decorator_list=[])
        elif EXTENDS == None:
            node = ast.ClassDef(name=className,bases=[],keywords=[],body=classBody,decorator_list=[])
        else:
            return None

        classDecTree.append(node)


    def visitClassBody(self, ctx):
        # LBRACE✕ RBRACE✕ classBodyDeclaration✓
        ctxs = ctx.classBodyDeclaration() # List declarations within the class body
        return self.visitAll(ctxs)

    def visitClassBodyDeclaration(self, ctx):
        # SEMI✕ block✕ STATIC✕ modifier✕ memberDeclaration✓
        print(self.visit(ctx.memberDeclaration()))
        return "x"

    def visitMemberDeclaration(self, ctx):
        # methodDeclaration✓ genericMethodDeclaration✕ fieldDeclaration✕
        # constructorDeclaration✕ genericConstructorDeclaration✕ interfaceDeclaration✕
        # annotationTypeDeclaration✕ classDeclaration✕ enumDeclaration✕ recordDeclaration✕

        methodDeclaration = ctx.methodDeclaration()
        genericMethodDeclaration = ctx.genericMethodDeclaration()
        fieldDeclaration = ctx.fieldDeclaration()
        constructorDeclaration = ctx.constructorDeclaration()
        genericConstructorDeclaration = ctx.genericConstructorDeclaration()
        interfaceDeclaration = ctx.interfaceDeclaration()
        annotationTypeDeclaration = ctx.annotationTypeDeclaration()
        classDeclaration = ctx.classDeclaration()
        enumDeclaration = ctx.enumDeclaration()
        recordDeclaration = ctx.recordDeclaration()

        if methodDeclaration != None:
            return self.visit(methodDeclaration)
        elif genericMethodDeclaration != None:
            return None
        elif fieldDeclaration != None:
            return None
        elif constructorDeclaration != None:
            return None
        elif genericConstructorDeclaration != None:
            return None
        elif interfaceDeclaration != None:
            return None
        elif annotationTypeDeclaration != None:
            return None
        elif classDeclaration != None:
            return None
        elif enumDeclaration != None:
            return None
        elif recordDeclaration != None:
            return None
        return None

    def visitMethodDeclaration(self, ctx):
        # typeTypeOrVoid✕ identifier✓ formalParameters✓ methodBody✓
        # LBRACK✕ RBRACK✕ THROWS✕ qualifiedNameList✕

        methodParams = self.visit(ctx.formalParameters())
        methodName = self.visit(ctx.identifier())
        methodBody = self.visit(ctx.methodBody())
        
        node = ast.FunctionDef(
        name=methodName,
        args=[
            ast.arguments(
                posonlyargs=[],
                args=methodParams,
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
        )],
        body=[methodBody],
        decorator_list=[],
        returns=[]
        )
        return node

    def visitFieldDeclaration(self, ctx):
        # VARIABLE OUTSIDE METHOD
        # EG: int hello = 5
        self.variableDeclaration(ctx)
        self.visitChildren(ctx)
    
    def visitLocalVariableDeclaration(self, ctx):
        # VARIABLE INSIDE METHOD
        # EG: int hello = 5
        self.variableDeclaration(ctx)
        self.visitChildren(ctx)

    # Shared functionality for FieldDeclaration, LocalVariableDeclaration
    def variableDeclaration(self, ctx):
        return None

    def visitStatement(self, ctx):
        return None

    def visitExpression(self, ctx):
        return None

    def visitIdentifier(self, ctx):
        # IDENTIFIER✓ MODULE✕ OPEN✕ REQUIRES✕ EXPORTS✕
        # OPENS✕ TO✕ USES✕ PROVIDES✕ WITH✕ TRANSITIVE✕
        # YIELD✕ SEALED✕ PERMITS✕ RECORD✕ VAR✕

        return ctx.IDENTIFIER().getText()

    def visitFormalParameters(self, ctx):
        # LPAREN✕ RPAREN✕ receiverParameter✕ COMMA✕ formalParameterList✓
        
        return self.visit(ctx.formalParameterList())
        
    def visitFormalParameterList(self, ctx):
        # formalParameter✓ COMMA✕ lastFormalParameter✕

        ctxs = ctx.formalParameter()
        return self.visitAll(ctxs)

    def visitFormalParameter(self, ctx):
        # typeType✕ variableDeclaratorId✓ variableModifier✕
        return self.visit(ctx.variableDeclaratorId())

    def visitVariableDeclaratorId(self, ctx):
        # identifier✓ RBRACK✕ RBRACK✕

        return self.visit(ctx.identifier())

    def visitTypeType(self, ctx):
        # classOrInterfaceType✓ primitiveType✓ annotation✕ LBRACK✕ RBRACK✕
        
        classOrInterfaceType = ctx.classOrInterfaceType()
        primitiveType = ctx.primitiveType()

        if classOrInterfaceType != None:
            return self.visit(classOrInterfaceType)        
        elif primitiveType != None:
            return self.visit(primitiveType)
        else:
            return None

    def visitClassOrInterfaceType(self, ctx):
        # identifier✓ typeArguments✕ DOT✕

        identifier = self.visit(ctx.identifier(0))

        if identifier == "String":
            return str
        else:
            return identifier

    def visitPrimitiveType(self, ctx):
        # BOOLEAN✓ CHAR✓ BYTE✓ SHORT✓ INT✓ LONG✓ FLOAT✓ DOUBLE✓

        BOOLEAN = ctx.BOOLEAN()
        CHAR = ctx.CHAR()
        BYTE = ctx.BYTE()
        SHORT = ctx.SHORT()
        INT = ctx.INT()
        LONG = ctx.LONG()
        FLOAT = ctx.FLOAT()
        DOUBLE = ctx.DOUBLE()

        if BOOLEAN != None:
            return bool
        elif CHAR != None:
            return str
        elif BYTE != None:
            return int
        elif SHORT != None:
            return int
        elif INT != None:
            return int
        elif LONG != None:
            return int
        elif FLOAT != None:
            return float
        elif DOUBLE != None:
            return float
        else:
            return None
        
    def visitAll(self, nodeList):

        visitList = []

        for nodes in nodeList:
            node = self.visit(nodes)
            visitList.append(node)

        return visitList

    def searchChildren(self, ctx, ruleIndex): # Returns all children matching a certain rule

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