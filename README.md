Basic Java to Python transpiler, using ANTLR4
Java 17 / Python 3.10

- Classes (ClassDeclaration) [EXTENDS ✓ - IMPLEMENTS ✕ - PERMITS ✕] 
    - No access modifiers (PRIVATE/PROTECTED/PUBLIC)
- Variables - (FieldDeclaration / LocalVariableDeclaration)
    - Primitives: byte/int, short/int, int/int, long/int, float/float, double/float, char/str, string/str, boolean/bool
    - Structures: array/list, arrayList/list

REPORT NOTES:
    Classes/Methods:
        Empty classes/methods can be translated, but are syntactically incorrect in Python
        Some information will be lost (e.g. 'final' parameter in Java)
    Variables:
        Python int size is *unlimited*; Java byte 8bit, short 16bit, int 32bit, long 64bit
        Python float size is 64bit; Java float 32bit, double 64bit
        Java long/float/double may have 'L', 'f', or 'd' at the end; which are removed in the translation
    
    TECHNICAL DEBT...
        Navigating (PARSE) tree
            j2py CSS-Type selectors