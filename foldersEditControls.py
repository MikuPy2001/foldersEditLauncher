import imghdr
import json
import os
import traceback
import types

from PyQt5 import QtCore, QtGui, QtWidgets


def getItem(Name, Path, ImagePath, WIP):
    item = QtWidgets.QListWidgetItem()
    item.setText(Name)
    item.Path = Path
    item.ImagePath = ImagePath
    item.WIP = WIP
    return item


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
        m = e.mimeData()

        if not (m.hasText() and m.text().startswith('file:///')):
            # print("不受支持的类型")
            return

        path = m.text().replace('file:///', '')
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
                # 如果拖入的是歌曲,则返回上一层的
                if os.path.isfile(os.path.join(path, "info.dat")) or os.path.isfile(os.path.join(path, "info.json")):
                    path = os.path.dirname(path)
                
                item = getItem(os.path.basename(path), path, "", False)
                self.addItem(item)
    def setCheckDuplicate(self,callBack):
        self.callBack=callBack
    def CheckDuplicate(self):
        return False


class MyQLabel(QtWidgets.QLabel):  # 支持图片拖入并显示
    # imgType_list = ['jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif']

    def __init__(self, Form):
        super().__init__(Form)
        self.imgloc = ""

    def dragEnterEvent(self, e):  # 进入
        super().dragEnterEvent(e)
        m = e.mimeData()
        # TODO 检查拖放类型
        if not (m.hasText() and m.text().startswith('file:///')):
            # print("不受支持的类型")
            return

        path = m.text().replace('file:///', '')
        if len(path.splitlines()) > 1:
            # print("不支持多文件")
            return
        if not os.path.isfile(path):
            # print("不是文件")
            return

        imgType = imghdr.what(path)
        if imgType is None:  # 受支持的格式
            print(("格式不受支持:", imgType))
            return

        e.acceptProposedAction()
        self.isDragEnter = True
        self.setText("松开鼠标以设置封面")

    def dragLeaveEvent(self, e):  # 离开
        super().dragLeaveEvent(e)
        if self.isDragEnter:
            self.isDragEnter = False
        self.refreshImg()

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
        self.refreshImg()

    def refreshImg(self):
        if self.imgloc == '':
            self.setText("拖入图片即可更换封面")
            return
        if not os.path.isfile(self.imgloc):
            self.setText("封面文件无效")
            return
        imgType = imghdr.what(self.imgloc)
        if imgType is None:  # 受支持的格式
            self.setText("封面无法解析")
            return
        pix = QtGui.QPixmap(self.imgloc)
        self.setPixmap(pix)
