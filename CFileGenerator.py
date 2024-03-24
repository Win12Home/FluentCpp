from subprocess import *
from PyQt5.QtCore import QThread,pyqtSignal
from time import sleep as Sleep
from pathlib import Path
from CModule import fl,get_file_path

class GenerateFile(QThread):
    gcclog=pyqtSignal(str)
    errorsignal=pyqtSignal(list,list)
    def __init__(self,filename:str,gccpath:str,compiledfilename:str,extras:list[str]=["-g","-std=c++11"]) -> None:
        super().__init__()
        self.filename=filename
        self.gccpath=gccpath
        self.comfilename=compiledfilename
        self.extras=extras
        self.breakit=False
        self.errors=[]
        self.warnings=[]

    def run(self) -> None:
        """
        Generate File And Run
        """
        self.i=" ".join(self.extras)
        self.gcclog.emit(str(Path.cwd()).replace("/","\\")+">"+f"{self.gccpath} {self.filename} -o {self.comfilename} {self.i}"+"\n")
        self.p=Popen(f"{self.gccpath} {self.filename} -o {self.comfilename} {self.i}",shell=True,stdout=PIPE,stderr=PIPE)
        self.line=None
        self.word=""
        for self.line in iter(self.p.stdout.readline,b""):
            self.gcclog.emit(self.line.decode("utf-8"))
            print(self.line.decode("utf-8"))
            self.word+=self.line.decode("utf-8")+"\n"
        for self.line in iter(self.p.stderr.readline,b""):
            self.gcclog.emit(self.line.decode("utf-8"))
            print(self.line.decode("utf-8"))
            self.word += self.line.decode("utf-8") + "\n"
        self.p.wait()
        self.oerrors=fl(self.word,"error")
        self.owarnings=fl(self.word,"warning")
        self.errors,self.warnings=[],[]
        for i in self.oerrors:
            self._=i[i.find("error: ")+6:].lstrip()
            if i.startswith(self.filename):
                self.lines = i[len(self.filename) + 1:].split(" ")[0].split(":")
                self.errors.append([self._,self.lines[0],self.lines[1]])
            elif i.startswith("collect2.exe"):
                self.errors.append([self._,"无","无"])
        for i in self.owarnings:
            self._=i[i.find("warning: ")+6:].lstrip()
            if i.startswith(self.filename):
                self.lines=i[len(self.filename)+1:].split(" ")[0].split(":")
                self.errors.append([self._,self.lines[0],self.lines[1]])
            elif i.startswith("collect2.exe"):
                self.errors.append([self._,"无","无"])
        self.errorsignal.emit(self.errors,self.warnings)
        if not self.errors and not self.warnings:
            self.gcclog.emit("编译完成")
            self.success=True
        elif self.errors:
            self.gcclog.emit("编译可能错误！")
            self.success=False
        elif self.warnings:
            self.gcclog.emit("编译成功，但有警告")
            self.success=True
        else:
            self.gcclog.emit("编译完成")
            self.success=True
        with open("./run.bat","w",encoding="ansi") as f:
            f.write("@echo off\ntitle FluentC++程序运行器\ncd {}\n{}\necho.\npause\nexit".format(get_file_path(self.comfilename),self.comfilename))
        while not self.success:
            Sleep(0.2)
            if self.breakit:
                break
        print("")
        if self.success:
            Popen(f"start run.bat",shell=True,stdout=PIPE,stderr=PIPE)

    def getGenerateCode(self) -> str:
        self.i=" ".join(self.extras)
        return f"{self.gccpath} {self.filename} -o {self.comfilename} -lstdc++ {self.i}"