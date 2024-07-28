from pathlib import Path
from pzsconfig import pszconfig

class pwsmanager(object):
    def __init__(self) -> None:
        self.__home = pszconfig().datafoldar()
        self.__default = "default"
        self.__vaultList = ["default","last"]
    def __read(self, vault:str):
        theVault = self.__default if vault=="default" else vault
        print("reading {}".format(theVault))
    def update(self,name:str, vault:str = "default"):
        self.__read(vault)
        print("update a password {}".format(name))
    def search(self, name:str, all:bool = False, vault:str = "default"):
        print("search {} password {} in {}".format(("all" if all else "last"),name,vault))
    def add_password(self,name:str, to:str = "default"):
        print("add a password {} into {}".format(name, to))
    def delete(self, name:str, vault:str = "default"):
        print("delete a password {} from {}".format(name,vault))