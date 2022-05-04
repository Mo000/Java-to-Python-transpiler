Basic Java to Python transpiler, using ANTLR4
Java 17 / Python 3.10

- Classes (ClassDeclaration) [EXTENDS ✓ - IMPLEMENTS ✕ - PERMITS ✕] 
    - no access modifiers (PRIVATE/PROTECTED/PUBLIC)
- Variables - (FieldDeclaration / LocalVariableDeclaration)
    - primitives: byte/int, short/int, int/int, long/int, float/float, double/float, char/str, string/str, boolean/bool
    - structures: array/list, [TODO: arrayList/list]
- Expressions
    - add (+), subtract (-), muliply (\*), divide (/), increment (++), decrement (--), not (!), mod (%), less-than (<) (<=), greater-than (>) (>=), equals (==), not-equals (!=), slice ([]), and (&&), or (||), bit-or (|), bit-xor (^), bit-and (&), bit-negation (~), assign (=), add-assign (+=), subtract-assign (-=), multiply-assign (\*=), divide-assign (/=), and-assign (&&=), or-assign (||=), xor-assign (^=), rshift-assign (>>=), lshift-assign (<<=), mod assign (%=), parenthesis (()), instanceof, creators ('new'), method-calls
- Statements
    - if (& else/else-if), for (& enhanced-for), try (& catch/finally), switch (converted to if...else), return, continue, break
- Standard Methods
    - system.out.println()

REPORT NOTES:
    Classes/Methods:
        Empty classes/methods can be translated, but are syntactically incorrect in Python
            So, body will have 'pass' appended to it, which is a Python placeholder
        Some information will be lost (e.g. 'final' parameter in Java)
    Variables:
        Python int size is *unlimited*; Java byte 8bit, short 16bit, int 32bit, long 64bit
        Python float size is 64bit; Java float 32bit, double 64bit
        Java long/float/double may have 'L', 'f', or 'd' at the end; which are removed in the translation
    Expressions:
        With parameters, operation precedence is optimised; e.g. 1+(2+3) just becomes 1+2+3
    Statements:
        For loop becomes a while loop to retain meaning, enhanced for-loop stays as a for loop
    TECHNICAL DEBT...
        Navigating (PARSE) tree
            j2py CSS-Type selectors

    Conversions aren't immediately obvious
        e.g. expression.DOT() -> ast.Attribute()
    Load/Store - assignment context for python AST
    For statements.. infinite loops, expression list, python orelse
        Should be converted to while loops in Python, except for enhanced for loops
    Multiple assignment, z = y = 0
    Standard exceptions...
    Standard methods
        differing arguments
    Switch statements
    Java empty bodies -> Python pass()
    Python 'self' is important, but not in Java...
        Java, all methods are within classes
        A simple constructor is appended to every class without a constructor, with 'self' arg and 'pass' as the body
    Using ANTLR:
        The java is not actually compiled, so incorrect Java can still be converted to some extent.
            e.g. converting an object that doesn't exist
    Tree traversal