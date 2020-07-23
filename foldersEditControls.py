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
    item.songlen = "0"
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


class MyQListWidget(MyQListWidget2):  # 接受 文件夹拖入

    def __init__(self, Form):
        super().__init__(Form)
        self.isDragEnter = False
        self.checkDuplicate = lambda path: False
        self.itemDoubleClicked.connect(self.itemDoubleClickedEVE)

    def dragEnterEvent(self, e):  # 进入
        super().dragEnterEvent(e)
        dirs = getDirs(e)
        for dir in dirs:
            if not self.checkDuplicate(dir):
                self.isDragEnter = True
                e.acceptProposedAction()
                break

    def dragLeaveEvent(self, e):  # 离开
        super().dragLeaveEvent(e)
        if self.isDragEnter:
            self.isDragEnter = False

    def dragMoveEvent(self, e):  # 移动
        super().dragMoveEvent(e)
        if self.isDragEnter:
            e.acceptProposedAction()

    def dropEvent(self, e):  # 放下
        super().dropEvent(e)
        if not self.isDragEnter:
            return
        self.isDragEnter = False
        for path in getDirs(e):
            # 如果拖入的是歌曲,则返回上一层的
            if os.path.isfile(os.path.join(path, "info.dat")) or os.path.isfile(os.path.join(path, "info.json")):
                path = os.path.dirname(path)
            # 查重
            if self.checkDuplicate(path):
                continue

            item = getItem(os.path.basename(path), path, "", False)
            self.addItem(item)


class MyQLabel(QtWidgets.QLabel):  # 支持图片拖入并显示
    def __init__(self, Form):
        super().__init__(Form)
        self.isDragEnter = False
        self.imgloc = ""

    def dragEnterEvent(self, e):  # 进入
        super().dragEnterEvent(e)
        if not get1Img(e) is None:
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

    def dropEvent(self, e):  # 放下
        super().dropEvent(e)
        if not self.isDragEnter:
            return
        self.isDragEnter = False
        self.setimg(get1Img(e))

    def setimg(self, imgloc=None):
        if isinstance(imgloc, str):
            self.imgloc = imgloc
        else:
            self.imgloc = None
        self.refreshImg()

    def refreshImg(self):
        if self.imgloc == None or self.imgloc == '':
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


class MyQTextEdit(QtWidgets.QTextEdit):  # 修改文件夹
    def __init__(self, Form):
        super().__init__(Form)
        self.isDragEnter = False
        self.checkDuplicate = lambda path: False
        self.oldTxt = ""

    def dragEnterEvent(self, e):  # 进入
        super().dragEnterEvent(e)
        dirs = getDirs(e)
        if len(dirs) == 1:
            dir = dirs[0]
            if not self.checkDuplicate(dir):
                e.acceptProposedAction()
                self.isDragEnter = True
                self.oldTxt = self.toPlainText()
                self.setText("松开鼠标以设置")

    def dragLeaveEvent(self, e):  # 离开
        super().dragLeaveEvent(e)
        if self.isDragEnter:
            self.isDragEnter = False
            self.setText(self.oldTxt)

    def dragMoveEvent(self, e):  # 移动
        super().dragMoveEvent(e)
        if self.isDragEnter:
            e.acceptProposedAction()

    def dropEvent(self, e):  # 放下
        super().dropEvent(e)
        if not self.isDragEnter:
            return
        self.isDragEnter = False
        self.setText(getDirs(e)[0])


def getData(e):
    m = e.mimeData()
    if not m.hasText():
        return []
    sps = m.text().splitlines()
    files = []
    for line in sps:
        if line.startswith('file:///'):
            files.append(line[8:])
    # print("getData", files)
    return files


def getDirs(e):
    dirs = []
    data = getData(e)
    for d in data:
        if os.path.isdir(d):
            dirs.append(d)
    # print("getDirs", dirs)
    return dirs


def getFile(e):
    data = getData(e)
    files = []
    for d in data:
        if os.path.isfile(d):
            files.append(d)
    if len(files) == 1:
        # print("getFile", files[0])
        return files[0]


def get1Img(e):
    f = getFile(e)
    if not f is None:
        if not imghdr.what(f) is None:  # 受支持的格式
            # print("get1Img", f)
            return f


if __name__ == "__main__":
    print(type("imgloc"))
