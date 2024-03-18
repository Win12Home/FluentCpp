from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtGui import QFontDatabase
from subprocess import Popen,PIPE
from json import loads,dumps
from pathlib import Path
from typing import Union
from shutil import copy2
from pyperclip import *

__all__=["version","get_file_extension","get_directory_path","sets","get_font_list","check_cpp_language_error","copy","get_file_path","DLLCopy"]



def get_file_extension(filename:str):
    path = Path(filename)
    return path.suffix[1:]

def get_directory_path(filename):
    path = Path(filename)
    directory = path.parent
    return str(directory).replace("/","\\")

def get_font_list():
    font_base=QFontDatabase()
    return font_base.families()

class DLLCopy(QThread):
    log=pyqtSignal(str)
    def __init__(self,parent):
        super().__init__(parent)

    def run(self):
        self.sys32path="C:\\Windows\\System32"
        self.thispath=str(Path.cwd()).replace("/","\\")
        self.srcs=[
            "\\dlls\\libgcc_s_seh-1.dll",
            "\\dlls\\libstdc++-6.dll",
            "\\dlls\\libwinpthread-1.dll"
        ]
        for i in self.srcs:
            copy2(self.thispath+i,self.sys32path)
        self.log.emit("补齐完成")

settings={}
original={
    "c++compiler":str(Path.cwd()).replace("/","\\")+"\\resources\\mingw64\\bin\\g++.exe",
    "c_compiler":str(Path.cwd()).replace("/","\\")+"\\resources\\mingw64\\bin\\gcc.exe",
    "cppextracompilecmd":"-std=c++11\n-lstdc++\n-fexec-charset=GBK\n-finput-charset=UTF-8\n-g",
    "cextracompilecmd":"-std=c11\n-lstdc++\n-fexec-charset=GBK\n-finput-charset=UTF-8\n-g",
    "fontsize":16,
    "family":"Consolas",
    "discordsaveinfo":False,
    "version":"1.0-pre2"
}

class sets:
    @staticmethod
    def get(name:str):
        global settings
        return settings[name]

    @staticmethod
    def refresh():
        global settings
        settings=original
        with open("config.fconf","w",encoding="utf-8")as f:
            f.write(dumps(settings))

    @staticmethod
    def write(name:str,value:Union[str|int|bool]):
        global settings
        settings[name]=value
        with open("config.fconf","w",encoding="utf-8")as f:
            f.write(dumps(settings))

    @property
    def __repr__(self):
        return None

class check_cpp_language_error(QThread):
    returnCheck=pyqtSignal(list)
    def __init__(self,code,isClanguage:bool=False,parent=None):
        super().__init__(parent)
        filename=""
        std=""
        if isClanguage:
            filename="test.c"
            std="--std=c11"
        else:
            filename="test.cpp"
            std = "--std=c++11"
        with open(filename,"w",encoding="utf-8")as f:
            f.write(code)
        self.command=["resources\\cppchecker\\cppcheck.exe","--enable=all",std,str(Path.cwd()).replace("/","\\")+"\\"+filename]
        print(" ".join(self.command))

    def run(self):
        errors=[]
        p=Popen(" ".join(self.command),stdout=PIPE,stderr=PIPE,shell=True)
        self.line=""
        for self.line in iter(p.stdout.readline,b""):
            print(self.line.decode("utf-8"))
            if (self.line.decode("utf-8")).find("Checking") == -1:
                errors.append(self.line.decode("utf-8"))
        p.wait()
        self.returnCheck.emit(errors)

def get_file_path(filename):
    path = Path(filename)
    file_name = path.stem
    directory = path.parent
    file_path = directory / file_name
    return str(file_path)

if Path("config.fconf").exists():
    with open("config.fconf","r",encoding="utf-8") as f:
        settings=loads(f.read())
else:
    sets.refresh()
version=sets.get("version")