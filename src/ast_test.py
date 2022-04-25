import ast
from pprint import pformat



with open("example.py", "r") as source:
        tree = ast.parse(source.read())
ast_dump = ast.dump(tree, indent=4)
with open("example_dump.txt", "w") as output:
        output.write(ast_dump)
        output.close()
print(ast_dump)