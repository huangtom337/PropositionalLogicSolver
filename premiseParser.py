# parser

from lark import Lark, Transformer, v_args

# Define the grammar
grammar = """
    start: expr
    expr: NAME                  -> var
         | expr "->" expr       -> implies
         | "(" expr ")"         -> parens
         | expr "^" expr        -> andcomparison
         | expr "||" expr        -> orcomparison
         | "~" expr             -> notoperator
    NAME: /[a-z]+/
    %import common.WS           // import common whitespace
    %ignore WS                  // ignore it
"""

# Define a transformer to process the AST
class MyTransformer(Transformer):
    def var(self, items):
        return ('var', str(items[0]))

    def implies(self, items):
        return ('implies', items[0], items[1])

    def parens(self, items):
        return items[0]

    def andcomparison(self, items):
        return ('and', items[0], items[1])
    
    def orcomparison(self, items):
        return ('or', items[0], items[1])
    
    def notoperator(self, items):
        return ('not', items[0])

# Initialize the parser
parser = Lark(grammar, parser='lalr', transformer=MyTransformer())

# Reverse-parse the AST back into a string
def reverse_parse(node):
    if isinstance(node, tuple):
        if node[0] == 'implies':
            return '(' + reverse_parse(node[1]) + ')' + '->' + '(' + reverse_parse(node[2]) + ')'
        elif node[0] == 'and':
            return '(' + reverse_parse(node[1]) + ')' + '^' + '(' + reverse_parse(node[2]) + ')'
        elif node[0] == 'or':
            return '(' + reverse_parse(node[1]) + ')' + '||' + '(' + reverse_parse(node[2]) + ')'
        elif node[0] == 'not':
            return '~' + '(' + reverse_parse(node[1]) + ')'
        elif node[0] == 'var':
            return node[1]
    return str(node)

