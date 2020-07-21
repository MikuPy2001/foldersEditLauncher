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
        self.nowitem = None
        self.initUI()
        self.setGameLoc(gamebasedir)

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
        # 关联点击事件,单击即可开始编辑
        self.ui.listWidget0.itemClicked.connect(self.listItemClickedEVE)
        self.ui.listWidget1.itemClicked.connect(self.listItemClickedEVE)
        self.ui.listWidget2.itemClicked.connect(self.listItemClickedEVE)
        self.ui.listWidgetDel.itemClicked.connect(self.listItemClickedEVE)
        self.nowitem = None
        self.ui.savefile.clicked.connect(self.savexml)

        self.show()

    def listItemClickedEVE(self, item):
        if not self.nowitem is None:
            self.nowitem.Path = self.ui.Path.toPlainText()
            self.nowitem.ImagePath = self.ui.ImagePath.imgloc
            self.nowitem.WIP = self.ui.WIP.isChecked()
        if item is None:
            self.nowitem = None
            self.ui.Path.setPlainText("请选择一个")
            self.ui.ImagePath.imgloc = item.ImagePath
            self.ui.WIP.setChecked(item.WIP)
            self.ui.ImagePath.refreshImg()
            self.ui.songlen.setText("0")
        else:
            self.nowitem = item
            self.ui.Path.setPlainText(item.Path)
            self.ui.ImagePath.imgloc = item.ImagePath
            self.ui.WIP.setChecked(item.WIP)
            self.ui.ImagePath.refreshImg()
            self.ui.songlen.setText(item.songlen)

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
        print(loc)
        loc = os.path.join(
            loc, "UserData", "SongCore", "folders.xml")
        self.xmlLoc = loc
        self.loadxml()

    def loadxml(self):
        # 从xml初始化列表
        if not path.isfile(self.xmlLoc):  # 没有自定义目录
            return
        with open(self.xmlLoc, 'r', encoding="utf-8") as f:
            folders = minidom.parseString(
                f.read()).documentElement.getElementsByTagName("folder")
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

    def savexml(self):
        # 列表保存到文件
        doc = Document()
        folders = doc.createElement("folders")
        doc.appendChild(folders)
        setNodeData(doc, folders, self.ui.listWidget0, 0)
        setNodeData(doc, folders, self.ui.listWidget1, 1)
        setNodeData(doc, folders, self.ui.listWidget2, 2)
        with open(self.xmlLoc, 'w', encoding="utf-8") as f:
            f.write(doc.toprettyxml())

    def closeEvent(self, e):
        print("窗口被关闭了")


if __name__ == "__main__":
    gamed = gameDir.getBeatSaberDir()
    app = QtWidgets.QApplication(sys.argv)
    widget = 窗口事件处理(gamed)  # 窗口事件处理 使用UI生成的,不要改
    sys.exit(app.exec_())
    print("程序结束了")
