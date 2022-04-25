from copyreg import constructor
from lang.JavaParserVisitor import JavaParserVisitor
from lang.JavaParser import JavaParser
from antlr4 import *
import ast

class ASTVisitor(JavaParserVisitor):

    astCtx = ast.Load() # Set context for loading/store identifiers

    # Visit a parse tree produced by JavaParser#compilationUnit.
    def visitCompilationUnit(self, ctx):
        # packageDeclaration✕ importDeclaration✕ typeDeclaration✓ moduleDeclaration✕ 
        
        packageDeclaration = ctx.packageDeclaration()
        importDeclaration = ctx.importDeclaration()
        typeDeclaration = ctx.typeDeclaration()
        moduleDeclaration = ctx.moduleDeclaration()

        rootList = []

        # if packageDeclaration != None:
        #     print(packageDeclaration)
        # if importDeclaration != None:
        #     print(importDeclaration)
        if typeDeclaration != None:
            rootList.extend(self.visitAll(typeDeclaration))
        # if moduleDeclaration != None:
        #     print(moduleDeclaration)

        python_ast = ast.Module(body=rootList, type_ignores=[])
    
        ast.fix_missing_locations(python_ast) # Add line numbers
        # Save file
        python_code = ast.unparse(python_ast)
        python_dump = ast.dump(python_ast, indent=4)
        #print(python_dump)
        with open("translation.py", "w") as output:
            output.write(python_code)
            output.close()
        with open("translation_dump.txt", "w") as output:
            output.write(python_dump)
            output.close()

    def visitTypeDeclaration(self, ctx):
        # classDeclaration✓ enumDeclaration✕ interfaceDeclaration✕
        # annotationTypeDeclaration✕ recordDeclaration✕ classOrInterfaceModifier✕ SEMI✕

        classDeclaration = ctx.classDeclaration()
        enumDeclaration = ctx.enumDeclaration()
        interfaceDeclaration = ctx.interfaceDeclaration()
        annotationTypeDeclaration = ctx.annotationTypeDeclaration()
        recordDeclaration = ctx.recordDeclaration()
        classOrInterfaceModifier = ctx.classOrInterfaceModifier()
        
        if classDeclaration != None:
            return self.visit(classDeclaration)        
        elif enumDeclaration != None:
            return None
        elif interfaceDeclaration != None:
            return None
        elif annotationTypeDeclaration != None:
            return None
        elif recordDeclaration != None:
            return None
        elif len(classOrInterfaceModifier) > 0:
            return None
        else:
            return None

    # Visit a parse tree produced by JavaParser#classDeclaration.
    def visitClassDeclaration(self, ctx):
        # CLASS✕ identifier✓ classBody✓ typeParameters✕ EXTENDS✓
        # typeType✕ IMPLEMENTS✕ typeList✕ PERMITS✕

        classEXTENDS = ctx.EXTENDS()

        className = self.visit(ctx.identifier())
        classBody = self.visit(ctx.classBody())

        node = None

        if classEXTENDS != None:
            extends = self.visit(ctx.typeType())
            classBase = ast.Constant(value=extends)
            node = ast.ClassDef(name=className,bases=[classBase],keywords=[],body=classBody,decorator_list=[]) # Can only extend one class in Java
        elif classEXTENDS == None:
            node = ast.ClassDef(name=className,bases=[],keywords=[],body=classBody,decorator_list=[])
        else:
            return None

        return node


    def visitClassBody(self, ctx):
        # LBRACE✕ RBRACE✕ classBodyDeclaration✓
        classBodyDeclaration = ctx.classBodyDeclaration() # List declarations within the class body
        return self.visitAll(classBodyDeclaration)

    def visitClassBodyDeclaration(self, ctx):
        # SEMI✕ block✕ STATIC✕ modifier✕ memberDeclaration✓

        return self.visit(ctx.memberDeclaration())

    def visitMemberDeclaration(self, ctx):
        # methodDeclaration✓ genericMethodDeclaration✕ fieldDeclaration✓
        # constructorDeclaration✓ genericConstructorDeclaration✕ interfaceDeclaration✕
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
            return self.visit(fieldDeclaration) # Capable of converting declarations like x,y,z = 1,2,3
        elif constructorDeclaration != None:
            return self.visit(constructorDeclaration)
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
        else:
            return None

    def visitConstructorDeclaration(self, ctx):
        # identifier✓ formalParameters✓ block✓ THROWS✕ qualifiedNameList✕

        formalParameters = ctx.formalParameters()
        block = ctx.block()
        
        constructorName = "__init__" # Standard Python class constructor name
        constructorParams = self.visit(formalParameters)
        constructorBody = self.visit(block)

        constructorArgs = []
        for arg in constructorParams:
            constructorArgs.append(ast.arg(arg=arg))

        node = ast.FunctionDef(
        name=constructorName,
        args=[
            ast.arguments(
                posonlyargs=[],
                args=constructorArgs,
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
        )],
        body=constructorBody,
        decorator_list=[],
        returns=[]
        )
        return node

    def visitMethodDeclaration(self, ctx):
        # typeTypeOrVoid✕ identifier✓ formalParameters✓ methodBody✓
        # LBRACK✕ RBRACK✕ THROWS✕ qualifiedNameList✕

        identifier = ctx.identifier()
        formalParameters = ctx.formalParameters()
        methodBody = ctx.methodBody()

        methodName = self.visit(identifier)
        methodBody = self.visit(methodBody)
        methodParams = self.visit(formalParameters)
        
        methodArgs = []
        for arg in methodParams:
            methodArgs.append(ast.arg(arg=arg))
        
        node = ast.FunctionDef(
        name=methodName,
        args=[
            ast.arguments(
                posonlyargs=[],
                args=methodArgs,
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
        )],
        body=methodBody,
        decorator_list=[],
        returns=[]
        )
        return node

    def visitMethodBody(self, ctx):
        # block✓ SEMI✕

        return self.visit(ctx.block())

    def visitBlock(self, ctx):
        # LBRACE✕ RBRACE✕ blockStatement✓

        blockStatement = ctx.blockStatement()
        return self.visitAll(blockStatement)


    def visitBlockStatement(self, ctx):
        # localVariableDeclaration✓ SEMI✕ statement✓ localTypeDeclaration✓

        localVariableDeclaration = ctx.localVariableDeclaration()
        localTypeDeclaration = ctx.localTypeDeclaration()
        statement = ctx.statement()

        if localVariableDeclaration != None:
            return self.visit(localVariableDeclaration)
        elif localTypeDeclaration != None:
            return self.visit(localTypeDeclaration)
        elif statement != None:
            return self.visit(statement)
        else:
            return None

    def visitStatement(self, ctx):
        # block✓ ASSERT✕ expression✓ SEMI✕ COLON✕ IF✕ parExpression✕
        # statement✕ ELSE✕ FOR✕ LPAREN✕ forControl✕ RPAREN✕ WHILE✕
        # DO✕ TRY✕ finallyBlock✕ catchClause✕ resourceSpecification✕
        # SWITCH✕ LBRACE✕ RBRACE✕ switchBlockStatementGroup✕
        # switchLabel✕ SYNCHRONIZED✕ RETURN✕ THROW✕ BREAK✕
        # identifier✕ CONTINUE✕ YIELD✕ switchExpression✕

        block = ctx.block()
        expression = ctx.expression()
        stateIF = ctx.IF()
        parExpression = ctx.parExpression()
        statement = ctx.statement()
        stateELSE = ctx.ELSE()
        stateFOR = ctx.FOR()
        stateWHILE = ctx.WHILE()
        stateDO = ctx.DO()
        stateTRY = ctx.TRY()
        finallyBlock = ctx.finallyBlock()
        catchClause = ctx.catchClause()
        stateSWITCH = ctx.SWITCH()
        switchBlockStatementGroup = ctx.switchBlockStatementGroup()
        switchLabel = ctx.switchLabel()
        stateRETURN = ctx.RETURN()
        stateTHROW = ctx.THROW()
        stateBREAK = ctx.BREAK()
        identifier = ctx.identifier()
        stateCONTINUE = ctx.CONTINUE()
        stateYIELD = ctx.YIELD()
        switchExpression = ctx.switchExpression()

        if block != None:
            return self.visit(block)

        statements = []
        expressions = []
        node = None

        if len(statement)>0:
            statements = self.visitAll(statement)

        if len(expression)>0:
            if len(expression)>1:
                expressions = self.visitAll(expression)
                print("len(statement expression>1)")
                return None
            else:
                # singular expression statement
                return self.visit(expression[0])

        return None

    def visitLocalTypeDeclaration(self, ctx):
        # classDeclaration✓ enumDeclaration✕ interfaceDeclaration✕
        # annotationTypeDeclaration✕ recordDeclaration✕ classOrInterfaceModifier✕ SEMI✕

        classDeclaration = ctx.classDeclaration()
        enumDeclaration = ctx.enumDeclaration()
        interfaceDeclaration = ctx.interfaceDeclaration()
        annotationTypeDeclaration = ctx.annotationTypeDeclaration()
        recordDeclaration = ctx.recordDeclaration()
        classOrInterfaceModifier = ctx.classOrInterfaceModifier()

        if classDeclaration != None:
            return self.visit(ctx.classDeclaration())
        elif enumDeclaration != None:
            return None
        elif interfaceDeclaration != None:
            return None
        elif annotationTypeDeclaration != None:
            return None
        elif recordDeclaration != None:
            return None
        elif len(classOrInterfaceModifier) > 0:
            return None
        else:
            return None

    def visitLocalVariableDeclaration(self, ctx):
        # typeType✕ variableDeclarators✓ VAR✕ identifier✕
        # ASSIGN✕ expression✕ variableModifier✕

        return self.visit(ctx.variableDeclarators())

    def visitVariableDeclarators(self, ctx):
        # variableDeclarator✓ COMMA✕

        node = None
        variableDeclarator = ctx.variableDeclarator()

        if len(variableDeclarator) > 1:
            # Multiple assignment
            variableNameList = []
            variableValueList = []
            variables = self.visitAll(variableDeclarator)
            for pair in variables:
                variableName, variableValue = pair
                variableNameList.append(variableName)
                variableValueList.append(variableValue)
            node = ast.Assign(targets=[ast.Tuple(elts=variableNameList, ctx=ast.Store())], value=ast.Tuple(elts=variableValueList, ctx=ast.Load()))
        else:
            # Single assignment
            variableName, variableValue = self.visit(variableDeclarator[0])
            node = ast.Assign(targets=[variableName], value=variableValue)
        return node

    def visitVariableDeclarator(self, ctx):
        # variableDeclaratorId✓ ASSIGN✕ variableInitializer✓

        variableInitializer = ctx.variableInitializer()

        variableName = self.visit(ctx.variableDeclaratorId())
        
        if variableInitializer != None:
            variableValue = self.visit(ctx.variableInitializer())
            return (ast.Name(id=variableName, ctx=ast.Store()), variableValue)
            #return ast.Assign(targets=[ast.Name(id=variableName, ctx=ast.Store())], value=variableValue)
        elif variableInitializer == None:
            return (ast.Name(id=variableName, ctx=ast.Store()), ast.Constant(value=None))
            #return ast.Assign(targets=[ast.Name(id=variableName, ctx=ast.Store())], value=None)
        else:
            return None

    def visitVariableDeclaratorId(self, ctx):
        # identifier✓ LBRACK✕ RBRACK✕

        return self.visit(ctx.identifier())

    def visitVariableInitializer(self, ctx):
        # arrayInitializer✓ expression✓

        arrayInitializer = ctx.arrayInitializer()
        expression = ctx.expression()
        if arrayInitializer != None:
            return self.visit(arrayInitializer)
        elif expression != None:
            return self.visit(expression)
        else:
            return None

    def visitArrayInitializer(self, ctx):
        # LBRACE✕ RBRACE✕ variableInitializer✓ COMMA✕
        node = ast.List(elts=self.visitAll(ctx.variableInitializer()), ctx=ast.Load())
        return node

    def visitExpression(self, ctx):
        # primary✓ methodCall✓ NEW✕ creator✓ LPAREN✕ typeType✕
        # RPAREN✕ expression✓ annotation✕ BITAND✓ ADD✓ ✓ ✓
        # DEC✓ TILDE✕ BANG✓ lambdaExpression✕ switchExpression✕
        # COLONCOLON✕ identifier✓ typeArguments✕ classType✕ MUL✓
        # DIV✓ MOD✓ LT✓ GT✓ LE✓ GE✓ EQUAL✓ NOTEQUAL✓ CARET✓ BITOR✓ AND✓
        # OR✓ COLON✕ QUESTION✕ ASSIGN✓ ADD_ASSIGN✓ SUB_ASSIGN✓
        # MUL_ASSIGN✓ DIV_ASSIGN✓ AND_ASSIGN✓ OR_ASSIGN✓
        # XOR_ASSIGN✓ RSHIFT_ASSIGN✓ URSHIFT_ASSIGN✕
        # LSHIFT_ASSIGN✓ MOD_ASSIGN✓ DOT✓ THIS✕ innerCreator✕
        # SUPER✕ superSuffix✕ explicitGenericInvocation✕
        # nonWildcardTypeArguments✕ LBRACK✓ RBRACK✓ INSTANCEOF✕ pattern✕

        primary = ctx.primary()
        methodCall = ctx.methodCall()
        creator = ctx.creator()
        expression = ctx.expression()
        annotation = ctx.annotation()
        lambdaExpression = ctx.lambdaExpression()
        switchExpression = ctx.switchExpression()
        identifier = ctx.identifier()
        
        exprLBRACK =  ctx.LBRACK() # [
        exprRBRACK = ctx.RBRACK() # [
        exprBITAND = ctx.BITAND() # &
        exprADD = ctx.ADD() # +
        exprSUB = ctx.SUB() # -
        exprINC = ctx.INC() # ++
        exprDEC = ctx.DEC() # --
        # exprTILDE = ctx.TILDE() # ~
        exprBANG = ctx.BANG() # !
        # exprCOLONCOLON = ctx.COLONCOLON() # ::
        exprMUL = ctx.MUL() # *
        exprDIV = ctx.DIV() # /
        exprMOD = ctx.MOD() # %
        exprLT = ctx.LT() # <
        exprGT = ctx.GT() # >
        exprLE = ctx.LE() # <=
        exprGE = ctx.GE() # >=
        exprEQUAL = ctx.EQUAL() # ==
        exprNOTEQUAL = ctx.NOTEQUAL() # !=
        exprCARET = ctx.CARET() # ^
        exprBITOR = ctx.BITOR() # |
        exprAND = ctx.AND() # &&
        exprOR = ctx.OR() # ||
        # exprCOLON = ctx.COLON() # :
        # exprQUESTION = ctx.QUESTION() # ?
        exprASSIGN = ctx.ASSIGN() # =
        exprADD_ASSIGN = ctx.ADD_ASSIGN() # +=
        exprSUB_ASSIGN = ctx.SUB_ASSIGN() # -=
        exprMUL_ASSIGN = ctx.MUL_ASSIGN() # *=
        exprDIV_ASSIGN = ctx.DIV_ASSIGN() # /=
        exprAND_ASSIGN = ctx.AND_ASSIGN() # &&=
        exprOR_ASSIGN = ctx.OR_ASSIGN() # ||=
        exprXOR_ASSIGN = ctx.XOR_ASSIGN() # ^=
        exprRSHIFT_ASSIGN = ctx.RSHIFT_ASSIGN() # >>=
        # exprURSHIFT_ASSIGN = ctx.URSHIFT_ASSIGN() # >>>=
        exprLSHIFT_ASSIGN = ctx.LSHIFT_ASSIGN() # <<
        exprMOD_ASSIGN = ctx.MOD_ASSIGN() # %=
        exprDOT = ctx.DOT() # .
        # exprTHIS = ctx.THIS() # this
        # exprSUPER = ctx.SUPER() # super

        expressions = []
        attrName = None
        node = None

        if exprDOT != None:
            self.astCtx == ast.Load() # Assignment context order is reversed for DOT expression (python AST.Attribute)
            if identifier != None:
                attrName = self.visit(identifier)

        if primary != None:
            return self.visit(primary)
        elif methodCall != None:
            return self.visit(methodCall)
        elif creator != None: # e.g. x = new Object()
            return self.visit(creator)

        self.astCtx = self.assignmentContext(ctx) # TODO: FIX THIS !!!

        if len(expression) > 0:
            expressions = self.visitAll(expression)

        if exprLBRACK != None: # Slice expression
            node = ast.Subscript(value=expressions[0], slice=expressions[1], ctx=self.astCtx)
        elif len(exprBITAND) > 0:
            if len(exprBITAND > 1):
                print("exprBITAND > 1")
                return None
            else:
                node = ast.BinOp(left=expressions[0], op=ast.BitAnd(), right=expressions[1])
        elif exprADD != None:
            node = ast.BinOp(left=expressions[0], op=ast.Add(), right=expressions[1])
        elif exprSUB != None:
            node = ast.BinOp(left=expressions[0], op=ast.Sub(), right=expressions[1])
        elif exprINC != None:
            node = ast.AugAssign(target=expressions[0], op=ast.Add(), value=ast.Constant(value=1))
        elif exprDEC != None:
            node = ast.AugAssign(target=expressions[0], op=ast.Sub(), value=ast.Constant(value=1))
        elif exprBANG != None:
            node = ast.UnaryOp(op=ast.Not(), operand=expressions[0])
        elif exprMUL != None:
            node = ast.BinOp(left=expressions[0], op=ast.Mult(), right=expressions[1])
        elif exprDIV != None:
            node = ast.BinOp(left=expressions[0], op=ast.Div(), right=expressions[1])
        elif exprMOD != None:
            node = ast.BinOp(left=expressions[0], op=ast.Mod(), right=expressions[1])
        elif len(exprLT) > 0:
            if len(exprLT > 1):
                print("exprLT > 1")
                return None
            else:
                node = ast.Compare(left=expressions[0], ops=ast.Lt(), comparators=expressions[1])
        elif len(exprGT) > 0:
            if len(exprGT > 1):
                print("exprGT > 1")
                return None
            else:
                node = ast.Compare(left=expressions[0], ops=ast.Gt(), comparators=expressions[1])
        elif exprLE != None:
            node = ast.Compare(left=expressions[0], ops=ast.LtE(), comparators=expressions[1])
        elif exprGE != None:
            node = ast.Compare(left=expressions[0], ops=ast.GtE(), comparators=expressions[1])
        elif exprEQUAL != None:
            node = ast.Compare(left=expressions[0], ops=ast.Eq(), comparators=expressions[1])
        elif exprNOTEQUAL != None:
            node = ast.Compare(left=expressions[0], ops=ast.NotEq(), comparators=expressions[1])
        elif exprCARET != None:
            node = ast.BinOp(left=expressions[0], op=ast.BitXor(), right=expressions[1])
        elif exprBITOR != None:
            node = ast.BinOp(left=expressions[0], op=ast.BitOr(), right=expressions[1])
        elif exprAND != None:
            node = ast.BoolOp(op=ast.And(), values=[expressions[0],expressions[1]])
        elif exprOR != None:
            node = ast.BoolOp(op=ast.Or(), values=[expressions[0],expressions[1]])
        elif exprASSIGN != None:
            #print(ast.dump(ast.Assign(targets=[expressions[0]], value=expressions[1]),indent=4))
            return ast.Assign(targets=[expressions[0]], value=expressions[1])
        elif exprADD_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.Add(), value=expressions[1])
        elif exprSUB_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.Sub(), value=expressions[1])
        elif exprMUL_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.Mult(), value=expressions[1])
        elif exprDIV_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.Div(), value=expressions[1])
        elif exprAND_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.BitAnd(), value=expressions[1])
        elif exprOR_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.BitOr(), value=expressions[1])
        elif exprXOR_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.BitXor(), value=expressions[1])
        elif exprRSHIFT_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.RShift(), value=expressions[1])
        elif exprLSHIFT_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.LShift(), value=expressions[1])
        elif exprMOD_ASSIGN != None:
            node = ast.AugAssign(target=expressions[0], op=ast.Mod(), value=expressions[1])
        elif exprDOT != None:
            node = ast.Attribute(value=expressions[0], attr=attrName, ctx=self.astCtx)
            
        self.astCtx = ast.Load()

        return node

    def visitCreator(self, ctx):
        # nonWildcardTypeArguments✕ createdName✓ classCreatorRest✓ arrayCreatorRest✓

        createdName = ctx.createdName()
        classCreatorRest = ctx.classCreatorRest()
        arrayCreatorRest = ctx.arrayCreatorRest()
        
        creatorName = self.visit(createdName)
        creatorParams = self.visit(classCreatorRest)

        creatorArgs = []
        for arg in creatorParams:
            creatorArgs.append(ast.arg(arg=str(arg.value)))

        if classCreatorRest != None:
            node = ast.Call(
                func=ast.Name(id=creatorName, ctx=ast.Load()), 
                args=creatorArgs, 
                keywords=[]
                )
            return node
        elif arrayCreatorRest != None:
            return self.visit(arrayCreatorRest)
        else:
            return None

    def visitCreatedName(self, ctx):
        # identifier✓ typeArgumentsOrDiamond✕ DOT✕ primitiveType✕

        identifier = ctx.identifier()

        if len(identifier) > 1:
            # Multiple identifiers
            print("len(createdName identifier) > 1")
            return None
        else:
            # Single identifier
            return self.visit(identifier[0])

    def visitClassCreatorRest(self, ctx):
        # arguments✓ classBody✕
        
        return self.visit(ctx.arguments())

    def visitArguments(self, ctx):
        # LPAREN✕ RPAREN✕ expressionList✓

        return self.visit(ctx.expressionList())

    def visitExpressionList(self, ctx):
        # expression✓ COMMA✕

        return self.visitAll(ctx.expression())

    def visitArrayCreatorRest(self, ctx):
        # LBRACK✕ RBRACK✕ arrayInitializer✓ expression✕

        return self.visit(ctx.arrayInitializer())

    def visitPrimary(self, ctx):
        # LPAREN✕ expression✕ RPAREN✕ THIS✕ SUPER✕ literal✓
        # identifier✓ typeTypeOrVoid✕ DOT✕ CLASS✕ nonWildcardTypeArguments✕
        # explicitGenericInvocationSuffix✕ arguments✕

        literal = ctx.literal()
        identifier = ctx.identifier()
        node = ast.Constant(value=None)

        if literal != None:
            value = self.visit(literal)
            node = ast.Constant(value=value)
        elif identifier != None:
            value = self.visit(identifier)
            node = ast.Name(id=value, ctx=self.astCtx)
        self.astCtx = ast.Load()
        return node

    def visitFieldDeclaration(self, ctx):
        # typeType✕ variableDeclarators✓ SEMI✕

        return self.visit(ctx.variableDeclarators())

    def visitIdentifier(self, ctx):
        # IDENTIFIER✓ MODULE✕ OPEN✕ REQUIRES✕ EXPORTS✕
        # OPENS✕ TO✕ USES✕ PROVIDES✕ WITH✕ TRANSITIVE✕
        # YIELD✕ SEALED✕ PERMITS✕ RECORD✕ VAR✕

        # Does not return an AST node or visit; used for identifiers in the AST, e.g. class names
        return ctx.IDENTIFIER().getText()

    def visitFormalParameters(self, ctx):
        # LPAREN✕ RPAREN✕ receiverParameter✕ COMMA✕ formalParameterList✓
        
        return self.visit(ctx.formalParameterList())
        
    def visitFormalParameterList(self, ctx):
        # formalParameter✓ COMMA✕ lastFormalParameter✕

        formalParameter = ctx.formalParameter()
        return self.visitAll(formalParameter)

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
        # identifier✓ typeArguments✕ DOT✓

        classDOT = self.visitAll(ctx.DOT())

        if len(classDOT) > 0:
            identifiers = self.visitAll(ctx.identifier())
            print("len(classDOT) > 0")
            return None
        else:
            identifier = self.visit(ctx.identifier(0))
            if identifier == "String":
                return str
            else:
                return identifier

    def visitLiteral(self, ctx):
        # integerLiteral✓ floatLiteral✓ CHAR_LITERAL✓ STRING_LITERAL✓
        # BOOL_LITERAL✓ NULL_LITERAL✓ TEXT_BLOCK✓

        integerLiteral = ctx.integerLiteral()
        floatLiteral = ctx.floatLiteral()
        litCHAR_LITERAL = ctx.CHAR_LITERAL()
        litSTRING_LITERAL = ctx.STRING_LITERAL()
        litBOOL_LITERAL = ctx.BOOL_LITERAL()
        litNULL_LITERAL = ctx.NULL_LITERAL()
        litTEXT_BLOCK = ctx.TEXT_BLOCK()

        if integerLiteral != None:
            return self.visit(integerLiteral)
        elif floatLiteral != None:
            return self.visit(floatLiteral)
        elif litCHAR_LITERAL != None:
            return self.cast(litCHAR_LITERAL.getText().strip('"'), str)
        elif litSTRING_LITERAL != None:
            return self.cast(litSTRING_LITERAL.getText().strip('"'), str)
        elif litBOOL_LITERAL != None:
            return self.cast(litBOOL_LITERAL.getText(), bool)
        elif litNULL_LITERAL != None:
            return None
        elif litTEXT_BLOCK != None:
            return self.cast(litSTRING_LITERAL.getText(), str)
        else:
            return None
    
    def visitIntegerLiteral(self, ctx):
        # DECIMAL_LITERAL✓ HEX_LITERAL✓ OCT_LITERAL✓ BINARY_LITERAL✓

        intDECIMAL_LITERAL = ctx.DECIMAL_LITERAL()
        intHEX_LITERAL = ctx.HEX_LITERAL()
        intOCT_LITERAL = ctx.OCT_LITERAL()
        intBINARY_LITERAL = ctx.BINARY_LITERAL()
        
        if intDECIMAL_LITERAL != None:
            return self.cast(intDECIMAL_LITERAL.getText(), int)
        if intHEX_LITERAL != None:
            return self.cast(intHEX_LITERAL.getText(), int)
        if intOCT_LITERAL != None:
            return self.cast(intOCT_LITERAL.getText(), int)
        if intBINARY_LITERAL != None:
            return self.cast(intBINARY_LITERAL.getText(), int)
        else:
            return None

    def visitFloatLiteral(self, ctx):
        # FLOAT_LITERAL✓ HEX_FLOAT_LITERAL✕

        floatFLOAT_LITERAL = ctx.FLOAT_LITERAL()
        floatHEX_FLOAT_LITERAL = ctx.HEX_FLOAT_LITERAL()

        if floatFLOAT_LITERAL != None:
            return self.cast(floatFLOAT_LITERAL.getText(), float)
        if floatHEX_FLOAT_LITERAL != None:
            return self.cast(floatHEX_FLOAT_LITERAL.getText(), float)
        else:
            return None

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
    
    def cast(self, value, type):
        # Cast a (string) value to another type, using type object
        if type == bool:
            return type(value.lower() == "true") # returns True if string is 'true' (case insensitive), otherwise False
        elif type != None:
            if type != str:
                # Remove "l" from end of long, "f" from end of float, "d" from end of double
                if value[-1] == "l" or value[-1] == "f" or value[-1] == "d":
                    value = value[:-1]
            return type(value)
        else:
            return None

    def assignmentContext(self, ctx):
        # Return the correct assignment context, based on the expression type
        if (ctx.INC() != None or ctx.DEC() != None or ctx.MOD_ASSIGN() != None or ctx.LSHIFT_ASSIGN() != None or
            ctx.RSHIFT_ASSIGN() != None or ctx.XOR_ASSIGN() != None or ctx.OR_ASSIGN() != None or ctx.AND_ASSIGN() != None or
            ctx.DIV_ASSIGN() != None or ctx.MUL_ASSIGN() != None or ctx.SUB_ASSIGN() != None or ctx.ASSIGN() != None or
            ctx.ADD_ASSIGN() != None):
            return ast.Store()
        else:
            return ast.Load()

        

    def visitAll(self, nodeList):
        # Visit all nodes in a list, and returns their values in a list

        visitList = []

        for nodes in nodeList:
            node = self.visit(nodes)
            visitList.append(node)

        return visitList