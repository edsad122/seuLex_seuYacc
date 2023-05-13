Brace_left = 1
Brace_right = 2
Bracket_left = 3
Bracket_right = 4
CHAR_link = 5
class RegFilter:


    @staticmethod
    def spcharFilter(src):
        srcLen = len(src)
        ans = ""
        i = 0
        while i < srcLen:
            c = src[i]
            if c == "\\" and i + 1 < srcLen:
                i += 1
                c = src[i]
                if c == 'p':
                    c = ' '  # spec rule
                elif c == 'r':
                    c = '\r'
                elif c == 'n':
                    c = '\n'
                elif c == 't':
                    c = '\t'
                elif c == 'v':
                    c = '\v'
                elif c == 'f':
                    c = '\f'
                else:
                    ans += '\\'
                ans += c
                i += 1
                continue
            if c == '{':
                c = chr(Brace_left)
            elif c == '}':
                c = chr(Brace_right)
            elif c == '[':
                c = chr(Bracket_left)
            elif c == ']':
                c = chr(Bracket_right)
            ans += c
            i += 1
        return ans

    @staticmethod
    def stringing_replace(stringBig, stringsrc, stringdst):
        pos = 0
        srclen = len(stringsrc)
        dstlen = len(stringdst)
        while (pos := stringBig.find(stringsrc, pos)) != -1:
            stringBig = stringBig[:pos] + stringdst + stringBig[pos + srclen:]
            pos += dstlen
        return stringBig

    @staticmethod
    def replaceBracePairs(stringContent, stringMap):
        stringResult = stringContent
        stringOld = ""
        while stringResult != stringOld:
            stringOld = stringResult
            for p_ in stringMap:
                stringResult = RegFilter.stringing_replace(
                    stringResult, chr(Brace_left) + p_ + chr(Brace_right), stringMap[p_]
                )
        return stringResult

    @staticmethod
    def singleBracketReplace(string):
        tmp = ""
        len_ = len(string)
        i = 0
        while i < len_:
            c = string[i]
            if c == "\\":
                i += 1
                c = string[i]
                tmp += c
                i += 1
                continue
            if c == '-':
                tmp += chr(CHAR_link)
            else:
                tmp += c
            i += 1
        string = tmp
        Array = [0] * 127
        newstring = ""
        if string[0] != '^':
            i = 0
            while i < len(string):
                if string[i] == chr(CHAR_link):
                    #如果i+1大于len（string）
                    if i+1 != len(string):
                        for k in range(ord(string[i - 1]), ord(string[i + 1]) + 1):
                            Array[k] = 1
                    i += 2
                else:
                    Array[ord(string[i])] = 1
                    i += 1
        else:
            # Array[9] = 1; Array[13] = 1; Array[10] = 1;
            # for (int i = 32; i < 127; i++) {
            for i in range(9, 127):
                Array[i] = 1
            i = 0
            while i < len(string):
                if string[i] == chr(CHAR_link):
                    for k in range(ord(string[i - 1]), ord(string[i + 1]) + 1):
                        Array[k] = 0
                    i += 2
                else:
                    Array[ord(string[i])] = 0
                    i += 1
        for j in range(len(Array)):
            if Array[j] == 1:
                target = chr(j)
                if target in ['(', '|', ')', '+', '?', '*', '.', '\\']:
                    newstring += '\\' + target + '|'
                else:
                    newstring += target + '|'
        newstring = newstring[:-1]  # delete last '|'
        return newstring

    @staticmethod
    def replaceBracketPairs(string):
        string1 = chr(Bracket_left)
        string2 = chr(Bracket_right)
        pos1 = 0
        pos2 = 0

        while (
            (pos1 := string.find(string1, pos1)) != -1
            and (pos2 := string.find(string2, pos1)) != -1
        ):
            pos1 = string.find(string1, pos1)
            pos2 = string.find(string2, pos2)
            len_ = pos2 - pos1

            string3 = "(" + RegFilter.singleBracketReplace(string[pos1 + 1 : pos2]) + ")"

            string = string[:pos1] + string3 + string[pos2 + 1 :]
            pos1 += len(string3)
            pos2 += len(string3)
        return string

    @staticmethod
    def setDots(src):
        len_ = len(src)
        pos = -1
        while pos != -1:
            pos = -1
            inBracket = False
            i = 0
            while i < len_:
                if src[i] == "\\":
                    i += 2
                if inBracket:
                    if src[i] == chr(Bracket_right):
                        inBracket = False
                    i += 1
                    continue
                if src[i] == chr(Bracket_left):
                    inBracket = True
                if src[i] == '.':
                    pos = i
                    break
                i += 1
            if pos != -1:
                src = src[:pos] + chr(Bracket_left) + chr(9) + "-" + chr(
                    126
                ) + chr(Bracket_right) + src[pos + 1 :]
        return src

    @staticmethod
    def totalFilter(src, stringMap):
        src = RegFilter.spcharFilter(src)
        src = RegFilter.replaceBracePairs(src, stringMap)
        src = RegFilter.setDots(src)
        src = RegFilter.replaceBracketPairs(src)
        return src

    @staticmethod
    def quoteFilter(src):
        ans = ""
        src = src[1 : len(src) - 1]
        for c in src:
            if c in ['(', '|', ')', '+', '?', '*', '.', '\\']:
                ans += '\\'
            ans += c
        return ans