from yyProducer import *
class YyWrite:
    @staticmethod
    def make_init():
        content = ""
        for idx, name in map_idx_idname.items():
            content += 'strcpy(item_name_table[{}], "{}");'.format(idx, name)
        for t, p_ in enumerate(producers):
            idx = p_[0]
            vec = p_[1]
            l = len(vec)
            v = [l, idx] + vec
            for i in range(l + 2):
                content += 'producers[{}][{}] = {};'.format(t, i, v[i])
        return content