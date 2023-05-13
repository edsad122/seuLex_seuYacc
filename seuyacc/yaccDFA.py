from yyProducer import *

firsts: Dict[int, Set[int]] = {}

def init_firsts():
    global firsts
    for p_ in producers:
        for s in p_[1]:
            if is_terminator(s):
                firsts.setdefault(s, set()).add(s)
    
    flag = True
    while flag:
        flag = False
        for p_ in producers:
            s = p_[0]
            if is_terminator(s):
                continue
            has_epsilon = True
            for item in p_[1]:
                this_set = firsts[item]
                for c in this_set:
                    if c == 0:
                        continue
                    if c not in firsts[s]:
                        flag = True
                        firsts[s].add(c)
                if 0 not in this_set:
                    has_epsilon = False
                    break
            if has_epsilon and 0 not in firsts[s]:
                flag = True
                firsts[s].add(0)