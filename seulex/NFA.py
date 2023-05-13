from typing import List, Set, Dict, Tuple
from DFA import *
global allowed_chars
allowed_chars: List[str] = []
CHAR_NULL=127
class NFANode:
    def __init__(self):
        self.id: int = 0
        self.input1: str = chr(CHAR_NULL)
        self.next1: NFANode = None
        self.input2: str = chr(CHAR_NULL)
        self.next2: NFANode = None

FA_flag: List[int] = [0] * 65536

NFANodes: List[NFANode] = [NFANode() for _ in range(65536)]

NFANodesPtr: int = 0

def newNFANode() -> NFANode:
    global NFANodesPtr
    NFANodes[NFANodesPtr].id = NFANodesPtr
    NFANodesPtr += 1
    return NFANodes[NFANodesPtr - 1]

op_stack: List[str] = []
node_stack: List[Tuple[NFANode, NFANode]] = []

def NFA_pop_node_by_op(op: str) -> None:
    pair_ = node_stack[-1]
    start, end = pair_
    if op == '|':
        node_stack.pop()
        pair2 = node_stack[-1]
        start2, end2 = pair2
        newStart = newNFANode()
        newEnd = newNFANode()
        newStart.input1 = newStart.input2 = '\0'
        newStart.next1 = start
        newStart.next2 = start2
        end.input1 = end2.input1 = '\0'
        end.next1 = end2.next1 = newEnd
        node_stack.pop()
        node_stack.append((newStart, newEnd))
    elif op == '\0':
        node_stack.pop()
        pair2 = node_stack[-1]
        start2, end2 = pair2
        end2.input1 = start.input1
        end2.next1 = start.next1
        end2.input2 = start.input2
        end2.next2 = start.next2
        node_stack.pop()
        node_stack.append((start2, end))
    elif op == '?' or op == '+' or op == '*':
        newStart = newNFANode()
        newEnd = newNFANode()
        newStart.input1 = '\0'
        newStart.next1 = start
        end.input1 = '\0'
        end.next1 = newEnd
        if op != '?':
            end.input2 = '\0'
            end.next2 = start
        if op != '+':
            newStart.input2 = '\0'
            newStart.next2 = newEnd
        node_stack.pop()
        node_stack.append((newStart, newEnd))
    else:
        print("error op")

def newRegInput(reg: str) -> Tuple[NFANode, NFANode]:
    global op_stack, node_stack
    op_stack = []
    node_stack = []
    ptr = 0
    cur = reg[int(ptr)]
    initNode = newNFANode()
    node_stack.append((initNode, initNode))

    while cur != '\0':
        if cur != '\\':
            if cur == '(' or cur == '|':
                if cur == '|':
                    op = op_stack[-1]
                    while op != '(':
                        NFA_pop_node_by_op(op)
                        op_stack.pop()
                        if len(op_stack) == 0:
                            break
                        else:
                            op = op_stack[-1]
                op_stack.append(cur)
                newInit = newNFANode()
                node_stack.append((newInit, newInit))
            elif cur == ')' or cur == '\0':
                op = op_stack[-1]
                while op != '(':
                    NFA_pop_node_by_op(op)
                    op_stack.pop()
                    if len(op_stack) == 0:
                        break
                    else:
                        op = op_stack[-1]
                if op == '(':
                    op_stack.pop()
                    op_stack.append('\0')
            elif cur == '+' or cur == '?' or cur == '*':
                op_stack.append(cur)
                NFA_pop_node_by_op(cur)
                op_stack.pop()
            else:
                op_stack.append('\0')
                newStart = newNFANode()
                newEnd = newNFANode()
                newStart.input1 = cur
                newStart.next1 = newEnd
                node_stack.append((newStart, newEnd))
        else:
            ptr += 1
            cur = reg[ptr]
            if cur != '\0':
                op_stack.append('\0')
                newStart = newNFANode()
                newEnd = newNFANode()
                newStart.input1 = cur
                newStart.next1 = newEnd
                node_stack.append((newStart, newEnd))

        ptr += 1
        if ptr== len(reg):
            break
        cur = reg[ptr]

    while len(op_stack) > 0:
        op = op_stack[-1]
        NFA_pop_node_by_op(op)
        op_stack.pop()

    pair_ = node_stack[-1]
    start, end = pair_

    return start, end

def parseReg(reg: str, startNode: NFANode, flag: int) -> None:
    pair_ = newRegInput(reg)
    nextStart = pair_[0]
    pastStart = newNFANode()
    pastStart.input1 = startNode.input1
    pastStart.next1 = startNode.next1
    pastStart.input2 = startNode.input2
    pastStart.next2 = startNode.next2
    startNode.input1 = startNode.input2 = '\0'
    startNode.next1 = pastStart
    startNode.next2 = nextStart
    FA_flag[pair_[1].id] = flag

def parseFirstReg(reg: str, startNode: NFANode, flag: int):
    pair_ = newRegInput(reg)
    startNode = pair_[0]
    FA_flag[pair_[1].id] = flag
    return pair_[0]

state_set: List[Set[int]] = [set() for _ in range(65536)]
state_table: List[Dict[str, Set[int]]] = [{} for _ in range(65536)]

def extend_closure(state_set: Set[int]) -> None:
    que = []
    for id in state_set:
        que.append(id)
    while len(que) > 0:
        id = que[0]
        que = que[1:]
        p = NFANodes[id]
        if p.input1 != '\0':
            continue
        if p.next1.id not in state_set:
            state_set.add(p.next1.id)
            que.append(p.next1.id)
        if p.input2 != '\0':
            continue
        if p.next2.id not in state_set:
            state_set.add(p.next2.id)
            que.append(p.next2.id)

def init_state_set(startNode: NFANode) -> None:
    state_set[0].add(startNode.id)
    extend_closure(state_set[0])

def NFA_to_DFA_table(startNode: NFANode) -> int:
    init_state_set(startNode)
    last_state_idx = 0
    for i in range(last_state_idx + 1):
        srcState = state_set[i]
        tgtTable = state_table[i]
        for c in allowed_chars:
            tgtTable[c] = set()  # 添加这行代码
            table = tgtTable[c]
            for id in srcState:
                node = NFANodes[id]
                if node.input1 == c:
                    table.add(node.next1.id)
                if node.input2 == c:
                    table.add(node.next2.id)
            extend_closure(table)
            if len(table) > 0:
                newOne = True
                for j in range(last_state_idx + 1):
                    if table == state_set[j]:
                        newOne = False
                        break
                if newOne:
                    state_set[last_state_idx + 1] = table
                    last_state_idx += 1
    return last_state_idx + 1

def constructDFA(stateCnt: int) -> None:
    for i in range(stateCnt):
        DFANodes[i].id = i
        DFANodes[i].flag = 0
        for j in state_set[i]:
            if FA_flag[j] != 0:
                if DFANodes[i].flag == 0 or FA_flag[j] < DFANodes[i].flag:
                    DFANodes[i].flag = FA_flag[j]
        thisTable = state_table[i]
        for c in allowed_chars:
            if len(thisTable[c]) == 0:
                continue
            tgtState = thisTable[c]
            for j in range(stateCnt):
                if tgtState == state_set[j]:
                    DFANodes[i].ptrs[c] = DFANodes[j]
                    break

def NFAtoDFA(startNode: NFANode) -> int:
    init_state_set(startNode)
    states = NFA_to_DFA_table(startNode)
    constructDFA(states)
    return states