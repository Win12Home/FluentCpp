from typing import Union
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from qfluentwidgets import *
from qfluentwidgets.components.material.acrylic_menu import *
from CModule import *
from darkdetect import *
from CFileGenerator import *
import sys

app = QApplication([])
setTheme(Theme.AUTO)


class AutoCompletePlainTextEdit(PlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_BraceLeft:
            self.insertPlainText("{}")
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Left)
            self.setTextCursor(cursor)
        elif event.key() == Qt.Key_BracketLeft:
            self.insertPlainText("[]")
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Left)
            self.setTextCursor(cursor)
        elif event.key() == Qt.Key_ParenLeft:
            self.insertPlainText("()")
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Left)
            self.setTextCursor(cursor)
        elif event.key() == Qt.Key_Apostrophe:
            self.insertPlainText("''")
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Left)
            self.setTextCursor(cursor)
        elif event.key() == Qt.Key_Tab:
            self.insertPlainText("    ")
        elif event.text() == "\"":
            self.insertPlainText("\"\"")
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Left)
            self.setTextCursor(cursor)
        elif event.key() == Qt.Key_Backspace:
            cursor = self.textCursor()
            self._t = ""
            for i in self.toPlainText():
                self._t += i
            if self._t[cursor.position() - 1:cursor.position() + 1] in ["[]", "{}", "()", "<>", "\"\"", "''"]:
                cursor.setPosition(cursor.position())
                cursor.deletePreviousChar()
                cursor.setPosition(cursor.position() + 1)
                cursor.deletePreviousChar()
                self.setTextCursor(cursor)
            elif self._t[cursor.position() - 4:cursor.position()] == "    ":
                for __count in range(4): cursor.deletePreviousChar()
            else:
                super().keyPressEvent(event)
        elif event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            pos = cursor.position()
            cursor.movePosition(QTextCursor.StartOfLine)
            line = cursor.block().text()
            self._t = ""
            for i in self.toPlainText():
                self._t += i
            indent = len(line) - len(line.lstrip())
            if self._t[pos - 1:pos + 2] == "{};":
                cursor.movePosition(QTextCursor.EndOfLine)
                cursor.deletePreviousChar()
                cursor.deletePreviousChar()
                self.setTextCursor(cursor)
                self.insertPlainText("\n" + " " * indent + "    \n" + " " * indent + "};")
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.setPosition(cursor.position() - 1)
                self.setTextCursor(cursor)
            elif self._t[pos - 1:pos + 1] == "{}":
                cursor.movePosition(QTextCursor.EndOfLine)
                cursor.deletePreviousChar()
                self.setTextCursor(cursor)
                self.insertPlainText("\n" + " " * indent + "    \n" + " " * indent + "}")
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.setPosition(cursor.position() - 1)
                self.setTextCursor(cursor)
            elif self._t[pos - 1] == ":":
                self.insertPlainText("\n" + " " * indent + "    ")
            else:
                super().keyPressEvent(event)
                self.insertPlainText(" " * indent)
        else:
            super().keyPressEvent(event)


class CppSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument | QTextDocument = None, useclanguage: bool = False):
        super(CppSyntaxHighlighter, self).__init__(parent)
        self.highlightingRules = []
        if isDarkTheme():
            self.highlightGreenColor = Qt.green
            self.highlightBlueColor = Qt.darkBlue
        else:
            self.highlightGreenColor = Qt.darkGreen
            self.highlightBlueColor = Qt.blue
            self.highlightCyanColor = Qt.darkCyan
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(self.highlightBlueColor)
        keywords = [
            "alignas", "alignof", "constexpr", "char16_t", "char32_t",
            "decltype", "nullptr", "noexcept", "static_assert", "auto",
            "asm", "const_cast", "dynamic_cast", "reinterpret_cast", "static_cast",
            "asm-definition", "bool", "break", "case", "catch", "char", "const",
            "struct", "delete", "do", "double", "float", "long", "int", "short",
            "signed", "unsigned", "wchar_t", "if", "enum", "explicit", "export",
            "extern", "friend", "inline", "mutable", "namespace", "operator",
            "private", "register", "return", "static", "template", "this",
            "typedef", "virtual", "typeid", "typename", "using", "void", "and",
            "and_eq", "bitand", "bitor", "catch", "class", "compl", "const_cost",
            "decltype", "new", "throw", "try", "xor", "xor_eq", "true", "false",
            "or_eq", "or", "not", "not_eq", "public", "protected", "thread_local",
            "sizeof", "for", "while", "else"
        ]
        cppkeywords = [
            "alignas", "alignof", "and", "and_eq", "asm", "bitand", "bitor", "bool",
            "catch", "char16_t", "char32_t", "class", "compl", "const_cost", "constexpr",
            "decltype", "delete", "dynamic_cast", "explicit", "false", "friend", "inline",
            "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator",
            "or_eq", "private", "protected", "public", "reinterpret_cast", "static_cast",
            "static_assert", "template", "this", "thread_local", "throw", "true", "try",
            "typeid", "typename", "using", "virtual", "wchar_t", "xor", "xor_eq"
        ]
        hashkeywords = [
            "#include", "#define", "#ifndef", "#endif", "#if", "#elif", "#error",
            "#line", "#pragma", "#undef", "#ifdef", "#else"
        ]
        for keyword in keywords:
            if useclanguage and keyword in cppkeywords:
                continue
            self.highlightingRules.append((QRegExp("\\b" + keyword + "\\b"), keywordFormat))
        singleQuoteFormat = QTextCharFormat()
        singleQuoteFormat.setForeground(self.highlightBlueColor)
        self.highlightingRules.append((QRegExp("'[^']*'"), singleQuoteFormat))
        doubleQuoteFormat = QTextCharFormat()
        doubleQuoteFormat.setForeground(self.highlightGreenColor)
        self.highlightingRules.append((QRegExp("\"[^\"]*\""), doubleQuoteFormat))
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(self.highlightGreenColor)
        self.highlightingRules.append((QRegExp("//[^\n]*"), commentFormat))
        hashFormat = QTextCharFormat()
        hashFormat.setForeground(self.highlightBlueColor)
        for keywords in hashkeywords:
            self.highlightingRules.append((QRegExp(keywords), hashFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(self.highlightGreenColor)

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength, self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text, startIndex + commentLength)


class FluentCApp(FluentWindow):
    def __init__(self) -> None:
        super().__init__()
        self.filename = None
        self.setWindowTitle("FluentC++ {}".format(version))
        self.setWindowIcon(QIcon("resources/icon.png"))
        self.resize(800, 600)
        self.editor = QWidget()
        self.editor.setObjectName("FluentCApp.Editor")
        self.editorText = AutoCompletePlainTextEdit(self.editor)
        self.editorText.setLineWrapMode(0)
        self.editorText.textChanged.connect(self.checkAndSave)
        self.filemenu_btn = TransparentDropDownPushButton("文件", self.editor)
        self.filemenu = RoundMenu()
        self.filemenu_a1 = QAction(QIcon(FluentIcon.DOCUMENT.path()), "新建")
        self.filemenu_a1.triggered.connect(self.newFile)
        self.filemenu_a2 = QAction(QIcon(FluentIcon.ADD.path()), "打开")
        self.filemenu_a2.triggered.connect(self.open)
        self.filemenu_a3 = QAction(QIcon(FluentIcon.SAVE_AS.path()), "另存为")
        self.filemenu_a3.triggered.connect(self.anotherSave)
        self.filemenu_a4 = QAction("退出")
        self.filemenu_a4.triggered.connect(self.close)
        self.filemenu.addActions([self.filemenu_a1, self.filemenu_a2, self.filemenu_a3, self.filemenu_a4])
        self.filemenu_btn.setGeometry(0, 0, 100, 30)
        self.filemenu_btn.setMenu(self.filemenu)
        self.editmenu_btn = TransparentDropDownPushButton("编辑", self.editor)
        self.editmenu = RoundMenu()
        self.editmenu_a1 = QAction(QIcon(FluentIcon.PASTE.path()), "粘贴")
        self.editmenu_a1.triggered.connect(self.editorText.paste)
        self.editmenu_a2 = QAction(QIcon(FluentIcon.CANCEL.path()), "撤销")
        self.editmenu_a2.triggered.connect(self.editorText.undo)
        self.editmenu_a3 = QAction("全选")
        self.editmenu_a3.triggered.connect(self.editorText.selectAll)
        self.editmenu.addActions([self.editmenu_a1, self.editmenu_a2, self.editmenu_a3])
        self.editmenu_btn.setGeometry(100, 0, 100, 30)
        self.editmenu_btn.setMenu(self.editmenu)
        self.runmenu_btn=TransparentDropDownPushButton("运行",self.editor)
        self.runmenu=RoundMenu()
        self.runmenu_a1=QAction(QIcon(FluentIcon.COMMAND_PROMPT.path()),"运行")
        self.runmenu_a1.triggered.connect(self.run)
        self.runmenu_a2=QAction(QIcon(FluentIcon.COPY.path()),"补齐DLL（在DLL错误的情况下）")
        self.runmenu_a2.triggered.connect(self.dllCopy)
        self.runmenu.addActions([self.runmenu_a1,self.runmenu_a2])
        self.runmenu_btn.setGeometry(200,0,100,30)
        self.runmenu_btn.setMenu(self.runmenu)
        self.editorText.setFont(QFont(sets.get("family"), sets.get("fontsize")))
        self.usedsyntax = CppSyntaxHighlighter(self.editorText.document())
        self.logText = TextEdit(self.editor)
        self.logText.setReadOnly(True)
        self.errorView=TreeWidget(self.editor)
        self.errorView.setHeaderLabels(["错误"])
        self.errorView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.errorView.customContextMenuRequested.connect(self.showMenu)
        self.settings = QWidget()
        self.settings.setObjectName("FluentCApp.SettingDialog")
        self.settingswidget = QStackedWidget(self.settings)
        self.setting1 = SettingCardGroup("常用设置", self.settingswidget)
        self.card_1a = SettingCard(FluentIcon.FONT, "字体", "设置字体")
        self.card_1a.combobox = ComboBox(self.card_1a)
        self.card_2a = SettingCard(FluentIcon.FONT_SIZE, "字体大小", "设置字体大小")
        self.card_2a.spinbox = SpinBox(self.card_2a)
        self.card_2a.spinbox.setMinimum(0)
        self.card_2a.spinbox.setMaximum(1000)
        self.card_3a = SwitchSettingCard(FluentIcon.CANCEL_MEDIUM, "退出时未保存提醒", "如果未保存文件，就会有这个提醒")
        self.card_3a.setChecked(not sets.get("discordsaveinfo"))
        self.card_3a.checkedChanged.connect(lambda: sets.write("discordsaveinfo", not self.card_3a.isChecked()))
        self.card_4a=PrimaryPushSettingCard("选择",FluentIcon.COMMAND_PROMPT,"C++编译器","设置C++编译器(g++)",self)
        self.card_4a.button.clicked.connect(self.setCppCompiler)
        self.card_4a.text=LineEdit(self.card_4a)
        self.card_4a.text.setText(sets.get("c++compiler"))
        self.card_4a.text.setReadOnly(True)
        self.card_5a = PrimaryPushSettingCard("选择", FluentIcon.COMMAND_PROMPT, "C语言编译器", "设置C语言编译器(gcc)",self)
        self.card_5a.button.clicked.connect(self.setC_Compiler)
        self.card_5a.text = LineEdit(self.card_5a)
        self.card_5a.text.setText(sets.get("c_compiler"))
        self.card_5a.text.setReadOnly(True)
        self.setting1.addSettingCards([self.card_1a, self.card_2a, self.card_3a,self.card_4a,self.card_5a])
        self.setting2 = QWidget()
        self.cppcompile = SubtitleLabel(self.setting2)
        self.cppcompile.setText("额外编译选项（C++）（换行为下一个）")
        self.cppcompiletext = PlainTextEdit(self.setting2)
        self.cppcompiletext.setPlaceholderText("输入额外编译选项")
        self.cppcompiletext.setPlainText(sets.get("cppextracompilecmd"))
        self.cppcompiletext.textChanged.connect(
            lambda: sets.write("cppextracompilecmd", self.cppcompiletext.toPlainText()))
        self.ccompile = SubtitleLabel(self.setting2)
        self.ccompile.setText("额外编译选项（C语言）（换行为下一个）")
        self.ccompiletext = PlainTextEdit(self.setting2)
        self.ccompiletext.setPlaceholderText("输入额外编译选项")
        self.ccompiletext.setPlainText(sets.get("cextracompilecmd"))
        self.ccompiletext.textChanged.connect(
            lambda: sets.write("cextracompilecmd", self.ccompiletext.toPlainText()))
        self.settingspivot = Pivot(self.settings)
        self.settingswidget.addWidget(self.setting1)
        self.settingswidget.addWidget(self.setting2)
        self.settingspivot.addItem("FluentCApp.SettingDialog.Set1", "常用设置",
                                   lambda: self.settingswidget.setCurrentWidget(self.setting1))
        self.settingspivot.addItem("FluentCApp.SettingDialog.Set2", "编译设置",
                                   lambda: self.settingswidget.setCurrentWidget(self.setting2))
        self.settingspivot.setCurrentItem("FluentCApp.SettingDialog.Set1")
        self.addSubInterface(self.editor, FluentIcon.EDIT.path(), "编辑", parent=self, selected=True)
        self.addSubInterface(self.settings, FluentIcon.SETTING.path(), "设置", position=NavigationItemPosition.BOTTOM,
                             parent=self)
        self.initializeFont()
        self.splashscreen=SplashScreen(self.windowIcon(),self)
        self.splashscreen.setIconSize(QSize(102,102))
        self.splashscreen.setCursor(Qt.BusyCursor)
        self.show()
        self.createSubInterface()
        self.splashscreen.finish()

    def createSubInterface(self):
        self.loop=QEventLoop(self)
        QTimer.singleShot(2500,self.loop.quit)
        self.loop.exec()

    def setCppCompiler(self):
        self.browse,_=QFileDialog.getOpenFileName(self,"选择C++编译器",filter="编译器 (g++.exe gcc.exe)")
        if self.browse:
            sets.write("c++compiler",str(self.browse).replace("/","\\"))
            self.card_4a.text.setText(str(self.browse).replace("/","\\"))

    def setC_Compiler(self):
        self.browse,_=QFileDialog.getOpenFileName(self,"选择C语言编译器",filter="编译器 (gcc.exe)")
        if self.browse:
            sets.write("c_compiler",str(self.browse).replace("/","\\"))
            self.card_5a.text.setText(str(self.browse).replace("/","\\"))

    def showMenu(self,pos):
        self._treeitem=self.errorView.itemAt(pos)
        if self._treeitem:
            self.errorViewMenu=RoundMenu(self)
            self.errorViewMenu.action1=QAction(QIcon(FluentIcon.COPY.path()),"复制消息",self)
            self.errorViewMenu.action1.triggered.connect(lambda:copy(self._treeitem.text(0)))
            self.errorViewMenu.addAction(self.errorViewMenu.action1)
            self.errorViewMenu.exec_(self.errorView.mapToGlobal(pos))

    def checkAndSave(self):
        self.autoSave()
        self.errorView.clear()
        """if self.filename and get_file_extension(self.filename) == "c":
            self.thread = check_cpp_language_error(self.editorText.toPlainText(),True,parent=self)
        else:
            self.thread=check_cpp_language_error(self.editorText.toPlainText(),parent=self)
        self.thread.start()
        self.thread.returnCheck.connect(self.check)"""
        self._view=QTreeWidgetItem(self.errorView)
        self._view.setText(0,"这块没做完")

    def check(self,items):
        if self.filename:
            if get_file_extension(self.filename) == "c":
                for self.i in items:
                    self._view = QTreeWidgetItem(self.errorView)
                    self._view.setText(0, str(self.i))
            else:
                for self.i in items:
                    self._view = QTreeWidgetItem(self.errorView)
                    self._view.setText(0, str(self.i))
        else:
            for self.i in items:
                self._view=QTreeWidgetItem(self.errorView)
                self._view.setText(0,str(self.i))

    def initializeFont(self):
        self.card_1a.combobox.clear()
        for self.i in get_font_list():
            self.card_1a.combobox.addItem(self.i)
        self.card_1a.combobox.setCurrentIndex(self.card_1a.combobox.findText(sets.get("family")))
        self.card_2a.spinbox.setValue(sets.get("fontsize"))
        self.card_1a.combobox.currentTextChanged.connect(lambda: self.fontchange(self.card_1a.combobox.currentText()))
        self.card_2a.spinbox.valueChanged.connect(lambda: self.fontchange(fontsize=self.card_2a.spinbox.value()))

    def fontchange(self, font=None, fontsize=None):
        if font:
            sets.write("family", font)
        else:
            sets.write("fontsize", fontsize)
        self.editorText.setFont(QFont(sets.get("family"), sets.get("fontsize")))

    def dllCopy(self):
        self.msg=MessageBox("提醒","运行补齐程序可能会报毒，需要继续吗？",self)
        self.msg.yesButton.setText("继续")
        self.msg.cancelButton.setText("算了")
        if self.msg.exec_():
            self.logText.setText("正在补齐...")
            self.threads=DLLCopy(self)
            self.threads.start()
            self.threads.log.connect(lambda item:self.logText.setText(self.logText.toPlainText()+"\n"+item))

    def close(self):
        if not self.filename and not self.editorText.toPlainText() == "" and not sets.get("discordsaveinfo"):
            self.msg = MessageBox("提醒",
                                  "你确定要退出吗？\n此文件未保存，如果继续，那会丢失数据！(你也不想你肝了几秒的文档丢失了吧）\n如果继续，请按\"退出\"",
                                  self)
            self.msg.yesButton.setText("退出")
            self.msg.cancelButton.setText("算了")
            if self.msg.exec_():
                super().close()
        else:
            super().close()

    def newFile(self):
        self.filename = None
        self.editorText.setPlainText("")
        self.changeTitle()

    def autoSave(self):
        if self.filename:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(self.editorText.toPlainText())

    def run(self):
        if not self.filename:
            self.browse, _ = QFileDialog.getSaveFileName(self, "另存为",
                                                         filter="C++文件 (*.cpp *.h *.hpp);;C语言文件 (*.c);;源文件 (*.cpp *.c);;头文件 (*.h *.hpp);;支持文件 (*.cpp *.c *.h *.hpp)")
            if self.browse:
                self.filename = str(self.browse).replace("/", "\\")
                if get_file_extension(self.browse) in ["cpp", "h", "hpp"]:
                    self.usedsyntax = CppSyntaxHighlighter(self.editorText.document())
                else:
                    self.usedsyntax = CppSyntaxHighlighter(self.editorText.document(), True)
                self.changeTitle()
                self.autoSave()
        if self.filename:
            self.logText.setText("编译开始")
            if get_file_extension(self.browse) == "c":
                self.mode = "cextracompilecmd"
                self.compile="c_compiler"
            else:
                self.mode="cppextracompilecmd"
                self.compile="c++compiler"
            self.threads=GenerateFile(self.filename,sets.get(self.compile),get_file_path(self.filename)+".exe",sets.get(self.mode).split("\n"))
            print(self.threads.getGenerateCode())
            self.threads.start()
            self.threads.gcclog.connect(self.logConnect)

    def logConnect(self,item:str):
        self.logText.setText(self.logText.toPlainText()+"\n"+item)
        if item == "编译可能错误！":
            self.msg=MessageBox("编译错误","编译可能错误，需要启动上一次编译的程序吗？",self)
            self.msg.yesButton.setText("继续")
            self.msg.cancelButton.setText("取消")
            if self.msg.exec_():
                if not Path(get_file_path(self.filename)+".exe").exists():
                    self.threads.breakit=True
                    self.threads.exit(-1)
                    self._name=get_file_path(self.filename)+".exe"
                    self.msg=MessageBox("错误",f"找不到{self._name}，编译未完成！",self)
                    self.msg.yesButton.setText("确定")
                    self.msg.cancelButton.hide()
                    self.msg.buttonLayout.insertStretch(1)
                    self.msg.exec_()
                else:
                    self.threads.success=True
            else:
                self.threads.breakit = True

    def changeTitle(self):
        if self.filename:
            self.setWindowTitle("FluentC++ {} - {}".format(version, self.filename))
        else:
            self.setWindowTitle("FluentC++ {}*".format(version))

    def anotherSave(self):
        self.browse, _ = QFileDialog.getSaveFileName(self, "另存为",
                                                     filter="C++文件 (*.cpp *.h *.hpp);;C语言文件 (*.c);;源文件 (*.cpp *.c);;头文件 (*.h *.hpp);;支持文件 (*.cpp *.c *.h *.hpp)")
        if self.browse:
            self.filename = str(self.browse).replace("/", "\\")
            if get_file_extension(self.browse) in ["cpp", "h", "hpp"]:
                self.usedsyntax = CppSyntaxHighlighter(self.editorText.document())
            else:
                self.usedsyntax = CppSyntaxHighlighter(self.editorText.document(), True)
            self.changeTitle()
            self.autoSave()

    def open(self):
        self.browse, _ = QFileDialog.getOpenFileName(self, "打开",
                                                     filter="C++文件 (*.cpp *.h *.hpp);;C语言文件 (*.c);;源文件 (*.cpp *.c);;头文件 (*.h *.hpp);;支持文件 (*.cpp *.c *.h *.hpp)")
        if self.browse:
            self.filename = str(self.browse).replace("/", "\\")
            self.changeTitle()
            if get_file_extension(self.browse) in ["cpp", "h", "hpp"]:
                self.usedsyntax = CppSyntaxHighlighter(self.editorText.document())
            else:
                self.usedsyntax = CppSyntaxHighlighter(self.editorText.document(), True)
            with open(self.browse, "r", encoding="utf-8") as f:
                self.editorText.setPlainText(f.read())

    def addSubInterface(self, interface: QWidget, icon: Union[FluentIconBase, QIcon, str], text: str,
                        position=NavigationItemPosition.TOP, parent=None, selected: bool = False,
                        **kwargs) -> NavigationTreeWidget:
        self.stackedWidget.addWidget(interface)
        self._item = self.navigationInterface.addItem(interface.objectName(), icon, text,
                                                      lambda: self.switchTo(interface), True, position, text,
                                                      parent.objectName())
        self._item.setSelected(selected)
        return self._item

    def resizeEvent(self, e) -> None:
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())
        self.editorText.setGeometry(QRect(QPoint(0, 30), QPoint(self.width() - 50 - 300, self.height() // 2 + 130)))
        self.logText.setGeometry(
            QRect(QPoint(0, self.height() // 2 + 130), QPoint(self.width() - 50 - 300, self.height() - 50)))
        self.errorView.setGeometry(QRect(QPoint(self.width() - 50 - 300,30),QPoint(self.width()-50,self.height()-50)))
        self.settingspivot.setGeometry(QRect(QPoint(0, 0), QPoint(self.width() - 50, 50)))
        self.settingswidget.setGeometry(QRect(QPoint(0, 50), QPoint(self.width() - 50, self.height() - 50)))
        self.card_1a.combobox.setGeometry(QRect(QPoint(300, 20), QPoint(self.width() - 100, 50)))
        self.card_2a.spinbox.setGeometry(QRect(QPoint(300, 20), QPoint(self.width() - 100, 50)))
        self.card_4a.text.setGeometry(QRect(QPoint(300,20),QPoint(self.width()-150,50)))
        self.card_5a.text.setGeometry(QRect(QPoint(300,20),QPoint(self.width()-150,50)))
        self.cppcompile.setGeometry(0, 0, 700, 50)
        self.cppcompiletext.setGeometry(QRect(QPoint(0, 50), QPoint(self.width() - 50, (self.height() - 100) // 2)))
        self.ccompile.setGeometry(0, (self.height() - 100) // 2, 700, 50)
        self.ccompiletext.setGeometry(0, (self.height() - 100) // 2 + 50, self.width() - 50, self.height() - 50)


if __name__ == "__main__":
    translator = FluentTranslator(QLocale(QLocale.Chinese, QLocale.SimplifiedChineseScript, QLocale.China))
    app.installTranslator(translator)
    appfluent = FluentCApp()
    sys.exit(app.exec_())
