import traceback
import types
import imghdr
import os
import json
from PyQt5 import QtCore, QtGui, QtWidgets


def getItem(Name, Path, ImagePath, WIP):
    item = QtWidgets.QListWidgetIte()
    item.setText(Name)
    item.Path = Path
    item.ImagePath = ImagePath
    item.WIP = WIP
    return item


# class MyQListWidgetItem(QtWidgets.QListWidgetItem):
#     def __init__(self):
#         super().__init__()
#         print("项目初始化")


class MyQListWidget1(QtWidgets.QListWidget):  # 解决item拖放问题
    # dropFormat="application/x-MyQListWidget1List"
    dropFormat = "application/x-qabstractitemmodeldatalist"

    def mimeData(self, items):  # 拖出序列化
        j = []
        for item in items:
            j.append([item.text(), item.Path, item.ImagePath, item.WIP])
        jsonstr = json.dumps(j)
        jsongbyte = jsonstr.encode("utf-8")
        data = QtCore.QMimeData()
        data.setData(self.dropFormat,
                     QtCore.QByteArray(jsongbyte))
        return data

    def dropMimeData(self, index, data, action):  # 插入序列化
        if not data.hasFormat(self.dropFormat):
            return super().dropMimeData(index, data, action)
        # print("自己插入的")
        jsonQByteArray = data.data(self.dropFormat)
        jsonbyte = jsonQByteArray.data()
        jsonstr = str(jsonbyte, encoding="utf-8")
        itemlist = json.loads(jsonstr)
        for itemstrs in itemlist:
            self.insertItem(index, getItem(
                itemstrs[0],
                itemstrs[1],
                itemstrs[2],
                itemstrs[3]
            ))
            index += 1

        return True

    # def dragEnterEvent(self, e):  # 进入
    #     super().dragEnterEvent(e)
    #     if e.mimeData().hasFormat(self.dropFormat):
    #         e.acceptProposedAction()

    # def dragMoveEvent(self, e):  # 移动
    #     super().dragMoveEvent(e)
    #     if e.mimeData().hasFormat(self.dropFormat):
    #         e.acceptProposedAction()


class MyQListWidget2(MyQListWidget1):  # 双击编辑item
    def __init__(self, Form):
        super().__init__(Form)
        self.itemDoubleClicked.connect(self.itemDoubleClickedEVE)

    def itemDoubleClickedEVE(self, item):
        # self.openPersistentEditor(item)
        item.setFlags(
            item.flags() |
            QtCore.Qt.ItemIsEditable
        )


class MyQListWidget(MyQListWidget2):  # 接受 文件拖入

    def __init__(self, Form):
        super().__init__(Form)
        self.isDragEnter = False
        self.itemDoubleClicked.connect(self.itemDoubleClickedEVE)

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

    def __init__(self, Form):
        super().__init__(Form)
        self.imgloc = ""

    def dragEnterEvent(self, e):  # 进入
        super().dragEnterEvent(e)
        # TODO 检查拖放类型
        path = e.mimeData().text().replace('file:///', '')
        paths = path.splitlines()
        if len(paths) > 1:
            print("不支持多文件")
            return
        imgType = imghdr.what(path)
        if imgType in self.imgType_list:  # 受支持的格式
            self.isDragEnter = True
            # self.pixmapbak = self.pixmap
            # print(self.pixmapbak)
            # self.setText("松开鼠标以设置封面")
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

        self.imgloc = path

    def refreshImg(self):
        imgType = imghdr.what(self.imgloc)
        if imgType in self.imgType_list:  # 受支持的格式
            pix = QtGui.QPixmap(self.imgloc)
            self.setPixmap(pix)
