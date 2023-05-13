from yyProducer import *
class YaccParser:
    def __init__(self):
        self.terminal = []
        self.start = ""
        self.producer_list = []
        self.program2 = ""

    def define_rules(self, ln):
        left = ""
        right = ""
        len_ln = len(ln)
        i = 0
        flag = True
        if ln[i] == "%" and ln[i + 1] != "%":
            i += 1
            while i < len_ln and ln[i] == " ":
                i += 1
            while i < len_ln and ln[i] != " ":
                left += ln[i]
                i += 1
            while i < len_ln and ln[i] == " ":
                i += 1

            if left == "token":
                while i < len_ln:
                    if ln[i] != " ":
                        right += ln[i]
                        if i == len_ln - 1:
                            self.terminal.append(right)
                    else:
                        self.terminal.append(right)
                        right = ""
                    i += 1
            elif left == "start":
                self.start = ln[i:].strip()
            else:
                raise Exception("")

    def read_producer_right(self, ifile, left):
        str_line = ""
        while str_line != "|" and str_line != ";":
            str_line = next(ifile).strip()
            cur_right = []
            while str_line != "|" and str_line != ";":
                cur_right.append(str_line)
                str_line = next(ifile).strip()
            self.producer_list.append((left, cur_right))

    def producer_parsing(self, ifile):
        left = ""
        while not left:
            left = next(ifile).strip()
        while left != "%%":
            str_line = next(ifile).strip()
            if str_line != ":" and str_line != "|":
                raise Exception("")
            self.read_producer_right(ifile, left)
            left = ""
            while not left:
                left = next(ifile).strip()

    def read_from_stream(self, ifile):
        step = 0
        in_def = False
        for ln in ifile:
            if ln.strip() == "%%":
                step += 1
                if step == 1:
                    self.producer_parsing(ifile)
                    step += 1
                continue
            if ln.strip() == "":
                continue

            if step == 0:
                self.define_rules(ln)
            elif step == 2:
                self.program2 += ln + '\n'
            else:
                raise Exception("")

    @staticmethod
    def strlist_contain(str_list, stt):
        return stt in str_list

    def last_deal(self):
        all_ter = []
        all_not_ter = []
        ter_ids = []
        g_ids = []
        ter_id = 300
        g_id = 999
        for term in self.terminal:
            all_ter.append(term)
            ter_ids.append(ter_id)
            ter_id += 1
        all_not_ter.append("__PROGRAM__")
        g_ids.append(g_id)
        all_not_ter.append(self.start)
        g_ids.append(g_id)
        for producer in self.producer_list:
            for k in producer[1]:
                if k[0] == "'":
                    if self.strlist_contain(all_ter, k):
                        continue
                    else:
                        all_ter.append(k)
                        ter_ids.append(ord(k[1]))
                else:
                    if self.strlist_contain(all_not_ter, k) or self.strlist_contain(all_ter, k):
                            continue
                    else:
                        all_not_ter.append(k)
                        g_ids.append(g_id)
        
        for i in range(len(ter_ids)):
            self.append_new_symbol(ter_ids[i], all_ter[i], True)
        for i in range(len(g_ids)):
            self.append_new_symbol(g_ids[i], all_not_ter[i], False)
        
        self.producers.append((self.idname_to_idx("__PROGRAM__"), [self.idname_to_idx(self.start)]))
        for pro in self.producer_list:
            left = self.idname_to_idx(pro[0])
            v = []
            for str_line in pro[1]:
                v.append(self.idname_to_idx(str_line))
            self.producers.append((left, v))
    
    def init_all(self, filename):
        with open(filename, "r") as ifile:
            self.read_from_stream(ifile)
        self.last_deal()
    
    def write_tabs(self, filename):
        with open(filename, "w") as tab_file:
            self.write_tab(tab_file, tab_file.write)