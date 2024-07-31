import typer
import pyperclip as clip
import polars as pl

from typing_extensions import Annotated
from encrytool import generatePassword,newKeys,encryting,generateXKCDPassword
from pzsconfig import newConfig,pszconfig
from rich import print
from pwsmanager import pwsmanager,buildPWDB

app = typer.Typer(no_args_is_help=True)

config = typer.Typer()
app.add_typer(config, name="config", help="manage config \t\t 管理配置")
passdb = typer.Typer()
app.add_typer(passdb, name="pass", help="manage password \t 管理密码")
cryptl = typer.Typer()
app.add_typer(cryptl, name="crypt", help="encrypt or decrypt \t 加密解密")

@app.command("version", help="show version \t\t 显示版本")
def version():
    print("VERSION 0.1.0")
    print("pysswordSz Copyright (C) 2024  Sidney Zhang <zly@lyzhang.me>")
    print("Licensed under GPL-3.0 license.")

@app.command(help="generate password \t 生成密码")
def genpass(n:int = 8,
            xkcd:bool = False,
            need_upper:bool = True,
            need_number:bool = True,
            need_punctuation:bool = True,
            minia:int = 1,
            urlsafe:bool = False,
            xk_mode:str = "pinyin",
            xk_padding:bool = False,
            show:bool = True,
            to_clip:bool = False):
    if xkcd :
        pswds = generateXKCDPassword(n=n, type_mode=xk_mode,
                                     padding=xk_padding)
    else:
        pswds = generatePassword(n = n, need_punctuation=need_punctuation,
                                 need_number=need_number,need_upper=need_upper,
                                 mina=minia, urlsafe=urlsafe)
    if show :
        print(pswds)
    if to_clip :
        clip.copy(pswds)

@app.command(help="init pysswordSz \t 初始化pysswordSz")
def init():
    newConfig()
    newKeys()
    print("The initialization of pysswordSz is complete!")

@config.command("list", help="list all configs / 列出所有已有配置")
def cfg_list():
    data = pszconfig().list()
    print(data)

@config.command("rm", help="remove one of config / 删除一个配置")
def cfg_remove(name:str):
    pszconfig().remove(name=name)


@config.command("set", help="set one of config / 设置一个配置")
def cfg_remove():
    print("set cofig")

@passdb.command("build",help="build a vault / 建立密码库")
def pss_build():
    buildPWDB()

@passdb.command("add", help="add a password to vault / 向密码库添加密码")
def pss_add(name:str, to:str="default"):
    pwsmanager().add_password(name = name, to = to)

@passdb.command("search",help="search a password in vault / 在密码库中搜索密码")
def pss_search(name:str, last_more:int = 0, vault:str="default",
               show:bool = True, to_clip:bool = False):
    mgr = pwsmanager()
    need_all = False if last_more == 0 else True
    data = mgr.search(name = name, all=need_all, vault=vault)
    if data.is_empty():
        print("")
    else:
        if need_all :
            with pl.Config(tbl_rows=-1):
                hl = last_more if last_more>0 else data.height
                print(data.head(hl))
        else:
            print(data)

@passdb.command("update", help="update a password in vault / 更新密码库中的密码")
def pss_update(name:str, vault:str="default"):
    pwsmanager().update(name=name, vault=vault)

@passdb.command("delete",help="delete a password in vault / 删除密码库中的密码")
def pss_delete(name:str, vault:str="default"):
    pwsmanager().delete(name=name, vault=vault)

@passdb.command("list", help="list all passwords in vault / 列出密码库中的所有密码")
def pss_list(vault:Annotated[str,typer.Argument(help="指定所需密码库",show_default=False)]="default", 
             add_columns:Annotated[str,typer.Argument(help="增加需要展示的列名，使用`,`隔开。",show_default=False)] = ""
            ):
    addcolumns = add_columns.split(",") if add_columns else None
    showall = typer.confirm("是否显示所有信息? --> ")
    needrows = -1 if showall else 16
    data = pwsmanager().list(vault=vault, other_columns=addcolumns)
    if data.is_empty():
        print("[green]There is currently no password in Vault {}...".format(vault))
    else :
        with pl.Config(tbl_rows=needrows):
            print(data)

@cryptl.command("encr",help="encrypt a file / 加密一个文件或文件夹")
def ctl_encr(file: Annotated[str, typer.Argument(help="需要加密的文件或文件夹路径")]):
    cipher = encryting()
    cipher.encrypt_file(file)
    print("[green]Encryption is complete!")

@cryptl.command("decr",help="decrypt a file / 解密一个文件或文件夹")
def ctl_decr(file: Annotated[str, typer.Argument(help="需要解密的文件路径")]):
    cipher = encryting()
    cipher.decrypt_file(file)
    print("[green]Decryption is complete!")

@cryptl.command("list",help="list all files / 列出所有加密文件")
def ctl_list():
    dataList = encryting().list_files()
    if dataList.is_empty():
        print("There is currently no encrypted data...")
    else:
        with pl.Config(tbl_rows=-1):
            print(dataList)

if __name__ == "__main__":
    app()
