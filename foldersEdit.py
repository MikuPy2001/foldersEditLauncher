# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'foldersEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(542, 672)
        self.listWidget2 = MyQListWidget(Form)
        self.listWidget2.setGeometry(QtCore.QRect(170, 30, 150, 481))
        self.listWidget2.setMinimumSize(QtCore.QSize(150, 0))
        self.listWidget2.setAcceptDrops(True)
        self.listWidget2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget2.setObjectName("listWidget2")
        self.listWidget1 = MyQListWidget(Form)
        self.listWidget1.setGeometry(QtCore.QRect(10, 360, 150, 300))
        self.listWidget1.setMinimumSize(QtCore.QSize(150, 0))
        self.listWidget1.setAcceptDrops(True)
        self.listWidget1.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget1.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget1.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget1.setObjectName("listWidget1")
        self.listWidget0 = MyQListWidget(Form)
        self.listWidget0.setGeometry(QtCore.QRect(10, 30, 150, 300))
        self.listWidget0.setMinimumSize(QtCore.QSize(150, 0))
        self.listWidget0.setAcceptDrops(True)
        self.listWidget0.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget0.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget0.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget0.setObjectName("listWidget0")
        self.no_uss_label_1 = QtWidgets.QLabel(Form)
        self.no_uss_label_1.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.no_uss_label_1.setObjectName("no_uss_label_1")
        self.no_uss_label_2 = QtWidgets.QLabel(Form)
        self.no_uss_label_2.setGeometry(QtCore.QRect(10, 340, 151, 16))
        self.no_uss_label_2.setObjectName("no_uss_label_2")
        self.no_uss_label_3 = QtWidgets.QLabel(Form)
        self.no_uss_label_3.setGeometry(QtCore.QRect(170, 10, 151, 16))
        self.no_uss_label_3.setObjectName("no_uss_label_3")
        self.no_uss_label_4 = QtWidgets.QLabel(Form)
        self.no_uss_label_4.setGeometry(QtCore.QRect(330, 540, 201, 16))
        self.no_uss_label_4.setObjectName("no_uss_label_4")
        self.listWidgetDel = MyQListWidget(Form)
        self.listWidgetDel.setGeometry(QtCore.QRect(170, 539, 150, 121))
        self.listWidgetDel.setMinimumSize(QtCore.QSize(150, 0))
        self.listWidgetDel.setAcceptDrops(True)
        self.listWidgetDel.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidgetDel.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidgetDel.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidgetDel.setObjectName("listWidgetDel")
        self.no_uss_label_5 = QtWidgets.QLabel(Form)
        self.no_uss_label_5.setGeometry(QtCore.QRect(170, 520, 151, 16))
        self.no_uss_label_5.setObjectName("no_uss_label_5")
        self.ImagePath = MyQLabel(Form)
        self.ImagePath.setGeometry(QtCore.QRect(330, 240, 200, 200))
        self.ImagePath.setAcceptDrops(True)
        self.ImagePath.setStyleSheet("border:1px solid red;")
        self.ImagePath.setScaledContents(True)
        self.ImagePath.setAlignment(QtCore.Qt.AlignCenter)
        self.ImagePath.setObjectName("ImagePath")
        self.no_uss_label_7 = QtWidgets.QLabel(Form)
        self.no_uss_label_7.setGeometry(QtCore.QRect(330, 10, 201, 16))
        self.no_uss_label_7.setObjectName("no_uss_label_7")
        self.no_uss_label_8 = QtWidgets.QLabel(Form)
        self.no_uss_label_8.setGeometry(QtCore.QRect(330, 560, 201, 16))
        self.no_uss_label_8.setObjectName("no_uss_label_8")
        self.WIP = QtWidgets.QCheckBox(Form)
        self.WIP.setGeometry(QtCore.QRect(330, 220, 191, 16))
        self.WIP.setObjectName("WIP")
        self.savefile = QtWidgets.QPushButton(Form)
        self.savefile.setGeometry(QtCore.QRect(330, 470, 201, 41))
        self.savefile.setObjectName("savefile")
        self.Path = QtWidgets.QTextEdit(Form)
        self.Path.setGeometry(QtCore.QRect(330, 30, 201, 131))
        self.Path.setObjectName("Path")
        self.no_uss_label_9 = QtWidgets.QLabel(Form)
        self.no_uss_label_9.setGeometry(QtCore.QRect(330, 580, 201, 16))
        self.no_uss_label_9.setObjectName("no_uss_label_9")
        self.no_uss_label_6 = QtWidgets.QLabel(Form)
        self.no_uss_label_6.setGeometry(QtCore.QRect(330, 200, 201, 16))
        self.no_uss_label_6.setObjectName("no_uss_label_6")
        self.no_uss_label_10 = QtWidgets.QLabel(Form)
        self.no_uss_label_10.setGeometry(QtCore.QRect(330, 600, 201, 16))
        self.no_uss_label_10.setObjectName("no_uss_label_10")
        self.no_uss_label_11 = QtWidgets.QLabel(Form)
        self.no_uss_label_11.setGeometry(QtCore.QRect(330, 620, 201, 16))
        self.no_uss_label_11.setObjectName("no_uss_label_11")
        self.no_uss_label_12 = QtWidgets.QLabel(Form)
        self.no_uss_label_12.setGeometry(QtCore.QRect(330, 640, 201, 16))
        self.no_uss_label_12.setObjectName("no_uss_label_12")
        self.no_uss_label_13 = QtWidgets.QLabel(Form)
        self.no_uss_label_13.setGeometry(QtCore.QRect(330, 170, 131, 16))
        self.no_uss_label_13.setObjectName("no_uss_label_13")
        self.songlen = QtWidgets.QLabel(Form)
        self.songlen.setGeometry(QtCore.QRect(460, 170, 71, 16))
        self.songlen.setObjectName("songlen")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "歌包管理 - 最可爱的塔塔喵出品"))
        self.no_uss_label_1.setText(_translate("Form", "默认歌包的子目录"))
        self.no_uss_label_2.setText(_translate("Form", "WIP歌包的子目录"))
        self.no_uss_label_3.setText(_translate("Form", "自定义歌包"))
        self.no_uss_label_4.setText(_translate("Form", "将文件夹拖入即可添加"))
        self.no_uss_label_5.setText(_translate("Form", "回收站"))
        self.ImagePath.setText(_translate("Form", "拖入图片即可更换封面"))
        self.no_uss_label_7.setText(_translate("Form", "文件夹路径"))
        self.no_uss_label_8.setText(_translate("Form", "拖动排序以及归类"))
        self.WIP.setText(_translate("Form", "设为练习专用歌包"))
        self.savefile.setText(_translate("Form", "保存文件"))
        self.no_uss_label_9.setText(_translate("Form", "回收站的条目将不会被保存"))
        self.no_uss_label_6.setText(_translate("Form", "以下设置仅限自定义歌包有效"))
        self.no_uss_label_10.setText(_translate("Form", "双击即可修改名称"))
        self.no_uss_label_11.setText(_translate("Form", "-1"))
        self.no_uss_label_12.setText(_translate("Form", "-"))
        self.no_uss_label_13.setText(_translate("Form", "本目录含有歌曲数量为:"))
        self.songlen.setText(_translate("Form", "0"))
from foldersEditControls import MyQLabel, MyQListWidget
