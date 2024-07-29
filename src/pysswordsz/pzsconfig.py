from pathlib import Path

import typer
import yaml
import platform
import os

def setting_config():
    # 处理配置位置
    overpath = os.getenv("PASSWORDS_SZ")
    if overpath is None :
        if platform.system() == "Windows" :
            overpath = "AppData/Local/passwords_sz"
        else :
            overpath = ".config/passwords_sz"
        conPath = Path.home() / overpath
    else :
        conPath = overpath
    return conPath

def newConfig() -> None:
    data = {
        "columns": ["name","url","user","password","commen"],
        "keyfolder":setting_config(),
        "datafolder":setting_config()
    }
    changefolder = typer.confirm("是否更改密钥KEY文件的保存位置?\nDo you want to change the KEY file location?\n--> ")
    if changefolder :
        data["keyfolder"] = typer.prompt("请输入密钥KEY文件的保存位置\nPlease input the KEY file location\n--> ")
    changefolder = typer.confirm("是否更改数据DATA文件的保存位置?\nDo you want to change the DATA file location?\n--> ")
    if changefolder :
        data["datafolder"] = typer.prompt("请输入数据DATA文件的保存位置\nPlease input the DATA file location\n--> ")
    os.mkdir(setting_config())
    with open(setting_config() / "config.yaml", "w", encoding="utf-8") as fx :
        yaml.dump(data, fx)

class pszconfig(object):
    def __init__(self) -> None:
        self.__home = setting_config()
        cfile = self.__home / "config.yaml"
        with open(cfile, "r", encoding="utf-8") as ftxt:
            self.__data = yaml.load(ftxt.read(),Loader=yaml.FullLoader)
    def keyfolder(self) -> Path:
        fp = self.__data["keyfolder"]
        return Path(fp)
    def datafolder(self) -> Path:
        fp = self.__data["datafolder"]
        return Path(fp)
    def list(self) -> None:
        print(self.__data)
    def setting(self, name, value) :
        if name == "columns":
            if "," in value :
                xtemp = value.spilt(",")
            else:
                xtemp = value
        else:
            xtemp = value
        print("complete set {} with value {}".format(name,xtemp))
    def remove(self, name) :
        print("remove config {}".format(name))