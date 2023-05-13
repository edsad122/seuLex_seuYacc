class DFANode:
    def __init__(self):
        self.id = 0
        self.flag = 0
        self.ptrs = {}

DFANodes = [DFANode() for _ in range(65536)]
minDFA = [DFANode() for _ in range(65536)]

class DFAMinimizerClass:
    def __init__(self):
        self.DFASets = []
        self.DFANodeIdx = [0] * 65536

    def init(self, stateCnt):
        initialSets = {}
        for i in range(stateCnt):
            dfatype = DFANodes[i].flag
            if dfatype not in initialSets:
                initialSets[dfatype] = set()
            initialSets[dfatype].add(i)
        
        for p_ in initialSets.items():
            self.DFASets.append(p_[1])
            for idx in p_[1]:
                self.DFANodeIdx[idx] = len(self.DFASets) - 1

    def deal(self):
        last_size = 0
        z = 0
        while len(self.DFASets) != last_size:
            last_size = len(self.DFASets)
            for i in range(len(self.DFASets)):
                curSet = self.DFASets[i]
                splitedSet = set()
                stde = next(iter(curSet))
                stdtable = DFANodes[stde].ptrs
                
                for e in curSet:
                    table = DFANodes[e].ptrs
                    notSame = False
                    if len(stdtable) == len(table):
                        for p_ in stdtable.items():
                            if p_[0] not in table or self.DFANodeIdx[p_[1].id] != self.DFANodeIdx[table[p_[0]].id]:
                                notSame = True
                                break
                    else:
                        notSame = True
                    
                    if notSame:
                        splitedSet.add(e)
                
                if splitedSet:
                    self.DFASets.append(splitedSet)
                    newIdx = len(self.DFASets) - 1
                    for e in splitedSet:
                        self.DFASets[i].remove(e)
                        self.DFANodeIdx[e] = newIdx

    def show(self):
        for i in range(len(self.DFASets)):
            print(f"{i:3} : ", end="")
            for j in self.DFASets[i]:
                print(f"{j:5}", end="")
            print()

    def generate(self):
        for i in range(len(self.DFASets)):
            minDFA[i].id = i
            e = next(iter(self.DFASets[i]))
            minDFA[i].flag = DFANodes[e].flag
            for p_ in DFANodes[e].ptrs.items():
                c = p_[0]
                idx = self.DFANodeIdx[p_[1].id]
                minDFA[i].ptrs[c] = minDFA[idx]
        
        return len(self.DFASets)

DFAMinimizer = DFAMinimizerClass()