import typer
import pyperclip as clip
from encrytool import generatePassword,newKeys,encryting
from pzsconfig import newConfig
from rich import print

app = typer.Typer(no_args_is_help=True)

config = typer.Typer()
app.add_typer(config, name="config")
passdb = typer.Typer()
app.add_typer(passdb, name="pass")
cryptl = typer.Typer()
app.add_typer(cryptl, name="crypt")

@app.command()
def version():
    print("VERSION 0.1.0")
    print("LICENSE under GPL-3.0")
    print("pysswordSz Copyright (C) 2024  Sidney Zhang <zly@lyzhang.me>")

@app.command()
def genpass(n: int = 16, need_upper:bool = True,
            need_number:bool = True, need_punctuation:bool = True,
            minia:int = 1, urlsafe:bool = False, 
            show:bool = True, to_clip:bool = False):
    pswds = generatePassword(n = n, need_punctuation=need_punctuation,
                             need_number=need_number,need_upper=need_upper,
                             mina=minia, urlsafe=urlsafe)
    if show :
        print(pswds)
    if to_clip :
        clip.copy(pswds)

@app.command()
def init():
    newConfig()
    newKeys()
    print("The initialization of pysswordSz is complete!")

@config.command("list")
def cfg_list():
    print("list all")

@config.command("rm")
def cfg_remove():
    print("rm someting")

@config.command("set")
def cfg_remove():
    print("set cofig")

@passdb.command("build")
def pss_build():
    print("init now")

@passdb.command("add")
def pss_add(name:str):
    print("add now {}".format(name))

@passdb.command("search")
def pss_search(name:str):
    print("search {}".format(name))

@passdb.command("update")
def pss_update(name:str):
    print("update {}".format(name))

@passdb.command("delete")
def pss_delete(name:str):
    print("delete {}".format(name))

@cryptl.command("encr")
def ctl_encr(file:str, zip:bool=False):
    print("encrypt {}".format(file))

@cryptl.command("decr")
def ctl_decr(file:str):
    cipher = encryting()
    cipher.decrypt_file(file)
    print("[green]Decryption is complete!")

@cryptl.command("list")
def ctl_list():
    dataList = encryting().list_files()
    if dataList.is_empty():
        print("There is currently no encrypted data...")
    else:
        print(dataList)

if __name__ == "__main__":
    app()
