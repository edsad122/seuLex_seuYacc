class YylParser:
    def __init__(self, filename):
        self.program1 = ""
        self.define_rules = {}
        self.regex_rules = []
        self.program2 = ""
        self.initAll(filename)

    def lnToPair(self, ln):
        left = ""
        right = ""
        i = 0
        len_ln = len(ln)
        while i < len_ln and (ln[i] == ' ' or ln[i] == '\t'):
            i += 1
        while i < len_ln and not (ln[i] == ' ' or ln[i] == '\t'):
            left += ln[i]
            i += 1
        while i < len_ln and (ln[i] == ' ' or ln[i] == '\t'):
            i += 1
        while i < len_ln:
            right += ln[i]
            i += 1
        return left, right

    def readFromStream(self, ifile):
        ln = ""
        step = 0
        inDef = False
        for ln in ifile:
            ln = ln.strip()
            if inDef:
                if ln == "%}":
                    inDef = False
                else:
                    self.program1 += ln + "\n"
                continue
            if ln == "%{":
                inDef = True
                continue
            if ln == "%%":
                step += 1
                continue
            if ln == "":
                continue
            if step == 0:
                left, right = self.lnToPair(ln)
                self.define_rules[left] = right
            elif step == 1:
                left, right = self.lnToPair(ln)
                self.regex_rules.append((left, right))
            elif step == 2:
                self.program2 += ln
            else:
                raise Exception("")
    
    def initAll(self, filename):
        with open(filename, "r") as ifile:
            self.readFromStream(ifile)
