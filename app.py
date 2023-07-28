# input

# premises = []

# while 1:
#     premise = input('Enter premise (infer when done): ')
#     if premise == 'infer': break
#     premises.append(premise)

from premiseParser import parser, reverse_parse
from collections import defaultdict
from laws import laws
display = []

# Parse a string into an AST
asts = []
# for premise in premises:
#     ast = parser.parse(premise)
#     asts.append(ast)
ast = parser.parse('p^q')
ast2 = parser.parse("(p^q)->(p->q)")
ast3 = parser.parse('(p||q)->t')
ast4 = parser.parse('~p')
ast5 = parser.parse('~(~t)')
ast6 = parser.parse('~(p->q)')
asts.append(ast.children[0])
asts.append(ast2.children[0])
asts.append(ast3.children[0])
asts.append(ast4.children[0])
asts.append(ast5.children[0])
asts.append(ast6.children[0])
facts = defaultdict() # stores fact: idx

# append initial facts
for idx, ast in enumerate(asts):
    facts[ast] = idx
    premise_string = reverse_parse(ast)
    display.append(premise_string)

print(facts)

# run the program
# final version
def apply_laws(old_facts):
    for law in laws:
        new_facts, new_fact_start_idx, descriptions = law(old_facts)
        if new_facts and descriptions:
            return new_facts, new_fact_start_idx, descriptions
      
    return None, None, None  # No laws could be applied

def solve():
    while True:
        old_facts = facts
        new_facts, new_fact_start_idx, descriptions = apply_laws(old_facts)
        
        if new_facts is None: break  # No more laws can be applied
        
        for new_fact_idx, new_fact in enumerate(new_facts):
            facts[new_fact] = new_fact_idx + new_fact_start_idx
        
        for description in descriptions:
            display.append(description)

solve()    


#fix output lining
max_width = max(len(str(idx)) + len(line.split('/')[0].rstrip()) + 1 if '/' in line else len(str(idx)) + len(line) + 1 for idx, line in enumerate(display))

for idx, line in enumerate(display):
    if '/' in line:
        left, right = line.split('/')
        new_line = f"{idx} {left.rstrip():<{max_width-len(str(idx))}}|{right}"
    else:
        new_line = f"{idx} {line:<{max_width-len(str(idx))}}"
    print(new_line)
    
# infer by steps
# steps = 4
# for _ in range(steps):
#     for law in laws:
#         old_facts = facts
#         new_facts, new_fact_start_idx, descriptions = law(old_facts) # returns [facts], fact index, ...
#         if new_facts:
#             for new_fact_idx, new_fact in enumerate(new_facts):
#                 facts[new_fact] = new_fact_idx + new_fact_start_idx
    
#         if descriptions:
#             for description in descriptions:
#                 display.append(description)


