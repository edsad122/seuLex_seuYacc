from yylParser import *
from RegFilter import *
from RegToDFA import *
from SwitchDuilder import *
from lexSource import *


def main():
    ctrl = RegToDFA()

    yyl = YylParser("littlec.l")

    ruleMap = yyl.define_rules
    for key, value in ruleMap.items():
        ruleMap[key] = RegFilter.spcharFilter(value)
    ctrl.init()

    regs = yyl.regex_rules
    i=0
    for key, value in regs:
        if key[0] == "\"" and key[-1] == "\"":
            key = RegFilter.quoteFilter(key)
        else:
            regs[i]=(RegFilter.totalFilter(key, ruleMap),value)
        i+=1
    for key, value in regs:
        print(key,value)
    for key, value in regs:
        ctrl.appendRegex(key, value)
    ctrl.generate()
    cnt = ctrl.nodes
    case_list = {}
    for i in range(cnt):
        f = minDFA[i].flag
        if f != 0:
            s = ctrl.flag_map[f]
            if s not in case_list:
                case_list[s] = set()
            case_list[s].add(i)
    DFAExecuter = SwitchBuilder.stdBuild("DFAState", case_list, "error(\"unexpected word\");") + " return WHITESPACE;"
    Func_DFAExec = "int DFAExec(void) { " + DFAExecuter + " }"

    case_list.clear()
    for i in range(cnt):
        f = minDFA[i].flag
        if f != 0:
            case_list["{return 1;}"] = set(range(cnt))
    Func_DFATry = "int DFATry(void) { " + SwitchBuilder.stdBuild("DFAState", case_list, "return 0;") + " }"

    case_list.clear()
    for i in range(cnt):
        table = minDFA[i].ptrs
        local_list = {}
        for p_ in table:
            next_state = p_[1].id
            order = "{ DFAState = " + str(next_state) + "; }"
            if order not in local_list:
                local_list[order] = set()
            local_list[order].add(p_[0])
        content = "{ " + SwitchBuilder.stdBuild("c", local_list, "{return 1;}") + " }"
        if content not in case_list:
            case_list[content] = set()
        case_list[content].add(i)

    DFA_pusher = SwitchBuilder.stdBuild("DFAState", case_list, "return 0;") + " return 0; "
    Func_DFAPush = "int DFAPush(char c) { " + DFA_pusher + " }"

    lexSource.program1 = yyl.program1
    lexSource.program2 = yyl.program2
    lexSource.auto_program = Func_DFAExec + "\n" + Func_DFATry + "\n" + Func_DFAPush + "\n"

    yield_lex_yy_c("lex.yy.c")

    return 0


if __name__ == "__main__":
    main()