from subprocess import *
from PyQt5.QtCore import QThread,pyqtSignal

class GenerateFile(QThread):
    gcclog=pyqtSignal(str)
    def __init__(self,filename:str,gccpath:str,compiledfilename:str,extras:list[str]=["-g","-std=c++11"]) -> None:
        super().__init__()
        self.filename=filename
        self.gccpath=gccpath
        self.comfilename=compiledfilename
        self.extras=extras
        self.breakit=False

    def run(self) -> None:
        """
        Generate File And Run
        """
        self.i=" ".join(self.extras)
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
        if self.word.find("error") == -1:
            self.gcclog.emit("编译完成")
            self.success=True
        else:
            self.gcclog.emit("编译可能错误！")
            self.success=False
        with open("./run.bat","w",encoding="utf-8") as f:
            f.write("@echo off\ntitle FluentC Debugger\n{}\necho.\npause\nexit".format(self.comfilename))
        while not self.success:
            if self.breakit:
                break
        print("")
        if self.success:
            Popen(f"start run.bat",shell=True,stdout=PIPE,stderr=PIPE)

    def getGenerateCode(self) -> str:
        self.i=" ".join(self.extras)
        return f"{self.gccpath} {self.filename} -o {self.comfilename} -lstdc++ {self.i}"