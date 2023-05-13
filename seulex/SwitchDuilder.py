class SwitchBuilder:
    @staticmethod
    def stdBuild(var_name, case_list, defaultCase="error(\"\");"):
        begin = "switch(" + var_name + ") { "
        end = "default: {" + defaultCase + "} }"

        middle = ""

        for p_ in case_list:
            pbegin = ""
            for caseIdx in case_list[p_]:
                pbegin += "case " + str(caseIdx) + " : "
            pbegin += " { "
            pend = " break; }"
            middle += pbegin + p_ + pend

        return begin + middle + end