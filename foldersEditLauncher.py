import time
import ctypes
import os
import sys
from codecs import open
from os import path
from xml.dom import minidom
from xml.dom.minidom import Document, parse, parseString

from PyQt5 import QtCore, QtGui, QtWidgets

import foldersEditControls
import gameDir
from foldersEdit import Ui_Form


def getNodeData(doc, TagName, default=""):
    # 从xml子节点拿到特定tag的文本数据
    Nodes = doc.getElementsByTagName(TagName)
    if len(Nodes) == 0:
        return default
    node = Nodes[0].firstChild
    if node is None:
        return default
    return node.data


def setNodeText(doc, fatherNode, nodeName, nodeText):
    # 为指定子节点设置一个文本节点
    node = doc.createElement(nodeName)
    node.appendChild(
        doc.createTextNode(
            str(
                nodeText
            )
        )
    )
    fatherNode.appendChild(node)


def setNodeData(doc, fatherNode, list, pack):
    # 将列表数据添加到xml里
    for i in range(list.count()):
        item = list.item(i)
        folder = doc.createElement("folder")

        setNodeText(doc, folder, "Name", item.text())
        setNodeText(doc, folder, "Path", item.Path)
        setNodeText(doc, folder, "ImagePath", item.ImagePath)
        setNodeText(doc, folder, "WIP", item.WIP)
        setNodeText(doc, folder, "Pack", pack)

        fatherNode.appendChild(folder)


class 窗口事件处理(QtWidgets.QWidget):
    def __init__(self, gamebasedir=None):
        super().__init__()
        self.initUI()  # 初始化界面
        self.show()  # 显示界面
        self.initLogic()  # 初始化逻辑
        self.setGameLoc(gamebasedir)  # 初始化数据

    def initUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 这是为了解决window下不能设置任务栏图标的bug
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "foldersEdit")
        # 设置图片
        self.setWindowIcon(QtGui.QIcon('Icon.png'))
        # 禁止最大化按钮
        self.setWindowFlags(
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint)
        # 禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

    def initLogic(self):
        # 设置列表通用属性
        self.list = [self.ui.listWidget0, self.ui.listWidget1,
                     self.ui.listWidget2, self.ui.listWidgetDel]
        self.nowitem = None
        for list in self.list:
            # 关联点击事件,单击即可开始编辑
            list.itemClicked.connect(self.listItemClickedEVE)
            # 查重
            list.checkDuplicate = self.checkDuplicate
        self.ui.Path.checkDuplicate = self.checkDuplicate
        self.nowitem = None
        self.ui.savefile.clicked.connect(self.savexml)
        self.ui.delimg.clicked.connect(self.ui.ImagePath.setimg)

    def listItemClickedEVE(self, item):
        if not self.nowitem is None:
            self.nowitem.Path = self.ui.Path.toPlainText()
            self.nowitem.ImagePath = self.ui.ImagePath.imgloc
            self.nowitem.WIP = self.ui.WIP.isChecked()
        if item is None:
            self.nowitem = None
            self.ui.Path.setPlainText("请选择一个")
            self.ui.ImagePath.setimg('')
            self.ui.WIP.setChecked(False)
            self.ui.songlen.setText("0")
        else:
            self.nowitem = item
            self.ui.Path.setPlainText(item.Path)
            self.ui.ImagePath.setimg(item.ImagePath)
            self.ui.WIP.setChecked(item.WIP)
            self.ui.songlen.setText(item.songlen)

    def checkDuplicate(self, path):
        for list in self.list:
            for i in range(list.count()):
                if list.item(i).Path == path:
                    return True
        return False

    def setGameLoc(self, loc):
        if loc is None or not os.path.isdir(loc):
            loc = QtWidgets.QFileDialog.getOpenFileName(
                self, '请选定游戏主文件',  # 标题
                os.getcwd(),  # 起始目录
                "游戏主文件(*Saber.exe)",  # 过滤器
            )
            if loc[0] == '':
                sys.exit(0)
                return
            loc = os.path.dirname(loc[0])
            gameDir.saveFile(loc)
        print(loc)
        loc = os.path.join(
            loc, "UserData", "SongCore", "folders.xml")
        self.xmlLoc = loc
        self.loadxml()
        self.rawXml = self.toXml()

    def loadxml(self):
        # 从xml初始化列表
        if not path.isfile(self.xmlLoc):  # 没有自定义目录
            return
        with open(self.xmlLoc, 'r', encoding="utf-8") as f:
            doc = minidom.parseString(f.read())
            folders = doc.documentElement.getElementsByTagName("folder")
        print(("一共有", len(folders), "个目录被读取"))
        self.ui.listWidget0.clear()
        self.ui.listWidget1.clear()
        self.ui.listWidget2.clear()
        self.ui.listWidgetDel.clear()

        for folder in folders:
            item = foldersEditControls.getItem(
                getNodeData(folder, 'Name'),
                getNodeData(folder, 'Path'),
                getNodeData(folder, 'ImagePath'),
                getNodeData(folder, 'WIP').lower() == 'true'
            )
            Pack = getNodeData(folder, 'Pack')
            if Pack == '0':
                self.ui.listWidget0.addItem(item)
            elif Pack == '1':
                self.ui.listWidget1.addItem(item)
            elif Pack == '2':
                self.ui.listWidget2.addItem(item)
            else:
                self.ui.listWidgetDel.addItem(item)

    def toXml(self):
        # 列表保存到string
        doc = Document()
        folders = doc.createElement("folders")
        doc.appendChild(folders)
        setNodeData(doc, folders, self.ui.listWidget0, 0)
        setNodeData(doc, folders, self.ui.listWidget1, 1)
        setNodeData(doc, folders, self.ui.listWidget2, 2)
        return doc.toprettyxml()

    def savexml(self):
        self.rawXml = self.toXml()
        with open(self.xmlLoc, 'w', encoding="utf-8") as f:
            f.write(self.rawXml)

    def closeEvent(self, e):
        if not self.nowitem is None:
            self.nowitem.Path = self.ui.Path.toPlainText()
            self.nowitem.ImagePath = self.ui.ImagePath.imgloc
            self.nowitem.WIP = self.ui.WIP.isChecked()
        newxml = self.toXml()
        if self.rawXml != newxml:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("保存提示")
            box.setText("文件已被修改,是否保存")
            box.addButton("保存", box.AcceptRole)
            box.addButton("不保存", box.DestructiveRole)
            box.addButton("取消", box.RejectRole)
            box.setIcon(box.Question)
            box.setWindowIcon(QtGui.QIcon('Icon.png'))
            res = box.exec()
            if res == box.AcceptRole:
                self.savexml()
            elif res == box.DestructiveRole:
                e.ignore()
        print("窗口被关闭了")


if __name__ == "__main__":
    stat = time.time()
    gamed = gameDir.getBeatSaberDir()
    app = QtWidgets.QApplication(sys.argv)
    widget = 窗口事件处理(gamed)  # 窗口事件处理 使用UI生成的,不要改
    end = time.time()
    print("显示窗口花费了", end-stat)
    sys.exit(app.exec_())
    print("程序结束了")
