import string

from secrets import token_urlsafe,randbelow,choice
from random import shuffle
from math import floor
from collections.abc import Callable
from typing import Any

def belongto(oripart:Callable, target:Callable) -> bool:
    for i in oripart :
        if i in target :
            return True
    return False

def hasin(oripart:Callable, target:Any) -> int:
    resn = 0
    for i in oripart :
        if i == target :
            resn = resn + 1
    return resn

def toprandList(top:int, n:int = 4, minz:int = 1) -> list[int] :
    res = []
    loT = floor(top * 2 / 3)
    for i in range(n-1) :
        tx = randbelow(loT)
        if tx < (top / n) and i < 1:
            tx = floor(top / n)
        if tx < minz :
            tx = tx + minz
        res.append(tx)
        loT = floor((top - sum(res)) * 2 / 3)
    if res[0] > (top / 3) :
        res.append(top - sum(res))
    else :
        res = [top - sum(res)] + res
    return res

def generatePassword(n:int, need_number:bool = True, 
                     need_upper:bool = True, need_punctuation:bool = True, 
                     mina:int = 1, urlsafe:bool = False) -> str :
    if urlsafe :
        n_x = floor(n / 1.3)
        pw = token_urlsafe(n_x)
        if not belongto(pw, "_-^@()[]") :
            pw = pw.replace(pw[randbelow(n)], "_")
    else :
        partnum = hasin([need_number,need_punctuation,need_upper], True)
        basechars = toprandList(top=n,n=(partnum+1),minz=mina)
        keyChar = [string.ascii_lowercase]
        if need_number :
            keyChar.append(string.digits)
        if need_upper :
            keyChar.append(string.ascii_uppercase)
        if need_punctuation :
            keyChar.append("!~@#$%^&*()_+=-[]|:;?<>,.{}")
        res = []
        for i in range(partnum+1) :
            res = res + [choice(keyChar[i]) for jj in range(basechars[i])]
        shuffle(res)
        shuffle(res)
        pw = "".join(res)
    return pw

class encryting(object):
    def __init__(self) -> None:
        pass