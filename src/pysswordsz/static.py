import random
import random_words
from pysswordsz.ChineseWords import CIZU

def getChinese() -> str:
    val = random.randint(0x4e00, 0x9fbf)
    return chr(val)

def getChineseWords() -> str:
    length = len(CIZU)
    word = CIZU[random.randint(0, length-1)]
    return word

class randomWords(object):
    def __init__(self, n:int = 8, mode:str = "pinyin", phrase:bool = True):
        if mode not in ["pinyin", "wubi", "wade", "english"]:
            raise ValueError("mode must be in ['pinyin', 'wubi', 'wade', 'english']")
        self.__mode = mode
        self.words = []
        if phrase :
            if mode != "english":
                self.words.extend([getChineseWords() for _ in range(n)])
            else:
                self.words.extend(random_words.randomWords(n))
        else :
            self.words.extend([getChinese() for _ in range(n)])
        if mode != "english" :
            pass
    def __str__(self):
        return " ".join(self.words)
    def __repr__(self):
        return " ".join(self.words)
    def join(self, seq:str = " ") -> str:
        return seq.join(self.words)
    def plain_join(self) -> str :
        pass