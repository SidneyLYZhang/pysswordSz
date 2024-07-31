from pathlib import Path
from pzsconfig import pszconfig
from encrytool import encryting,generatePassword
from uuid import uuid4
from datetime import datetime

import typer

import polars as pl

def buildPWDB(name:str) -> None:
    cons = pszconfig()
    filePlace = cons.datafoldar()
    columns = cons.columns
    data = {
        i:[] for i in (["uuid","name"]+columns+["password","createtime"])
    }
    data = pl.DataFrame(data)
    data.write_csv(filePlace / (name+".lyz"))
    cons.setting("vault",name)
    if cons.vaultlist :
        if name in cons.vaultlist :
            raise ValueError("vault {} already exists".format(name))
        else:
            cons.setting("vaultlist",cons.vaultlist.append(name))
    else:
        cons.setting("vaultlist",[name])
    print("build a password database {}".format(name))

def ask_password() -> list :
    resList = {}
    resList["n"] = typer.prompt("输入密码长度 --> ",default=16,type=int)
    is_url = typer.confirm("是否需要URL安全字符? --> ")
    if is_url :
        resList["urlsafe"] = is_url
    else:
        resList["need_number"] = typer.confirm("是否需要数字? --> ",default=True)
        resList["need_upper"] = typer.confirm("是否需要大写字母? --> ",default=True)
        resList["eed_punctuation"] = typer.confirm("是否需要符号? --> ",default=True)
        resList["mina"] = typer.prompt("各类型字符的最小个数 --> ",default=1,type=int)
    return resList

class pwsmanager(object):
    def __init__(self) -> None:
        cons = pszconfig()
        self.__home = cons.datafoldar()
        self.__default = cons.vault
        self.__vaultList = cons.vaultlist
        self.__cipher = encryting()
        self.__columns = cons.columns
    def __read(self, vault:str) -> pl.DataFrame:
        theVault = self.__default if vault=="default" else vault
        if theVault not in self.__vaultList :
            raise ValueError("vault {} not exists".format(theVault))
        return pl.read_csv(self.__home / (theVault+".lyz"))
    def update(self,name:str, vault:str = "default"):
        self.__read(vault)
        print("update a password {}".format(name))
    def search(self, name:str, all:bool = False, vault:str = "default"):
        print("search {} password {} in {}".format(("all" if all else "last"),name,vault))
    def add_password(self,name:str, to:str = "default"):
        theVault = self.__default if to=="default" else to
        if theVault not in self.__vaultList :
            raise ValueError("vault {} not exists".format(theVault))
        add_Data = {
            "uuid":uuid4(),
            "name":name}
        if typer.confirm("是否需要生成新密码？ --> ") :
            password = generatePassword(**ask_password())
        else :
            password = typer.prompt("请输入密码 --> ",hide_input=True,confirmation_prompt=True)
        add_Data["password"] = self.__cipher.encrypt_data(password)
        for i in self.__columns:
            txt = typer.prompt("please input the {} of {} --> ".format(i,name))
            is_encr = typer.confirm("是否需要加密保存? --> ")
            if is_encr :
                add_Data[i] = self.__cipher.encrypt_data(txt)
            else :
                add_Data[i] = txt
        add_Data["createtime"] = datetime.now()
        alldata = self.__read(to)
        alldata = alldata.vstack(pl.DataFrame(add_Data))
        alldata.write_csv(self.__home / (theVault+".lyz"))
        print("Complete adding a password of {} into {} vault...".format(name, to))
    def delete(self, name:str, vault:str = "default"):
        print("delete a password {} from {}".format(name,vault))