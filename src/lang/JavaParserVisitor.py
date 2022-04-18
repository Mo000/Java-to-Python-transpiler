# Generated from JavaParser.g4 by ANTLR 4.10.1
from antlr4 import *
import ast

# This class defines a complete generic visitor for a parse tree produced by JavaParser.

class JavaParserVisitor(ParseTreeVisitor):
    path = [] # Path down the tree, containing all nodes with bodies
    python_ast = ast.parse('')
    # Visit a parse tree produced by JavaParser#compilationUnit.
    def visitCompilationUnit(self, ctx):
        self.path.append(self.python_ast.body) # AST root
        self.visitChildren(ctx)
        self.path.pop() # Nodes are removed from path after all children are visited

        ast.fix_missing_locations(self.python_ast) # Add line numbers

        #Save file
        python_code = ast.unparse(self.python_ast)
        python_dump = ast.dump(self.python_ast, indent=4)
        print(python_dump)
        with open("translation.py", "w") as output:
            output.write(python_code)
            output.close()
        with open("translation_dump.txt", "w") as output:
            output.write(python_dump)
            output.close()



    # Visit a parse tree produced by JavaParser#packageDeclaration.
    def visitPackageDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#importDeclaration.
    def visitImportDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#modifier.
    def visitModifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classOrInterfaceModifier.
    def visitClassOrInterfaceModifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableModifier.
    def visitVariableModifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classDeclaration.
    def visitClassDeclaration(self, ctx):
        child_count = int(ctx.getChildCount())
        if child_count >3:
            # extends, implements, or permits
            # c0 = ctx.getChild(0)  # class
            c1 = ctx.getChild(1).getText()  # class name
            c2 = ctx.getChild(2).getText()  #  extends/implements/permits
            if c2 == 'extends':
                c3 = ctx.getChild(3).getChild(0).getText()  # extends class name
            # implements/permits not implemented
            node = ast.ClassDef(name=c1,bases=[ast.Name(c3, ast.Load())],keywords=[],body=[],decorator_list=[])
        else:
            c1 = ctx.getChild(1).getText()  # class name
            node = ast.ClassDef(name=c1,bases=[],keywords=[],body=[],decorator_list=[])
        self.path[-1].insert(len(self.path[-1]), node)
        self.path.append(self.path[-1][-1].body)
        self.visitChildren(ctx)
        self.path.pop()


    # Visit a parse tree produced by JavaParser#typeParameters.
    def visitTypeParameters(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeParameter.
    def visitTypeParameter(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeBound.
    def visitTypeBound(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumDeclaration.
    def visitEnumDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumConstants.
    def visitEnumConstants(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumConstant.
    def visitEnumConstant(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumBodyDeclarations.
    def visitEnumBodyDeclarations(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceDeclaration.
    def visitInterfaceDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classBody.
    def visitClassBody(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceBody.
    def visitInterfaceBody(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classBodyDeclaration.
    def visitClassBodyDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#memberDeclaration.
    def visitMemberDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodBody.
    def visitMethodBody(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeTypeOrVoid.
    def visitTypeTypeOrVoid(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#genericMethodDeclaration.
    def visitGenericMethodDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#genericConstructorDeclaration.
    def visitGenericConstructorDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constructorDeclaration.
    def visitConstructorDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceBodyDeclaration.
    def visitInterfaceBodyDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMemberDeclaration.
    def visitInterfaceMemberDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constDeclaration.
    def visitConstDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constantDeclarator.
    def visitConstantDeclarator(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def visitInterfaceMethodDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMethodModifier.
    def visitInterfaceMethodModifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#genericInterfaceMethodDeclaration.
    def visitGenericInterfaceMethodDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceCommonBodyDeclaration.
    def visitInterfaceCommonBodyDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableDeclarators.
    def visitVariableDeclarators(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableDeclarator.
    def visitVariableDeclarator(self, ctx):
        # CONSTANT INT ASSIGN - TODO: variable -> other types
        c0 = ctx.getChild(0).getText()  # variable name
        c1 = ctx.getChild(1).getText()  # operator (=)
        c2 = ctx.getChild(2).getText()  # value
        node = ast.Assign(
            targets=[ast.Name(id=c0, ctx=ast.Store())],
            value=ast.Constant(value=int(c2)))
        self.path[-1].insert(len(self.path[-1]), node)
        self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableDeclaratorId.
    def visitVariableDeclaratorId(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableInitializer.
    def visitVariableInitializer(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayInitializer.
    def visitArrayInitializer(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classOrInterfaceType.
    def visitClassOrInterfaceType(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArgument.
    def visitTypeArgument(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#qualifiedNameList.
    def visitQualifiedNameList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#formalParameters.
    def visitFormalParameters(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#receiverParameter.
    def visitReceiverParameter(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#formalParameterList.
    def visitFormalParameterList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#formalParameter.
    def visitFormalParameter(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lastFormalParameter.
    def visitLastFormalParameter(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaLVTIList.
    def visitLambdaLVTIList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaLVTIParameter.
    def visitLambdaLVTIParameter(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#qualifiedName.
    def visitQualifiedName(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#literal.
    def visitLiteral(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#integerLiteral.
    def visitIntegerLiteral(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#floatLiteral.
    def visitFloatLiteral(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#altAnnotationQualifiedName.
    def visitAltAnnotationQualifiedName(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotation.
    def visitAnnotation(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValuePairs.
    def visitElementValuePairs(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValuePair.
    def visitElementValuePair(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValue.
    def visitElementValue(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValueArrayInitializer.
    def visitElementValueArrayInitializer(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationTypeDeclaration.
    def visitAnnotationTypeDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationTypeBody.
    def visitAnnotationTypeBody(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationTypeElementDeclaration.
    def visitAnnotationTypeElementDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationTypeElementRest.
    def visitAnnotationTypeElementRest(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationMethodOrConstantRest.
    def visitAnnotationMethodOrConstantRest(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationMethodRest.
    def visitAnnotationMethodRest(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationConstantRest.
    def visitAnnotationConstantRest(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#defaultValue.
    def visitDefaultValue(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#moduleDeclaration.
    def visitModuleDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#moduleBody.
    def visitModuleBody(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#moduleDirective.
    def visitModuleDirective(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#requiresModifier.
    def visitRequiresModifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordDeclaration.
    def visitRecordDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordHeader.
    def visitRecordHeader(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordComponentList.
    def visitRecordComponentList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordComponent.
    def visitRecordComponent(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordBody.
    def visitRecordBody(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#block.
    def visitBlock(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#blockStatement.
    def visitBlockStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#localVariableDeclaration.
    def visitLocalVariableDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#identifier.
    def visitIdentifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#localTypeDeclaration.
    def visitLocalTypeDeclaration(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#statement.
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catchClause.
    def visitCatchClause(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catchType.
    def visitCatchType(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#finallyBlock.
    def visitFinallyBlock(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resourceSpecification.
    def visitResourceSpecification(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resources.
    def visitResources(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resource.
    def visitResource(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchBlockStatementGroup.
    def visitSwitchBlockStatementGroup(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchLabel.
    def visitSwitchLabel(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forControl.
    def visitForControl(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forInit.
    def visitForInit(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enhancedForControl.
    def visitEnhancedForControl(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#parExpression.
    def visitParExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expressionList.
    def visitExpressionList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodCall.
    def visitMethodCall(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expression.
    def visitExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#pattern.
    def visitPattern(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaExpression.
    def visitLambdaExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaParameters.
    def visitLambdaParameters(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaBody.
    def visitLambdaBody(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#primary.
    def visitPrimary(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchExpression.
    def visitSwitchExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchLabeledRule.
    def visitSwitchLabeledRule(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#guardedPattern.
    def visitGuardedPattern(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchRuleOutcome.
    def visitSwitchRuleOutcome(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classType.
    def visitClassType(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#creator.
    def visitCreator(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#createdName.
    def visitCreatedName(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#innerCreator.
    def visitInnerCreator(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayCreatorRest.
    def visitArrayCreatorRest(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classCreatorRest.
    def visitClassCreatorRest(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#explicitGenericInvocation.
    def visitExplicitGenericInvocation(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArgumentsOrDiamond.
    def visitTypeArgumentsOrDiamond(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#nonWildcardTypeArgumentsOrDiamond.
    def visitNonWildcardTypeArgumentsOrDiamond(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#nonWildcardTypeArguments.
    def visitNonWildcardTypeArguments(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeList.
    def visitTypeList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeType.
    def visitTypeType(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#primitiveType.
    def visitPrimitiveType(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArguments.
    def visitTypeArguments(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#superSuffix.
    def visitSuperSuffix(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#explicitGenericInvocationSuffix.
    def visitExplicitGenericInvocationSuffix(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arguments.
    def visitArguments(self, ctx):
        return self.visitChildren(ctx)


