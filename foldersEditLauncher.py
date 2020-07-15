import ctypes
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from foldersEdit import Ui_Form
import foldersEditControls

import os
from os import path
from xml.dom.minidom import parse


def getNodeData(xml, TagName, default=""):
    Nodes = xml.getElementsByTagName(TagName)
    if len(Nodes) > 0:
        return Nodes[0].firstChild.data
    else:
        return default


class 窗口事件处理(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # self.无用代码()
        self.loadxml()
        self.nowitem = None

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

    def loadxml(self):
        # foldersfile = path.join(os.getcwd(), 'Beat Saber', 'UserData',
        #                         'SongCore', 'folders (2).xml')
        foldersfile = path.join(os.getcwd(),  'UserData',
                                'SongCore', 'folders.xml')
        if not path.isfile(foldersfile):  # 没有自定义目录
            return
        folders = parse(
            foldersfile).documentElement.getElementsByTagName("folder")
        print(("一共有", len(folders), "个目录被读取"))
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
