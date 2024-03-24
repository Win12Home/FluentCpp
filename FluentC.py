from __future__ import division  #我也不知道为什么要引入，这就是第二个注释（惊人的两个注释）#
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
from random import randint
from keyword import kwlist
from Examples import *
import pyexpat
import sys

app = QApplication([])
setTheme(Theme.AUTO)

class DocumentsBox(MessageBoxBase):
    def __init__(self,parent):
        super().__init__(parent)
        self.title=SubtitleLabel("选择示例")
        self.content=BodyLabel()
        self.content.setText("在这里选择一个示例")
        self.listbox=TreeWidget()
        self.listbox.setHeaderLabels(["名称","难度(1-10)"])
        self.listbox.setMinimumHeight(350)
        self.viewLayout.addWidget(self.title)
        self.viewLayout.addWidget(self.content)
        self.viewLayout.addWidget(self.listbox)
        self.widget.setFixedWidth(400)
        self.setupListBox()
        self.yesButton.setText("选定")
        self.cancelButton.setText("取消")

    def setupListBox(self):
        self.l1=QTreeWidgetItem(self.listbox)
        self.l1.setText(0,"Hello World!")
        self.l1.setText(1,"1")
        self.l2=QTreeWidgetItem(self.listbox)
        self.l2.setText(0,"搜索数组项")
        self.l2.setText(1,"2")
        self.l3=QTreeWidgetItem(self.listbox)
        self.l3.setText(0,"二分查找(vector)")
        self.l3.setText(1,"3")
        self.l4=QTreeWidgetItem(self.listbox)
        self.l4.setText(0,"彩色输出")
        self.l4.setText(1,"3")
        self.listbox.setCurrentItem(self.l1)
        self.listbox.setColumnWidth(0,300)
        self.listbox.setColumnWidth(1,50)

    def getListBoxSelectedItem(self):
        self.item=self.listbox.currentItem()
        if self.item == self.l1:
            return helloworld
        elif self.item == self.l2:
            return search
        elif self.item == self.l3:
            return binarysearch
        elif self.item == self.l4:
            return rainbow

