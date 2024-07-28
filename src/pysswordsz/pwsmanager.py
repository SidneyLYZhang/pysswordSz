from pathlib import Path

class pwsmanager(object):
    def __init__(self, path:str|Path) -> None:
        self.__home = Path(path)