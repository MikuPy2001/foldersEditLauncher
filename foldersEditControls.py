import imghdr
import os

from PyQt5 import QtCore, QtGui, QtWidgets


class MyQListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self):
        super().__init__()
        self.setFlags(
            QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsEditable)


class MyQListWidget(QtWidgets.QListWidget):
    def __init__(self, Form):
        super().__init__(Form)
        self.isDragEnter = False

    def dragEnterEvent(self, e):  # 进入
        super().dragEnterEvent(e)
        path = e.mimeData().text().replace('file:///', '')
        paths = path.splitlines()
        for path in paths:
            if os.path.isdir(path):
                self.isDragEnter = True
                e.acceptProposedAction()
                return

    def dragLeaveEvent(self, e):  # 离开
        super().dragLeaveEvent(e)
        if self.isDragEnter:
            self.isDragEnter = False

    def dragMoveEvent(self, e):  # 移动
        super().dragMoveEvent(e)
        if self.isDragEnter:
            e.acceptProposedAction()

    def dropEvent(self, e):  # 放下文件后的动作
        super().dropEvent(e)
        if not self.isDragEnter:
            return
        self.isDragEnter = False
        path = e.mimeData().text().replace('file:///', '')  # 删除多余开头
        paths = path.splitlines()
        print("收到以下文件夹")
        for path in paths:
            if os.path.isdir(path):
                print(path)


class MyQLabel(QtWidgets.QLabel):
    imgType_list = ['jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif']

    def dragEnterEvent(self, e):  # 进入
        super().dragEnterEvent(e)
        path = e.mimeData().text().replace('file:///', '')
        paths = path.splitlines()
        if len(paths) > 1:
            print("不支持多文件")
            return
        imgType = imghdr.what(path)
        if imgType in self.imgType_list:  # 受支持的格式
            self.isDragEnter = True
            e.acceptProposedAction()
        else:
            print("格式不受支持:"+imgType)

    def dragLeaveEvent(self, e):  # 离开
        super().dragLeaveEvent(e)
        if self.isDragEnter:
            self.isDragEnter = False

    def dragMoveEvent(self, e):  # 移动
        super().dragMoveEvent(e)
        if self.isDragEnter:
            e.acceptProposedAction()

    def dropEvent(self, e):  # 放下文件后的动作
        super().dropEvent(e)
        if not self.isDragEnter:
            return
        self.isDragEnter = False
        path = e.mimeData().text().replace('file:///', '')  # 删除多余开头

        pix = QtGui.QPixmap(path)
        self.setPixmap(pix)
