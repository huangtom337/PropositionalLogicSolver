from premiseParser import reverse_parse


def modus_ponens(old_facts):

    for ast in old_facts:
        op = ast[0]
        if op == 'implies':
            var_p, var_q = ast[1], ast[2]
            if var_q in old_facts: continue # inference already exists
            
            if var_p in old_facts:
                var_p_idx = old_facts[var_p]
                var_p_str = reverse_parse(var_q)
                description = f'{var_p_str}/ modus ponens {var_p_idx} {old_facts[ast]}'
                return [var_q], len(old_facts), [description]
                 
   # not applicable
    return None, None, None

def double_negation(old_facts):
    
    for ast in old_facts:
        op = ast[0]
        if op == 'not':
            not_var_p = ast[1]
            if not_var_p[0] == 'not':
                var_p = not_var_p[1]
                if var_p in old_facts: continue # inference already exists

                var_p_str = reverse_parse(var_p)
                description = f'{var_p_str}/ double negation {old_facts[ast]}'
                return [var_p], len(old_facts), [description]
            
    return None, None, None

def simplification(old_facts):

    for ast in old_facts:
        op = ast[0]
        if op == 'and':
            var_p, var_q = ast[1], ast[2]
            if var_p and var_q in old_facts: continue # both inferences already exist
                                                      # not accounting if only one exist
            p, q = reverse_parse(var_p), reverse_parse(var_q) 
            description1 = f'{p}/ simplification {old_facts[ast]}'
            description2 = f'{q}/ simplification {old_facts[ast]}'
            return [var_p, var_q], len(old_facts), [description1, description2]
        
    return None, None, None

def modus_tollens(old_facts):
    
    for ast in old_facts:
        op = ast[0]
        if op == 'implies':
            var_p, var_q = ast[1], ast[2]
            not_var_p = ('not', var_p)
            if not_var_p in old_facts: continue # inference already exists
            
            not_var_q = ('not', var_q)
            if not_var_q in old_facts:
                not_var_q_idx = old_facts[not_var_q]
                not_var_p_str = reverse_parse(not_var_p)
                description = f'{not_var_p_str}/ modus tollens {not_var_q_idx} {old_facts[ast]}'
                return [not_var_p], len(old_facts), [description]
            
    return None, None, None

laws = [modus_ponens, double_negation, simplification, modus_tollens]