import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from 歌曲文件夹 import Ui_Form


class 窗口事件处理(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.无用代码()

    def initUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('Icon.png'))
        # 禁止最大化按钮
        self.setWindowFlags(
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint)
        # 禁止拉伸窗口大小
        self.setFixedSize(self.width(), self.height())

        self.show()

    def 无用代码(self):
        # 无用代码
        for i in range(10):
            item = QtWidgets.QListWidgetItem()
            item.setText(f"默认-{i}")
            self.ui.listWidget1.addItem(item)
        for i in range(10):
            item = QtWidgets.QListWidgetItem()
            item.setText(f"自定义-{i}")
            self.ui.listWidget3.addItem(item)

    def closeEvent(self, e):
        print("窗口被关闭了")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = 窗口事件处理()
    sys.exit(app.exec_())
