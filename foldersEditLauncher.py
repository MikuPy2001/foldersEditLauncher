from codecs import open
import ctypes
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from foldersEdit import Ui_Form
import foldersEditControls

import os
from os import path
from xml.dom.minidom import parse, Document, parseString
from xml.dom import minidom


def getNodeData(doc, TagName, default=""):
    Nodes = doc.getElementsByTagName(TagName)
    if len(Nodes) == 0:
        return default
    node = Nodes[0].firstChild
    if node is None:
        return default
    return node.data


def setNodeText(doc, fatherNode, nodeName, nodeText):
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
    def __init__(self):
        super().__init__()
        self.nowitem = None
        self.initUI()
        # self.无用代码()
        self.setXmlLoc()
        self.loadxml()

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
        self.nowitem = item
        self.ui.Path.setPlainText(item.Path)
        self.ui.ImagePath.imgloc = item.ImagePath
        self.ui.WIP.setChecked(item.WIP)
        self.ui.ImagePath.refreshImg()

    def setXmlLoc(self):
        self.xmlLoc = path.join(
            os.getcwd(),
            'Beat Saber',
            'UserData', 'SongCore', 'folders.xml')

    def savexml(self):
        doc = Document()
        folders = doc.createElement("folders")
        doc.appendChild(folders)
        setNodeData(doc, folders, self.ui.listWidget0, 0)
        setNodeData(doc, folders, self.ui.listWidget1, 1)
        setNodeData(doc, folders, self.ui.listWidget2, 2)
        with open(self.xmlLoc, 'w', encoding="utf-8") as f:
            f.write(doc.toprettyxml())

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

    def 无用代码(self):
        # 无用代码
        for i in range(10):
            item = QtWidgets.QListWidgetItem()
            item.setText(f"默认-{i}")
            self.ui.listWidget0.addItem(item)
        for i in range(10):
            item = QtWidgets.QListWidgetItem()
            item.setText(f"自定义-{i}")
            self.ui.listWidget2.addItem(item)

    def closeEvent(self, e):
        print("窗口被关闭了")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = 窗口事件处理()  # 窗口事件处理 使用UI生成的,不要改
    sys.exit(app.exec_())
