import base64
from urllib.parse import unquote
from cryptography.fernet import Fernet
# 凯撒
def carsar(string, n):
    t = ''
    for i in range(0, len(string)):
        if 'A' <= string[i] <= 'Z':
            num = ord(string[i]) - 65 - n
            t += chr(num % 26 + 65)
        elif 'a' <= string[i] <= 'z':
            num = ord(string[i]) - 97 - n
            t += chr(num % 26 + 97)
        else:
            t += string[i]
    return t

# 摩斯
def morse(string, sign=' '):
    MorseList = {
        ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
        "..-.": "F", "--.": "G","....": "H", "..": "I", ".---": "J",
        "-.-": "K", ".-..": "L","--": "M", "-.": "N","---": "O",
        ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
        "..-": "U", "...-": "V", ".--": "W", "-..-": "X","-.--": "Y",
        "--..": "Z",

        "-----": "0", ".----": "1", "..---": "2", "...--": "3", "....-": "4",
        ".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9",

        ".-.-.-": ".", "---...": ":", "--..--": ",", "-.-.-.": ";", "..--..": "?",
        "-...-": "=", ".----.": "'", "-..-.": "/", "-.-.--": "!", "-....-": "-",
        "..--.-": "_", ".-..-.": '"', "-.--.": "(", "-.--.-": ")", "...-..-": "$",
        ".-....": "&", ".--.-.": "@", ".-.-.": "+"
    }
    t = ''
    lists = string.split(sign)
    for code in lists:
        t += MorseList.get(code, '')
    return t

# rail fence
def rail_fence(string, n):
    lst = list(range(len(string)))
    f = [[None] * len(lst) for n in range(n)]
    r = list(range(n - 1)) + list(range(n - 1, 0, -1))
    for n, x in enumerate(lst):
        f[r[n % len(r)]][n] = x
    rst = [c for i in f for c in i if c is not None]
    return ''.join(string[rst.index(n)] for n in lst)

# 栅栏
def fence(string, n):
    t = ''
    slen = len(string)
    ys = slen % n
    s = slen // n
    lst = []
    if ys != 0:
        index = 0
        for i in range(ys):
            lst.append(list(string[index:index+s+1]))
            index += (s+1)
        for i in range(n-ys):
            lst.append(list(string[index:index+s])+[''])
            index += s
    else:
        lst = list(zip(*[iter(list(string))]*s))
    return ''.join(map(''.join,zip(*lst)))

# 埃特巴什
def atbash(string):
    t = ''
    a = "abcdefghijklmnopqrstuvwxyz"
    b = ''.join(list(reversed(a)))
    for char in string:
        if char in a.upper():
            t += b[a.index(char.lower())].upper()
        elif char in a:
            t += b[a.index(char)]
        else:
            t += char
    return t
# 培根
def bacon(string):
    cipher = {
        'lower': [
            "aaaaa", "aaaab", "aaaba", "aaabb", "aabaa", "aabab",
            "aabba", "aabbb", "abaaa", "abaab", "ababa", "ababb",
            "abbaa", "abbab", "abbba", "abbbb", "baaaa", "baaab",
            "baaba", "baabb", "babaa", "babab", "babba", "babbb",
            "bbaaa", "bbaab"
        ],
        'upper': [
            "AAAAA", "AAAAB", "AAABA", "AAABB", "AABAA", "AABAB",
            "AABBA", "AABBB", "ABAAA", "ABAAA", "ABAAB", "ABABA",
            "ABABB", "ABBAA", "ABBAB", "ABBBA", "ABBBB", "BAAAA",
            "BAAAB", "BAABA", "BAABB", "BAABB", "BABAA", "BABAB",
            "BABBA", "BABBB"
        ]
    }
    letter = {
        'lower': [
            'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z'
        ],
        'upper': [
            'a', 'b', 'c', 'd', 'e', 'f',
            'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r',
            's', 't', 'u', 'v', 'w', 'x',
            'y', 'z'
        ]
    }
    t = ''
    flag = 'lower' if string.islower() else 'upper'
    lists = []
    for i in range(0, len(string), 5):
        lists.append(string[i:i+5])
    for s in lists:
        for i in range(0, 26):
            if s == cipher[flag][i]:
                t += letter[flag][i]
    return t

# 键盘
def qwerty(letters):
    qwe = {
        'q': 'a', 'w': 'b', 'e': 'c', 'r': 'd', 't': 'e', 'y': 'f', 'u': 'g',
        'i': 'h', 'o': 'i', 'p': 'j', 'a': 'k', 's': 'l', 'd': 'm', 'f': 'n',
        'g': 'o', 'h': 'p', 'j': 'q', 'k': 'r', 'l': 's', 'z': 't',
        'x': 'u', 'c': 'v', 'v': 'w', 'b': 'x', 'n': 'y', 'm': 'z',

        'Q': 'A', 'W': 'B', 'E': 'C', 'R': 'D', 'T': 'E', 'Y': 'F', 'U': 'G',
        'I': 'H', 'O': 'I', 'P': 'J', 'A': 'K', 'S': 'L', 'D': 'M', 'F': 'N',
        'G': 'O', 'H': 'P', 'J': 'Q', 'K': 'R', 'L': 'S', 'Z': 'T',
        'X': 'U', 'C': 'V', 'V': 'W', 'B': 'X', 'N': 'Y', 'M': 'Z',
    }
    t = ''
    for char in letters:
        t += qwe.get(char)
    return t

