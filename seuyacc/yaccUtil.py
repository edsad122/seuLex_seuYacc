from yaccDFA import *
init_firsts()
from collections import deque
class LRItem:
    def __init__(self):
        self.position = 0
        self.gramarIdx = -1
        self.predictiveSymbol = None

    def __lt__(self, other):
        if self.gramarIdx == other.gramarIdx:
            if self.position == other.position:
                return self.predictiveSymbol < other.predictiveSymbol
            return self.position < other.position
        return self.gramarIdx < other.gramarIdx

class LRState:
    def __init__(self):
        self.idx = -1
        self.edgesMap = {}
        self.LRItemsSet = set()

    def extend(self):
        s = self
        que = deque(s.LRItemsSet)
        while que:
            item = que.popleft()
            producer = producers[item.gramarIdx]
            itemLen = len(producer[1])
            if item.position >= itemLen:
                continue
            if is_terminator(producer[1][item.position]):
                continue
            newLeft = producer[1][item.position]
            nexts = set()
            flag = True
            for j in range(item.position + 1, itemLen):
                noEpsilon = True
                fi = firsts[producer[1][j]]
                for c in fi:
                    if c == 0:
                        noEpsilon = False
                    else:
                        nexts.add(c)
                if noEpsilon:
                    flag = False
                    break
            if flag:
                nexts.add(item.predictiveSymbol)
            for i in range(len(producers)):
                if producers[i][0] != newLeft:
                    continue
                for c in nexts:
                    newItem = LRItem()
                    newItem.gramarIdx = i
                    newItem.position = 0
                    newItem.predictiveSymbol = c
                    if newItem not in s.LRItemsSet:
                        s.LRItemsSet.add(newItem)
                        que.append(newItem)

class LRDFA:
    def __init__(self):
        self.startState = 0
        self.statesVec = []

        dfa = self

        item0 = LRItem()
        item0.gramarIdx = 0
        item0.predictiveSymbol = '$'
        state0 = LRState()
        state0.LRItemsSet.add(item0)

        init_firsts()

        state0.extend()

        state0.idx = 0

        dfa.startState = 0
        dfa.statesVec.append(state0)

        que = deque()
        que.append(0)
        while que:
            idx = que.popleft()
            start = dfa.statesVec[idx]
            newStates = {}
            for item in start.LRItemsSet:
                producer = producers[item.gramarIdx]
                if item.position >= len(producer[1]):
                    continue
                c = producer[1][item.position]
                newItem = LRItem()
                newItem.position = item.position + 1
                newItem.gramarIdx = item.gramarIdx
                newStates.setdefault(c, LRState()).LRItemsSet.add(newItem)
            for p_, state in newStates.items():
                state.extend()
            for p_, state in newStates.items():
                start = dfa.statesVec[idx]
                flag = True
                for other in dfa.statesVec:
                    if len(state.LRItemsSet) != len(other.LRItemsSet):
                        continue
                    same = True
                    for item in state.LRItemsSet:
                        if item not in other.LRItemsSet:
                            same = False
                            break
                        if same:
                            start.edgesMap[p_] = other.idx
                            flag = False
                            break
                    if flag:
                        c = p_
                        idx = len(dfa.statesVec)
                        start.edgesMap[c] = idx
                        state.idx = idx
                        dfa.statesVec.append(state)
                        que.append(idx)
    def generateLALR(self):
        n = len(self.statesVec)
        stateBelongs = [-1] * 65536
        for i in range(n):
            if stateBelongs[i] != -1:
                continue
            stateBelongs[i] = i
            for j in range(i + 1, n):
                if stateBelongs[j] != -1:
                    continue
                isSame = True
                for item1 in self.statesVec[i].LRItemsSet:
                    flag = False
                    for item2 in self.statesVec[j].LRItemsSet:
                        if item1.gramarIdx == item2.gramarIdx and item1.position == item2.position:
                            flag = True
                            break
                    if not flag:
                        isSame = False
                        break
                for item1 in self.statesVec[j].LRItemsSet:
                    flag = False
                    for item2 in self.statesVec[i].LRItemsSet:
                        if item1.gramarIdx == item2.gramarIdx and item1.position == item2.position:
                            flag = True
                            break
                    if not flag:
                        isSame = False
                        break
                if isSame:
                    stateBelongs[j] = i
        cnt = 0
        stateCnts = [0] * 65536
        for i in range(n):
            if stateBelongs[i] == i:
                stateCnts[i] = cnt
                cnt += 1
        newVec = []
        for i in range(n):
            if i != stateBelongs[i]:
                continue
            newState = self.statesVec[i]
            for p_, state in newState.edgesMap.items():
                newState.edgesMap[p_] = stateCnts[stateBelongs[state]]
            newVec.append(newState)
        self.statesVec = newVec