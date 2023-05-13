from DFA import *
from NFA import *
class RegToDFA:
    def __init__(self):
        self.nodes = 0
        self.flag_map = {}
        self.flagCnt = 10
        self.startNode = None
        self.reg = [0] * 65536

    def init(self):
        for i in range(9, 127):
            if i != '#':
                allowed_chars.append(i)
        self.FA_flag = [0] * 65536

    def appendRegex(self, regStr, info):
        self.reg = list(regStr)
        #如果flag为空
        if self.flag_map == {}:
            self.startNode=parseFirstReg(self.reg, self.startNode, self.flagCnt)
        else:
            parseReg(self.reg, self.startNode, self.flagCnt)
        self.flag_map[self.flagCnt] = info
        self.flagCnt += 1

    def generate(self):
        states = NFAtoDFA(self.startNode)
        DFAMinimizer.init(states)
        DFAMinimizer.deal()
        self.nodes = DFAMinimizer.generate()

    def show(self):
        for i in range(self.nodes):
            print(f"{i:3d} :  [ {minDFA[i].flag:4d} ] ", end="")
            for p_ in minDFA[i].ptrs:
                print(f" < {p_[0]} , {p_[1].id:3d} >", end="")
            print("\n\n")