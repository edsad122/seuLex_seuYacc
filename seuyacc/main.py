from yaccUtil import *
from yaccParser import *
from LRTable import *
from yyWrite import *
from yyWrite import *
from yaccSource import *
def main():
    yyy = YaccParser("littlec.y")

    dump_producers(print)

    # print(YyWrite.make_init())

    yyy.writeTabs("y.tab.h")

    dfa = LRDFA()
    dfa.generateLALR()

    lrt = LRTable(dfa)

    # lrt.dump(print)
    # print(lrt.code_dump("state", "c"))

    with open("y.tab.c", "w") as f:
        f.write("{}\n".format(yacc_program))
        f.write("void init_producers() {{ {} }}\n".format(YyWrite.make_init()))
        f.write("int GoTo(int state, int c) {{ {} }}\n".format(lrt.code_dump("state", "c")))


if __name__ == "__main__":
    main()