#Ook!
def ook(string):
    def to_brainfuck(s):
        s = s.replace('\n'," ").replace('\r\n'," ")
        i = iter(s.split(' '))
        s = ''.join(map(' '.join,(zip(i,i))))
        s = s.replace("Ook. Ook?", ">")
        s = s.replace("Ook? Ook.", "<")
        s = s.replace("Ook. Ook.", "+")
        s = s.replace("Ook! Ook!", "-")
        s = s.replace("Ook! Ook.", ".")
        s = s.replace("Ook. Ook!", ",")
        s = s.replace("Ook! Ook?", "[")
        s = s.replace("Ook? Ook!", "]")
        return s
    program = to_brainfuck(string)
    print(program)
    d={'>':'p+=1\n','<':'p-=1\n','+':'n[p]+=1\n','-':'n[p]-=1\n','.':'t+=chr(n[p])\n',',':'n[p]=int(input())\n','[':'while n[p]:\n',']':''}
    s='t=""\nn=[0]*32768\np=0\n'
    i=0
    for c in program:
        s += '    '*i + d[c]
        if c=='[': i+=1
        if c==']': i-=1; s += '\r'
    exec(s)
    return locals()['t']


# ascii
def ascii(string, sign=' '):
    t = ''
    lists = map(int, string.split(sign))
    for i in lists:
        t += chr(i)
    return t

# rot 5/13/18/47
def rot(string, sign=0):
    result = {}
    def rot5(s):
        digits = '0123456789'
        t = ''
        for c in s:
            t += digits[int(c)-5] if c.isdigit() else c
        return t
    def rot13(s):
        lowers = 'abcdefghijklmnopqrstuvwxyz'
        uppers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        t = ''
        for c in s:
            if c.isalpha():
                t += uppers[ord(c)-ord('A')-13] if c.isupper() else lowers[ord(c)-ord('a')-13]
            else:
                t += c
        return t
    def rot18(s):
        return rot5(rot13(string))
    def rot47(s):
        t = ''
        for c in s:
            j = ord(c)
            t += chr(33 + ((j + 14) % 94)) if (33 <= j <= 126) else c
        return t
    try:
        assert sign in [0, 5, 13, 18, 47]
        if sign != 0:
            return eval(f'rot{sign}(string)')
        else:
            return f"rot5 : {rot5(string)}\nrot13: {rot13(string)}\nrot18: {rot18(string)}\nrot47: {rot47(string)}"
    except:
        print("'sign' must equal 5/13/18/47.")

# fernet
def fernet(key, msg):
    f = Fernet(key)
    return f.decrypt(msg)

if __name__ == "__main__":
    key = 'hBU9lesroX_veFoHz-xUcaz4_ymH-D8p28IP_4rtjq0='
    msg = b'gAAAAABaDDCRPXCPdGDcBKFqEFz9zvnaiLUbWHqxXqScTTYWfZJcz-WhH7rf_fYHo67zGzJAdkrwATuMptY-nJmU-eYG3HKLO9WDLmO27sex1-R85CZEFCU='
    print(fernet(key, msg))
    print(fence('1470258369',3))
    print(rot(r'f6ag{h4ll5_Ctf}', 5))
    print(rot(r's1nt{u3yy0_Pgs}', 13))
    print(rot(r's6nt{u8yy5_Pgs}', 18))
    print(rot(r'7`28L9b==_0rE7N', 47))
    print(rot(r'8`28L9b==_0rE7N'))
    print(morse(".-- ...-- .-.. -.-. ----- -- . ..--.- - --- ..--.- ..--- ----- ..--- ----- ..--.- .... --. .- -- ...--"))
    print(carsar("iodj", 3))
    print(bacon("aababababbaaaaaaabba"))
    print(bacon("AABABABABAAAAAAAABBA"))
    print(qwerty("ysqu"))
    print(ascii('67 84 70 123 82 77 125'))
    print(base64.b64decode('SSBsb3ZlIHlvdQ=='))
    print(base64.b32decode('JEQGY33WMUQHS33V'))
    print('\u0059\u006f\u0075\u0020\u0068\u0061\u0064\u0020\u006d\u0065\u0020\u0061\u0074\u0020\u0068\u0065\u006c\u006c\u006f')
    print(unquote('%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C'))
    print(atbash('uozt{Zgyzhv_xlwv_uiln_xguhsld}'))

