from yyProducer import *
class LRTableSide:
    def __init__(self, type, data):
        self.type = type  # 0-reduce, 1-shift / GOTO
        self.data = data  # reduce: producerId, shift: stateId

class LRTable:
    def __init__(self):
        self.table = []

    def __init__(self, dfa):
        for src in dfa.statesVec:
            row = {}
            for c, stateId in src.edgesMap.items():
                e = LRTableSide(1, stateId)
                row[c] = e
            for item in src.LRItemsSet:
                if item.position != producers[item.grammarIdx].second.size():
                    continue
                gid = item.grammarIdx
                if item.predictiveSymbol not in row or (row[item.predictiveSymbol].type == 0 and gid < row[item.predictiveSymbol].data):
                    row[item.predictiveSymbol] = LRTableSide(0, gid)
            self.table.append(row)

    def dump(self, print_):
        for i, row in enumerate(self.table):
            print_("%3d :  " % i)
            for c, side in row.items():
                if side.type == 0:
                    print_(" %c->r[%3d ] " % (c, side.data))
                else:
                    print_(" %c ==> %3d> " % (c, side.data))
            print_("\n")

    def code_dump(self, state_name, symbol_name):
        outer_before = "switch (" + state_name + ")	{"
        outer_after = "default: return 65536; }"
        inner = ""
        for i, row in enumerate(self.table):
            inner_before = "case " + str(i) + " : switch (" + symbol_name + ")	{"
            inner_after = "default: return 65536; }"
            tmp = ""
            for c, side in row.items():
                to = -1 - side.data if side.type == 0 else side.data
                tmp += "case " + str(c) + " :{return " + str(to) + ";}"
            inner += inner_before + tmp + inner_after
        return outer_before + inner + outer_after