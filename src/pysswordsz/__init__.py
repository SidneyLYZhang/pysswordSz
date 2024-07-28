import typer
import pyperclip as clip
from encrytool import generatePassword

app = typer.Typer(no_args_is_help=True)

config = typer.Typer()
app.add_typer(config, name="config")
passdb = typer.Typer()
app.add_typer(passdb, name="pass")
cryptl = typer.Typer()
app.add_typer(cryptl, name="crypt")

@app.command()
def version():
    print("VERSION 0.0.1 (c) 2024 Sidney Zhang <zly@lyzhang.me>")

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

@config.command("list")
def cfg_list():
    print("list all")

@config.command("rm")
def cfg_remove():
    print("rm someting")

@config.command("set")
def cfg_remove():
    print("set cofig")

@passdb.command("init")
def pss_init():
    print("init now")

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
    print("decrypt {}".format(file))

if __name__ == "__main__":
    app()
