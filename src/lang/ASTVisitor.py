from copyreg import constructor
from lang.JavaParserVisitor import JavaParserVisitor
from lang.JavaParser import JavaParser
from antlr4 import *
import ast

class ASTVisitor(JavaParserVisitor):

    # Global variables
    astCtx = ast.Load() # Set context for loading/store identifiers
    asnCtx = False # Set context for assignment expression
    methodCtx = None # Set context for method

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
        python_dump = ast.dump(python_ast, indent=4)
        # print(python_dump)
        python_code = ast.unparse(python_ast)
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
        classBody = self.emptyToPass(classBody)

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

        constructor = None
        node = None
        
        # If there is no constructor, create one with parameter 'self'
        for declaration in classBodyDeclaration:
            memberDeclaration = declaration.memberDeclaration().constructorDeclaration()
            if memberDeclaration != None:
                constructor = memberDeclaration
                
        node = self.visitAll(classBodyDeclaration)

        if constructor == None:

            simpleConstructor = ast.FunctionDef(
            name="__init__",
            args=[
                ast.arguments(
                    posonlyargs=[],
                    args=[ast.arg(arg='self')],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]
            )],
            body=[ast.Pass()],
            decorator_list=[],
            returns=[]
            )
            node.insert(0, simpleConstructor)

        return node

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
        constructorBody = self.emptyToPass(constructorBody)

        constructorArgs = [ast.arg(arg='self')]
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
        methodBody = self.emptyToPass(methodBody)
        
        methodArgs = [ast.arg(arg='self')] # As all Java methods will be within classes, they should all have 'self' arg in Python
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

        node = None

        if localVariableDeclaration != None:
            node = self.visit(localVariableDeclaration)
        elif localTypeDeclaration != None:
            node = self.visit(localTypeDeclaration)
        elif statement != None:
            node = self.visit(statement)
        return node

    def visitStatement(self, ctx):
        # block✓ ASSERT✕ expression✓ SEMI✕ COLON✕ IF✓ parExpression✓
        # statement✓ ELSE✓ FOR✓ LPAREN✕ forControl✓ RPAREN✕ WHILE✓
        # DO✕ TRY✓ finallyBlock✓ catchClause✓ resourceSpecification✕
        # SWITCH✓ LBRACE✕ RBRACE✕ switchBlockStatementGroup✓
        # switchLabel✓ SYNCHRONIZED✕ RETURN✓ THROW✕ BREAK✕
        # identifier✕ CONTINUE✓ YIELD✕ switchExpression✕

        block = ctx.block()
        expression = ctx.expression()
        identifier = ctx.identifier()
        parExpression = ctx.parExpression()
        stateIF = ctx.IF()
        statement = ctx.statement()
        stateELSE = ctx.ELSE()
        stateFOR = ctx.FOR()
        forControl = ctx.forControl()
        stateWHILE = ctx.WHILE()
        stateTRY = ctx.TRY()
        finallyBlock = ctx.finallyBlock()
        catchClause = ctx.catchClause()
        stateSWITCH = ctx.SWITCH()
        switchBlockStatementGroup = ctx.switchBlockStatementGroup()
        switchLabel = ctx.switchLabel()
        stateRETURN = ctx.RETURN()
        stateBREAK = ctx.BREAK()
        stateCONTINUE = ctx.CONTINUE()
        switchExpression = ctx.switchExpression()

        statements = []
        parenExpression = []
        node = None

        if parExpression != None:
            parenExpression = self.visit(parExpression)
        if len(statement)>0:
            statements = self.visitAll(statement)

        if stateIF != None:
            elseNode = []
            if stateELSE != None:
                elseNode = statements[1]
                if not isinstance(elseNode, list):
                    elseNode = [elseNode] # elseNode must be a list (a block returns a list, a statement does not)
            ifBody = statements[0]
            ifBody = self.emptyToPass(ifBody)
            node = ast.If(test=parenExpression, body=ifBody, orelse=elseNode)
        elif stateFOR != None:
            node = self.visit(forControl)
            if not isinstance(node, list):
                node.body.extend(statements) # Concatenate body lists
                node.body = self.emptyToPass(node.body)
            else:
                node[1].body.extend(statements)
                node[1].body.append(node[2]) # Add iterator statement to end of while loop
                node.pop() # Remove iterator from list (will be appended to while body, not method body)
                node[1].body = self.emptyToPass(node[1].body)
        elif stateWHILE != None:
            whileBody = statements[0]
            whileBody = self.emptyToPass(whileBody)
            node = ast.While(test=parenExpression, body=whileBody, orelse=[])
        elif stateTRY != None:
            # Exception types not converted
            finalBodyNode = []
            if finallyBlock != None:
                finalBodyNode = self.visit(finallyBlock)
                finalBodyNode = self.emptyToPass(finalBodyNode)
            tryBody = self.visit(block)
            tryBody = self.emptyToPass(tryBody)
            node = ast.Try(body=tryBody, handlers=self.visitAll(catchClause), orelse=[], finalbody=finalBodyNode)
        elif stateSWITCH != None:
            prevNode = []
            for i in range(len(switchBlockStatementGroup)-1,-1,-1): # Iterate backwards
                switchNode = self.visit(switchBlockStatementGroup[i])
                if hasattr(switchNode, "test"):
                    switchNode.test = ast.Compare(left=parenExpression, ops=[ast.Eq()], comparators=[switchNode.test])
                    if not isinstance(prevNode, list):
                        prevNode = [prevNode] # Ensure that prevNode is always a list
                    switchNode.orelse = prevNode
                    prevNode = switchNode
                else:
                    # Default (else) statement
                    prevNode = switchNode
            node = prevNode
        elif stateBREAK != None:
            return ast.Pass()
        elif stateRETURN != None:
            return ast.Return(value=self.visit(expression[0]))
        elif stateCONTINUE != None:
            return ast.Continue()
        elif len(expression)>0:
            if len(expression)>1:
                return self.visitAll(expression)
            else:
                if expression[0].methodCall != None: # If the statement is a method call, the resulting node will be ast.Expr()
                    return ast.Expr(value=self.visit(expression[0]))
                else:
                    return self.visit(expression[0])
        elif block != None:
            node = self.visit(block)
            
        return node

    def visitForControl(self, ctx):
        # enhancedForControl✓ SEMI✕ forInit✓ expression✓ expressionList✓

        forInit = ctx.forInit()
        expression = ctx.expression()
        expressionList = ctx.expressionList()
        enhancedForControl = ctx.enhancedForControl() # e.g. for (int x : array) {}

        node = None

        if enhancedForControl != None:
            node = self.visit(enhancedForControl)
        else:
            # Non-infinite loop
            init = self.visit(forInit)
            expr = self.visit(expression)
            exprList = self.visit(expressionList)

            # Extract values from equivalent python ast nodes
            forBody = []
            if hasattr(init.targets[0], "elts"): # Unpack multiple assignment tuples
                forTarget = init.targets[0].elts[0]
                forA = init.value.elts[0]
                
                # Add other assignments to body
                for i in range(len(init.targets[0].elts)):
                    if i == 0: continue # Skip first assignment
                    forBody.append(ast.Assign(targets=[init.targets[0].elts[i]],value=init.value.elts[i]))
            else:
                forTarget = init.targets[0]
                forA = init.value
            forB = expr.comparators[0]
            forBOp = expr.ops[0] # Lt <, Gt >, LtE <=, GtE >=
            forC = exprList[0].value

            # Convert {x=a; x<b; x+=c} to while loop
            # [variable statement, condition statement, iterator statement]
            node = [None, None, None]

            node[0] = ast.Assign(targets=[forTarget], value=forA)
            node[1] = ast.While(test=ast.Compare(left=forTarget, ops=[forBOp], comparators=[forB]),
             body=[], orelse=[])
            node[2] = ast.Assign(targets=[forTarget], value=forC)
        return node
    
    def visitEnhancedForControl(self, ctx):
        # variableDeclaratorId✓ COLON✕ expression✓ typeType✕ VAR✕ variableModifier✕

        variableDeclaratorId = ctx.variableDeclaratorId()
        expression = ctx.expression()

        var = self.visit(variableDeclaratorId)
        expr = self.visit(expression)

        node = None

        node = ast.For(target=ast.Name(id=var, ctx=ast.Load()),
         iter=expr, body=[], orelse=[])

        return node

    def visitForInit(self, ctx):
        # localVariableDeclaration✓ expressionList✕

        return self.visit(ctx.localVariableDeclaration())

    def visitSwitchBlockStatementGroup(self, ctx):
        # switchLabel✓ blockStatement✓
        # switchLabel list not handled

        switchLabel = ctx.switchLabel()[0]
        blockStatement = ctx.blockStatement()

        switchBody = self.visitAll(blockStatement)
        switchBody = self.emptyToPass(switchBody)

        node = self.visit(switchLabel)

        if hasattr(node, "body"):
            node.body = switchBody
        else:
            node = switchBody

        return node
    
    def visitSwitchLabel(self, ctx):
        # CASE✕ COLON✕ typeType✕ expression✓ IDENTIFIER✕ identifier✕ DEFAULT✓

        switchDEFAULT = ctx.DEFAULT()
        expression = ctx.expression()


        node = None
        if switchDEFAULT == None:
            labelValue = self.visit(expression)
            node = ast.If(test=labelValue, body=[], orelse=[])
        else:
            node = []
        return node
    
    def visitFinallyBlock(self, ctx):
        # FINALLY✕ block✓

        return self.visit(ctx.block())

    def visitCatchClause(self, ctx):
        # CATCH✕ LPAREN✕ catchType✓ identifier✓ RPAREN✕ block✓ variableModifier✕

        catchClauseBody = self.visit(ctx.block())
        catchClauseBody = self.emptyToPass(catchClauseBody)

        return ast.ExceptHandler(type=self.visit(ctx.catchType()),name=self.visit(ctx.identifier()),body=catchClauseBody)

    def visitCatchType(self, ctx):
        # qualifiedName✓ BITOR✕
        # List not handled
        # Exceptions not converted

        exception = self.visit(ctx.qualifiedName()[0])

        # An example of how exceptions could be converted
        if (exception == "Exception"):
            exception = "Exception"

        return ast.Name(id=exception, ctx=ast.Load())

    def visitQualifiedName(self, ctx):
        # identifier✓ DOT✕
        # List not handled
        
        return self.visit(ctx.identifier()[0])

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
        elif variableInitializer == None:
            return (ast.Name(id=variableName, ctx=ast.Store()), ast.Constant(value=None))
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

    def visitParExpression(self, ctx):
        # LPAREN✕ expression✓ RPAREN✕
        return self.visit(ctx.expression())

    def visitExpression(self, ctx):
        # primary✓ methodCall✓ NEW✕ creator✓ LPAREN✕ typeType✕
        # RPAREN✕ expression✓ annotation✕ BITAND✓ ADD✓
        # DEC✓ TILDE✓ BANG✓ lambdaExpression✕ switchExpression✕
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
        exprTILDE = ctx.TILDE() # ~
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
        exprLSHIFT_ASSIGN = ctx.LSHIFT_ASSIGN() # <<=
        exprMOD_ASSIGN = ctx.MOD_ASSIGN() # %=
        exprDOT = ctx.DOT() # .
        # exprTHIS = ctx.THIS() # this
        # exprSUPER = ctx.SUPER() # super
        exprINSTANCEOF = ctx.INSTANCEOF() # instanceof

        expressions = []
        node = None

        if methodCall != None:
            return self.identifyMethod(ctx)
        elif primary != None:
            return self.visit(primary)
        elif creator != None: # e.g. x = new Object()
            return self.visit(creator)
        self.astCtx = self.assignmentContext(ctx) # Global variable, set to ast.Store() if we are storing a value (assignment)

        if exprASSIGN != None:
            # If assignment has a dot or slice, the last, rather than the first, element must have ctx = ast.Store()
            if (expression[0].DOT() != None or expression[0].LBRACK() != None):
                self.asnCtx = True # Global variable, is True for the first child of an assignment (left hand side)
        
        if len(expression) > 0:
            expressions = self.visitAll(expression)

        if exprLBRACK != None: # Slice expression
            if (expression[0].DOT() == None and expression[0].LBRACK() == None and self.asnCtx == True):
                # If this is the last child of a slice or dot (the variable being written), and we are on the LHS of assignment
                self.astCtx = ast.Store()
                self.asnCtx = False
            node = ast.Subscript(value=expressions[0], slice=expressions[1], ctx=self.astCtx)
        elif exprDOT != None:
            if (expression[0].DOT() == None and expression[0].LBRACK() == None and self.asnCtx == True):
                self.astCtx = ast.Store()
                self.asnCtx = False
            node = ast.Attribute(value=expressions[0], attr=self.visit(ctx.getChild(2)), ctx=self.astCtx)
        elif exprASSIGN != None:
            if expression[1].ASSIGN() == None: # Single assignment, e.g. x = 0
                node = ast.Assign(targets=[expressions[0]], value=expressions[1])
            else:
                # Multiple assignment, e.g. x = y = 0
                expressions[1].targets.insert(0, expressions[0]) # Retain the assignment order
                node = expressions[1]
        elif len(exprBITAND) > 0:
            if len(exprBITAND) > 1:
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
        elif exprTILDE != None:
            node = ast.UnaryOp(op=ast.Invert(), operand=expressions[0])
        elif len(exprLT) > 0:
            if len(exprLT) > 1:
                print("exprLT > 1")
                return None
            else:
                node = ast.Compare(left=expressions[0], ops=[ast.Lt()], comparators=[expressions[1]])
        elif len(exprGT) > 0:
            if len(exprGT) > 1:
                print("exprGT > 1")
                return None
            else:
                node = ast.Compare(left=expressions[0], ops=[ast.Gt()], comparators=[expressions[1]])
        elif exprLE != None:
            node = ast.Compare(left=expressions[0], ops=[ast.LtE()], comparators=[expressions[1]])
        elif exprGE != None:
            node = ast.Compare(left=expressions[0], ops=[ast.GtE()], comparators=[expressions[1]])
        elif exprEQUAL != None:
            node = ast.Compare(left=expressions[0], ops=[ast.Eq()], comparators=[expressions[1]])
        elif exprNOTEQUAL != None:
            node = ast.Compare(left=expressions[0], ops=[ast.NotEq()], comparators=[expressions[1]])
        elif exprCARET != None:
            node = ast.BinOp(left=expressions[0], op=ast.BitXor(), right=expressions[1])
        elif exprBITOR != None:
            node = ast.BinOp(left=expressions[0], op=ast.BitOr(), right=expressions[1])
        elif exprAND != None:
            node = ast.BoolOp(op=ast.And(), values=[expressions[0],expressions[1]])
        elif exprOR != None:
            node = ast.BoolOp(op=ast.Or(), values=[expressions[0],expressions[1]])
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
        elif exprINSTANCEOF != None:
            child1 = self.visit(ctx.getChild(0))
            child2 = ast.Name(id=self.visit(ctx.getChild(2)),ctx=ast.Load())
            node = ast.Call(func=ast.Name(id='isinstance', ctx=ast.Load()), args=[child1, child2], keywords=[])
            
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

        expressionList = ctx.expressionList()
        
        node = []

        if expressionList != None:
            node = self.visit(expressionList)
        return node

    def visitExpressionList(self, ctx):
        # expression✓ COMMA✕

        return self.visitAll(ctx.expression())

    def visitArrayCreatorRest(self, ctx):
        # LBRACK✕ RBRACK✕ arrayInitializer✓ expression✕

        return self.visit(ctx.arrayInitializer())

    def visitPrimary(self, ctx):
        # LPAREN✕ expression✓ RPAREN✕ THIS✓ SUPER✓ literal✓
        # identifier✓ typeTypeOrVoid✕ DOT✕ CLASS✕ nonWildcardTypeArguments✕
        # explicitGenericInvocationSuffix✕ arguments✕

        literal = ctx.literal()
        identifier = ctx.identifier()  
        expression = ctx.expression()
        exprTHIS = ctx.THIS()
        exprSUPER = ctx.SUPER()

        node = ast.Constant(value=None)
        
        if exprTHIS != None:
            node = ast.Name(id="self", ctx=self.astCtx)
        if exprSUPER != None:
            node = ast.Name(id="super", ctx=self.astCtx)
        elif expression != None: # Parenthesis
            node = self.visit(expression)
        elif literal != None:
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

        formalParameterList = ctx.formalParameterList()

        node = []

        if formalParameterList != None:
            node = self.visit(formalParameterList)
        
        return node
        
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
            return "bool"
        elif CHAR != None:
            return "str"
        elif BYTE != None:
            return "int"
        elif SHORT != None:
            return "int"
        elif INT != None:
            return "int"
        elif LONG != None:
            return "int"
        elif FLOAT != None:
            return "float"
        elif DOUBLE != None:
            return "float"
        else:
            return None

    
    def visitMethodCall(self, ctx):
        # identifier✕ expressionList✓ LPAREN✕ RPAREN✕ THIS✓ SUPER✓
        
        expressionList = ctx.expressionList()

        node = None
        argsList = None
        funcNode = None
        objectArg = self.methodCtx[2]

        if self.methodCtx == None:
            print("No method context")
            return ast.Pass()
        if expressionList == None:
            argsList = []
        else:
            argsList = self.visit(expressionList)
            
        if objectArg != None:
            argsList.insert(0, self.visit(objectArg))

        methodNames = self.methodCtx[0] # e.g. Name of the method object/attributes (i.e. separated by dots)
        methodName = self.methodCtx[1] # Name of the method with parens ()
        
        if self.methodCtx[0] != "": # method of attribute
            nameList = methodNames.split(".")
            # Create first node from first name in nameList
            prevNode = ast.Name(id=nameList[0], ctx=ast.Load())
            nameList.pop(0)
            # Add method name as last name in nameList
            nameList.append(methodName)
            # Iterate over the rest of nameList to append each name as an attribute
            for name in nameList:
                funcNode = ast.Attribute(value=prevNode, attr=name, ctx=ast.Load())
                prevNode = funcNode
        else:
            funcNode = ast.Name(id=methodName, ctx=ast.Load())

        node = ast.Call(func=funcNode, args=argsList, keywords=[])

        return node
    
    def identifyMethod(self, ctx):
        # Identify a method by expression and methodCall identifiers

        expression = ctx.expression()
        methodCall = ctx.methodCall()
        convertedMethod = None

        if len(expression) > 0:
            if len(expression) > 1:
                print("len(expression) > 1")
                return None
            exprTxt = expression[0].getText()
        else:
            exprTxt = "self" # If there's no object, then it must be referencing a method within its own class, so use 'self'
        if methodCall.SUPER() == None: # "THIS" and "SUPER" can be used as methods, without an object
            if methodCall.THIS() == None:
                methodTxt = self.visit(methodCall.identifier())
            else:
                exprTxt = ""
                methodTxt = "this"
        else:
            exprTxt = ""
            methodTxt = "super"

        # [javaExpr (string), javaMethod (string), pythonExpr (string), pythonMethod (string), args]
        simpleConversionList = [
            ["System.out", "println", "", "print", ""],
            ["", "super", "", "super", ""],
            ["", "this", "", "self", ""],
        ]

        objectConversionList = [
            ["object", "length", "", "len", ""],
        ]
        for conversion in simpleConversionList:
            convertedMethod = self.convertMethod(exprTxt, methodTxt, conversion[0], conversion[1], conversion[2], conversion[3])
            if convertedMethod != None: # Found method
                break

        if convertedMethod == None:
            for conversion in objectConversionList: # Check objectConversionList if not found in simpleConversionList
                convertedMethod = self.convertMethod("object", methodTxt, conversion[0], conversion[1], conversion[2], conversion[3])
                if convertedMethod != None:
                    convertedMethod[2] = expression[0] # Add object as argument (e.g. str1.length -> len(str1))
                    break

        if convertedMethod == None:
            convertedMethod = [exprTxt, methodTxt, None] # No conversion, if no method is found

        self.methodCtx = convertedMethod # Set the global method context

        return self.visit(methodCall)

    def convertMethod(self, expression, methodCall, javaExpr, javaMethod, pythonExpr, pythonMethod):
        newMethod = None
        if (expression == javaExpr and methodCall == javaMethod):
            newMethod = [pythonExpr, pythonMethod, None]
        return newMethod
    
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

    def emptyToPass(self, list): # Converts empty lists to ast.Pass() for bodies
        if list == []:
            list = [ast.Pass()]
        return list

    def visitAll(self, nodeList):
        # Visit all nodes in a list, and returns their values in a list

        visitList = []

        for nodes in nodeList:
            node = self.visit(nodes)
            if isinstance(node, list):
                # if one node returns a list of nodes, unpack it
                visitList.extend(node)
            else:
                visitList.append(node)

        return visitList