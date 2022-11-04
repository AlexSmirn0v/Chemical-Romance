import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui
from Substance import Substance
from Theory import up, under
from Class_father import Class_father


class Sub_name(Class_father):
    def __init__(self, parent=None, *args):
        super().__init__()
        uic.loadUi('Sub_name.ui', self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        self.parenter = parent
        self.initUI()
        if args:
            self.first_sub = Substance(args[0][0])
            self.temp_list = args[0][0]
            self.htmler(str(self.first_sub))

    def resulter(self):
        self.first_sub = Substance(self.temp_list)
        self.htmler(' => ')
        self.Name.setPlainText(self.first_sub.get_name())
        self.Type.setText('Тип: ' + self.first_sub.get_type())

    def clearer(self):
        self.textBrowser.setHtml(None)
        self.Name.setHtml(None)
        self.Type.setText('Тип: ')
        self.temp_list = list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Sub_name()
    ex.show()
    sys.exit(app.exec_())