class LoadingSplashScreen(SplashScreen):
    def __init__(self, icon, parent):
        super().__init__(icon, parent)
        self.loadScreen = IndeterminateProgressRing(self)
        self.loadScreen.setFixedSize(QSize(40, 40))
        self.loadScreen.setToolTip("哇，你发现我了！")
        self.loadScreen.installEventFilter(ToolTipFilter(self.loadScreen,200))
        self._opacityUse = True

    def resizeEvent(self, e):
        iw, ih = self.iconSize().width(), self.iconSize().height()
        self.titleBar.resize(self.width(), self.titleBar.height())
        self.iconWidget.move(self.width() // 2 - iw // 2, self.height() // 2 - ih // 2 - self.iconWidget.height() // 2)
        self.loadScreen.move(self.width() // 2 - self.loadScreen.width() // 2,
                             self.height() // 2 - self.loadScreen.height() // 2 + self.iconWidget.height() // 2 + 60)

    def setFinishUseOpacity(self, value):
        self._opacityUse = value

    def finish(self):
        if self._opacityUse:
            for i in range(100, 0, -8):
                self._opacity = i / 100
                self.op = QGraphicsOpacityEffect()
                self.op.setOpacity(self._opacity)
                self.setGraphicsEffect(self.op)
                self.setAutoFillBackground(True)
                self.parent().repaint()
        super().finish()

class AutoCompletePlainTextEdit(PlainTextEdit):
    autoCompleteChanged=pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self._usingAutomaticComplete=True

    def setUsingAutoComplete(self,a0:bool):
        self.autoCompleteChanged.emit()
        self._usingAutomaticComplete=a0

    def keyPressEvent(self, event: QKeyEvent):
        try:
            if self._usingAutomaticComplete:
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
                    if self._t[pos - 1:pos + 1] in ["{}","()","[]"]:
                        self.insertPlainText("\n" + " " * indent + "    " + "\n" + " " * indent)
                        cursor = self.textCursor()
                        cursor.movePosition(QTextCursor.StartOfLine)
                        cursor.setPosition(cursor.position()-1)
                        self.setTextCursor(cursor)
                    elif self._t[pos - 1] == ":":
                        self.insertPlainText("\n" + " " * indent + "    ")
                    else:
                        super().keyPressEvent(event)
                        self.insertPlainText(" " * indent)
                else:
                    super().keyPressEvent(event)
            else:
                if event.key() == Qt.Key_Return:
                    cursor=self.textCursor()
                    pos=cursor.position()
                    cursor.movePosition(QTextCursor.StartOfLine)
                    line=cursor.block().text()
                    indent=len(line) - len(line.lstrip())
                    super().keyPressEvent(event)
                    self.insertPlainText(" " * indent)
                else:
                    super().keyPressEvent(event)
        except IndexError:
            super().keyPressEvent(event)
        finally:
            pass
            #self.numberview.update()

class NullSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,parent:QTextDocument|QTextDocument=None):
        super(NullSyntaxHighlighter, self).__init__(parent)

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,parent:QTextDocument|QTextDocument=None):
        super().__init__(parent)
        self.highlightingRules=[]
        if isDarkTheme():
            self.highlightGreenColor = Qt.green
            self.highlightBlueColor = QColor("#6a5acd")
            self.highlightCyanColor = Qt.cyan
        else:
            self.highlightGreenColor = Qt.darkGreen
            self.highlightBlueColor = Qt.darkBlue
            self.highlightCyanColor = Qt.darkCyan
        keywordFormat=QTextCharFormat()
        keywordFormat.setForeground(self.highlightBlueColor)
        for i in kwlist:
            self.highlightingRules.append((QRegExp("\\b"+i+"\\b"),keywordFormat))
        for i in ["int","str","float","list","set","dict"]:
            self.highlightingRules.append((QRegExp("\\b" + i + "\\b"), keywordFormat))
        stringFormat=QTextCharFormat()
        stringFormat.setForeground(self.highlightGreenColor)
        self.multilineStringFormat=QTextCharFormat()
        self.multilineStringFormat.setForeground(self.highlightGreenColor)
        self.highlightingRules.append((QRegExp("\"\"\"[^#]*\"\"\""),self.multilineStringFormat))
        self.highlightingRules.append((QRegExp("\"[^\"\n]*\""),stringFormat))
        self.highlightingRules.append((QRegExp("'[^'\n]*'"),stringFormat))
        commentFormat=QTextCharFormat()
        commentFormat.setForeground(self.highlightGreenColor)
        commentFormat.setFontItalic(True)
        self.highlightingRules.append((QRegExp("#[^\n]"),commentFormat))
        anotherKeywordFormat=QTextCharFormat()
        anotherKeywordFormat.setForeground(self.highlightCyanColor)
        for i in ["self"]:
            self.highlightingRules.append((QRegExp("\\b"+i+"\\b"),anotherKeywordFormat))

    def highlightBlock(self, text):
        inMultiLineComment = False
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                if format == self.multilineStringFormat:
                    if not inMultiLineComment:
                        inMultiLineComment = True
                        self.setFormat(index, length, format)
                    else:
                        inMultiLineComment = False
                else:
                    self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

class JsonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,parent:QTextDocument|QTextDocument=None):
        super(JsonSyntaxHighlighter,self).__init__(parent)
        self.highlightingRules=[]
        if isDarkTheme():
            self.highlightGreenColor = Qt.green
            self.highlightBlueColor = QColor("#6a5acd")
        else:
            self.highlightGreenColor = Qt.darkGreen
            self.highlightBlueColor = Qt.darkBlue
        braceFormat = QTextCharFormat()
        braceFormat.setForeground(self.highlightBlueColor)
        self.highlightingRules.append((QRegExp(r"[{}[\]]"),braceFormat))
        stringFormat=QTextCharFormat()
        stringFormat.setForeground(self.highlightGreenColor)
        self.highlightingRules.append((QRegExp(r'"[^"\\]*(\\.[^"\\]*)*"'),stringFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

class CppSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument | QTextDocument = None, useclanguage: bool = False):
        super(CppSyntaxHighlighter, self).__init__(parent)
        self.highlightingRules = []
        self.highlightRedColor=Qt.red
        if isDarkTheme():
            self.highlightGreenColor = Qt.green
            self.highlightBlueColor = QColor("#6a5acd")
        else:
            self.highlightGreenColor = Qt.darkGreen
            self.highlightBlueColor = Qt.darkBlue
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(self.highlightRedColor)
        typeFormat=QTextCharFormat()
        typeFormat.setForeground(self.highlightBlueColor)
        keywords = [
            "alignas", "alignof", "decltype", "nullptr", "noexcept", "static_assert",
            "asm", "const_cast", "dynamic_cast", "reinterpret_cast", "static_cast",
            "asm-definition", "break", "case", "catch","delete", "do",
            "if", "enum", "explicit", "export","extern", "friend", "inline",
            "mutable", "operator",
            "register", "return", "static", "template", "this",
            "typedef", "virtual", "typeid", "typename", "using", "and",
            "and_eq", "bitand", "bitor", "catch", "compl",
            "decltype", "throw", "try", "xor", "xor_eq", "true", "false",
            "or_eq", "or", "not", "not_eq", "thread_local",
            "sizeof", "for", "while", "else"
        ]
        typeskeyword=[
            "constexpr", "char16_t", "char32_t","auto","void","new","wchar_t",
            "const_cost","bool","int","double","float","short","long","char",
            "const","class","signed","unsigned","private","public","protected",
            "namespace","struct"
        ]
        cppkeywords = [
            "alignas", "alignof", "and", "and_eq", "asm", "bitand", "bitor","catch", "compl",
            "decltype", "delete", "dynamic_cast", "explicit", "false", "friend", "inline",
            "mutable", "noexcept", "not", "not_eq", "nullptr", "operator",
            "or_eq", "reinterpret_cast", "static_cast","static_assert", "template", "this",
            "thread_local", "throw", "true", "try","typeid", "typename", "using", "virtual", "xor", "xor_eq"
        ]
        cpptypeskeyword=[
            "char16_t","char32_t","const_cost","constexpr","bool","wchar_t","new","class",
            "private","protected","public","private","protected","struct","namespace"
        ]
        hashkeywords = [
            "#include", "#define", "#ifndef", "#endif", "#if", "#elif", "#error",
            "#line", "#pragma", "#undef", "#ifdef", "#else"
        ]
        for keyword in keywords:
            if useclanguage and keyword in cppkeywords:
                continue
            self.highlightingRules.append((QRegExp("\\b" + keyword + "\\b"), keywordFormat))
        for keyword in typeskeyword:
            if useclanguage and keyword in cpptypeskeyword:
                continue
            self.highlightingRules.append((QRegExp("\\b"+keyword+"\\b"),typeFormat))
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
        self.editor = QWidget()
        self.editor.setObjectName("FluentCApp.Editor")
        self.editorText = AutoCompletePlainTextEdit(self.editor)
        self.editorText.setLineWrapMode(0)
        self.editorText.textChanged.connect(self.checkAndSave)
        self.filemenu_btn = TransparentDropDownPushButton("文件", self.editor)
        self.filemenu = RoundMenu()
        self.filemenu_a1 = QAction(QIcon(FluentIcon.DOCUMENT.path()), "新建")
        self.filemenu_a1.triggered.connect(self.newFile)
        self.filemenu_a2=QAction(QIcon(FluentIcon.ARROW_DOWN.path()),"示例")
        self.filemenu_a2.triggered.connect(self.example)
        self.filemenu_a3 = QAction(QIcon(FluentIcon.ADD.path()), "打开")
        self.filemenu_a3.triggered.connect(self.open)
        self.filemenu_a4 = QAction(QIcon(FluentIcon.SAVE_AS.path()), "另存为")
        self.filemenu_a4.triggered.connect(self.anotherSave)
        self.filemenu_a5 = QAction("退出")
        self.filemenu_a5.triggered.connect(self.close)
        self.filemenu.addActions([self.filemenu_a1, self.filemenu_a2, self.filemenu_a3, self.filemenu_a4,self.filemenu_a5])
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
        self.runmenu_btn = TransparentDropDownPushButton("运行", self.editor)
        self.runmenu = RoundMenu()
        self.runmenu_a1 = QAction(QIcon(FluentIcon.COMMAND_PROMPT.path()), "运行")
        self.runmenu_a1.triggered.connect(self.run)
        self.runmenu_a2 = QAction(QIcon(FluentIcon.COPY.path()), "补齐DLL（在DLL错误的情况下）")
        self.runmenu_a2.triggered.connect(self.dllCopy)
        self.runmenu.addActions([self.runmenu_a1, self.runmenu_a2])
        self.runmenu_btn.setGeometry(200, 0, 100, 30)
        self.runmenu_btn.setMenu(self.runmenu)
        self.editorText.setFont(QFont(sets.get("family"), sets.get("fontsize")))
        self.usedsyntax = CppSyntaxHighlighter(self.editorText.document())
        self.logWidget=QStackedWidget(self.editor)
        self.logText = PlainTextEdit()
        self.logText.setReadOnly(True)
        self.logTreeWidget=TreeWidget()
        self.logTreeWidget.setHeaderLabels(["类别","行","列","消息"])
        self.logTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.logTreeWidget.customContextMenuRequested.connect(self.showMessage)
        self.logWidget.addWidget(self.logText)
        self.logWidget.addWidget(self.logTreeWidget)
        self.logWidget.setCurrentWidget(self.logText)
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
        self.card_4a = PrimaryPushSettingCard("选择", FluentIcon.COMMAND_PROMPT, "C++编译器", "设置C++编译器(g++)",
                                              self)
        self.card_4a.button.clicked.connect(self.setCppCompiler)
        self.card_4a.text = LineEdit(self.card_4a)
        self.card_4a.text.setText(sets.get("c++compiler"))
        self.card_4a.text.setReadOnly(True)
        self.card_5a = PrimaryPushSettingCard("选择", FluentIcon.COMMAND_PROMPT, "C语言编译器", "设置C语言编译器(gcc)",
                                              self)
        self.card_5a.button.clicked.connect(self.setC_Compiler)
        self.card_5a.text = LineEdit(self.card_5a)
        self.card_5a.text.setText(sets.get("c_compiler"))
        self.card_5a.text.setReadOnly(True)
        self.setting1.addSettingCards([self.card_1a, self.card_2a, self.card_3a, self.card_4a, self.card_5a])
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
        self.resize(1280,768)
        self.splashscreen = LoadingSplashScreen(self.windowIcon(), self)
        self.splashscreen.setIconSize(QSize(142,142))
        self.splashscreen.setCursor(Qt.BusyCursor)
        self.splashscreen.show()
        self.show()
        self.createSubInterface()
        self.splashscreen.finish()

    def example(self):
        self.msg=DocumentsBox(self)
        if self.msg.exec_():
            self.selitem=self.msg.getListBoxSelectedItem()
            self.msg=MessageBox("提醒","你确定要覆盖文件吗？\n此文件未保存，如果继续，那会丢失数据！\n如果继续，请按\"覆盖\"键",self)
            self.msg.yesButton.setText("覆盖")
            self.msg.cancelButton.setText("取消")
            if self.msg.exec_():
                self.filename=None
                self.changeTitle()
                self.editorText.setUsingAutoComplete(True)
                self.usedsyntax=CppSyntaxHighlighter(self.editorText.document())
                self.editorText.setPlainText(self.selitem)

    def createSubInterface(self):
        self.loop = QEventLoop(self)
        self.a = randint(4500,15000)
        print(self.a)
        QTimer.singleShot(self.a, self.loop.quit)
        self.loop.exec()

    def setCppCompiler(self):
        self.browse, _ = QFileDialog.getOpenFileName(self, "选择C++编译器", filter="编译器 (g++.exe gcc.exe)")
        if self.browse:
            sets.write("c++compiler", str(self.browse).replace("/", "\\"))
            self.card_4a.text.setText(str(self.browse).replace("/", "\\"))

    def setC_Compiler(self):
        self.browse, _ = QFileDialog.getOpenFileName(self, "选择C语言编译器", filter="编译器 (gcc.exe)")
        if self.browse:
            sets.write("c_compiler", str(self.browse).replace("/", "\\"))
            self.card_5a.text.setText(str(self.browse).replace("/", "\\"))

    def checkAndSave(self):
        self.changeTitle()
        self.autoSave()

    def check(self, items):
        if self.filename:
            if get_file_extension(self.filename).lower() == "c":
                for self.i in items:
                    self._view = QTreeWidgetItem(self.errorView)
                    self._view.setText(0, str(self.i))
            else:
                for self.i in items:
                    self._view = QTreeWidgetItem(self.errorView)
                    self._view.setText(0, str(self.i))
        else:
            for self.i in items:
                self._view = QTreeWidgetItem(self.errorView)
                self._view.setText(0, str(self.i))

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
        self.repaint()

    def dllCopy(self):
        self.msg = MessageBox("提醒", "运行补齐程序可能会报毒，需要继续吗？", self)
        self.msg.yesButton.setText("继续")
        self.msg.cancelButton.setText("算了")
        if self.msg.exec_():
            self.logText.setPlainText("正在补齐...")
            self.threads = DLLCopy(self)
            self.threads.start()
            self.threads.log.connect(lambda item: self.logText.setPlainText(self.logText.toPlainText() + "\n" + item))

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
        self.usedsyntax=CppSyntaxHighlighter(self.editorText.document())
        self.editorText.setPlainText("")
        self.changeTitle()

    def autoSave(self):
        if self.filename:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(self.editorText.toPlainText())

    def showMessage(self,pos):
        self._item=self.logTreeWidget.itemAt(pos)
        if self._item:
            self.popMenu=RoundMenu(parent=self)
            self.action1=Action(FluentIcon.COPY,"复制")
            self.action1.triggered.connect(lambda:self.copy(self._item))
            self.action2=Action(FluentIcon.COPY,"复制消息")
            self.action2.triggered.connect(lambda:copy(self._item.text(3)))
            self.action3=Action("切换到日志")
            self.action3.triggered.connect(lambda:self.logWidget.setCurrentWidget(self.logText))
            self.popMenu.addActions([self.action1,self.action2,self.action3])
            self.popMenu.exec_(QCursor.pos())

    def copy(self,item):
        self.word=""
        self.dict = {}
        if item.text(0) == "错误":
            self.dict["type"] = "error"
        else:
            self.dict["type"] = "warning"
        self.dict["col_row"]=item.text(1)+":"+item.text(2)
        self.dict["info"]=item.text(3)
        self.word=dumps(self.dict)
        copy(self.word)

    def run(self):
        self.logWidget.setCurrentWidget(self.logText)
        self.logTreeWidget.clear()
        if self.filename and get_file_extension(self.filename).lower() == "c":
            self.compile = "c_compiler"
        else:
            self.compile = "c++compiler"
        if Path(sets.get(self.compile)).exists() or sets.get(self.compile) == "":
            if not self.filename:
                self.browse, _ = QFileDialog.getSaveFileName(self, "另存为",
                                                             filter="C++文件 (*.cpp *.h *.hpp);;C语言文件 (*.c);;源文件 (*.cpp *.c);;头文件 (*.h *.hpp);;支持C/C++文件 (*.cpp *.c *.h *.hpp);;JSON文件 (*.json);;Python文件 (*.py *.pyi);;所有文件 (*.*)")
                if self.browse:
                    self.editorText.setUsingAutoComplete(True)
                    self.filename = str(self.browse).replace("/", "\\")
                    if get_file_extension(self.browse).lower() in ["cpp", "h", "hpp"]:
                        self.usedsyntax = CppSyntaxHighlighter(self.editorText.document())
                    elif get_file_extension(self.browse).lower() == "c":
                        self.usedsyntax = CppSyntaxHighlighter(self.editorText.document(), True)
                    elif get_file_extension(self.browse).lower() == "json":
                        self.usedsyntax=JsonSyntaxHighlighter(self.editorText.document())
                    elif get_file_extension(self.browse).lower() in ["py","pyi"]:
                        self.usedsyntax=PythonSyntaxHighlighter(self.editorText.document())
                    else:
                        self.editorText.setUsingAutoComplete(False)
                        self.usedsyntax=NullSyntaxHighlighter(self.editorText.document())
                    self.changeTitle()
                    self.autoSave()
            if self.filename:
                if get_file_extension(self.filename).lower() in ["c","cpp","h","hpp"]:
                    self.logText.setPlainText("编译开始")
                    if get_file_extension(self.browse).lower() == "c":
                        self.mode = "cextracompilecmd"
                        self.compile = "c_compiler"
                    else:
                        self.mode = "cppextracompilecmd"
                        self.compile = "c++compiler"
                    self.threads = GenerateFile(self.filename, sets.get(self.compile), get_file_path(self.filename) + ".exe",
                                                sets.get(self.mode).split("\n"))
                    print(self.threads.getGenerateCode())
                    self.threads.start()
                    self.threads.gcclog.connect(self.logConnect)
                    self.threads.errorsignal.connect(self.errSignalRun)
                else:
                    self.msg=MessageBox("错误","此文件不可运行！",self)
                    self.msg.yesButton.setText("确定")
                    self.msg.buttonLayout.insertStretch(1)
                    self.msg.exec()
        else:
            self.msg=MessageBox("错误","编译器未指定或者不存在",self)
            self.msg.yesButton.setText("确定")
            self.msg.cancelButton.hide()
            self.msg.buttonLayout.insertStretch(1)
            self.msg.exec()

    def errSignalRun(self,l1:list[str],l2:list[str]):
        for i in l1:
            self._item=QTreeWidgetItem(self.logTreeWidget)
            self._item.setText(0,"错误")
            self._item.setText(1,i[1])
            self._item.setText(2,i[2])
            self._item.setText(3,i[0])
            self._item.setIcon(0, QIcon(InfoBarIcon.ERROR.path()))
        for i in l2:
            self._item=QTreeWidgetItem(self.logTreeWidget)
            self._item.setText(0,"警告")
            self._item.setText(1,i[1])
            self._item.setText(2,i[2])
            self._item.setText(3,i[0])
            self._item.setIcon(0,QIcon(InfoBarIcon.WARNING.path()))
        if l1 or l2:
            self.logWidget.setCurrentWidget(self.logTreeWidget)

    def logConnect(self, item: str):
        self.logText.setPlainText(self.logText.toPlainText() + "\n" + item)
        if item == "编译可能错误！":
            self.msg = MessageBox("编译错误", "编译可能错误，需要启动上一次编译的程序吗？", self)
            self.msg.yesButton.setText("继续")
            self.msg.cancelButton.setText("取消")
            if self.msg.exec_():
                if not Path(get_file_path(self.filename) + ".exe").exists():
                    self.threads.breakit = True
                    self.threads.exit(-1)
                    self._name = get_file_path(self.filename) + ".exe"
                    self.msg = MessageBox("错误", f"找不到{self._name}，编译未完成！", self)
                    self.msg.yesButton.setText("确定")
                    self.msg.cancelButton.hide()
                    self.msg.buttonLayout.insertStretch(1)
                    self.msg.exec_()
                else:
                    self.threads.success = True
            else:
                self.threads.breakit = True

    def changeTitle(self):
        if self.filename:
            self.setWindowTitle("FluentC++ {} - {}".format(version, self.filename))
        else:
            self.setWindowTitle("FluentC++ {}*".format(version))

    def anotherSave(self):
        self.browse, _ = QFileDialog.getSaveFileName(self, "另存为",
                                                     filter="C++文件 (*.cpp *.h *.hpp);;C语言文件 (*.c);;源文件 (*.cpp *.c);;头文件 (*.h *.hpp);;支持C/C++文件 (*.cpp *.c *.h *.hpp);;JSON文件 (*.json);;Python文件 (*.py *.pyi);;所有文件 (*.*)")
        if self.browse:
            self.editorText.setUsingAutoComplete(True)
            self.filename = str(self.browse).replace("/", "\\")
            if get_file_extension(self.browse).lower() in ["cpp", "h", "hpp"]:
                self.usedsyntax = CppSyntaxHighlighter(self.editorText.document())
            elif get_file_extension(self.browse).lower() == "c":
                self.usedsyntax = CppSyntaxHighlighter(self.editorText.document(), True)
            elif get_file_extension(self.browse).lower() == "json":
                self.usedsyntax=JsonSyntaxHighlighter(self.editorText.document())
            elif get_file_extension(self.browse).lower() in ["py", "pyi"]:
                self.usedsyntax = PythonSyntaxHighlighter(self.editorText.document())
            else:
                self.editorText.setUsingAutoComplete(False)
                self.usedsyntax=NullSyntaxHighlighter(self.editorText.document())
            self.changeTitle()
            self.autoSave()

    def open(self):
        self.browse, _ = QFileDialog.getOpenFileName(self, "打开",
                                                     filter="C++文件 (*.cpp *.h *.hpp);;C语言文件 (*.c);;源文件 (*.cpp *.c);;头文件 (*.h *.hpp);;支持C/C++文件 (*.cpp *.c *.h *.hpp);;JSON文件 (*.json);;Python文件 (*.py *.pyi);;所有文件 (*.*)")
        if self.browse:
            self.filename = str(self.browse).replace("/", "\\")
            self.changeTitle()
            if get_file_extension(self.browse).lower() in ["cpp", "h", "hpp"]:
                self.usedsyntax = CppSyntaxHighlighter(self.editorText.document())
            elif get_file_extension(self.browse).lower() == "c":
                self.usedsyntax = CppSyntaxHighlighter(self.editorText.document(), True)
            elif get_file_extension(self.browse).lower() == "json":
                self.usedsyntax=JsonSyntaxHighlighter(self.editorText.document())
            elif get_file_extension(self.browse).lower() in ["py", "pyi"]:
                self.usedsyntax = PythonSyntaxHighlighter(self.editorText.document())
            else:
                self.usedsyntax=NullSyntaxHighlighter(self.editorText.document())
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
        self.editorText.setGeometry(QRect(QPoint(0, 30), QPoint(self.width() - 50, self.height() // 2 + 130)))
        self.logWidget.setGeometry(
            QRect(QPoint(0, self.height() // 2 + 130), QPoint(self.width() - 50, self.height() - 50)))
        self.settingspivot.setGeometry(QRect(QPoint(0, 0), QPoint(self.width() - 50, 50)))
        self.settingswidget.setGeometry(QRect(QPoint(0, 50), QPoint(self.width() - 50, self.height() - 50)))
        self.card_1a.combobox.setGeometry(QRect(QPoint(300, 20), QPoint(self.width() - 100, 50)))
        self.card_2a.spinbox.setGeometry(QRect(QPoint(300, 20), QPoint(self.width() - 100, 50)))
        self.card_4a.text.setGeometry(QRect(QPoint(300, 20), QPoint(self.width() - 150, 50)))
        self.card_5a.text.setGeometry(QRect(QPoint(300, 20), QPoint(self.width() - 150, 50)))
        self.cppcompile.setGeometry(0, 0, 700, 50)
        self.cppcompiletext.setGeometry(QRect(QPoint(0, 50), QPoint(self.width() - 50, (self.height() - 100) // 2)))
        self.ccompile.setGeometry(0, (self.height() - 100) // 2, 700, 50)
        self.ccompiletext.setGeometry(0, (self.height() - 100) // 2 + 50, self.width() - 50, self.height() - 50)


if __name__ == "__main__":
    translator = FluentTranslator(QLocale(QLocale.Chinese, QLocale.SimplifiedChineseScript, QLocale.China))
    app.installTranslator(translator)
    appfluent = FluentCApp()
    appfluent.show()
    sys.exit(app.exec_())
