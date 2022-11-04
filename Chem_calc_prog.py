import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui
from Substance import Substance
from Theory import up, under
from Class_father import Class_father


class Chem_calc(Class_father):
    def __init__(self, parent=None, *args):
        super().__init__()
        uic.loadUi('Chem_calc.ui', self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        self.parenter = parent
        self.initUI()
        if args:
            self.first_sub = Substance(args[0][0])
            self.temp_list = args[0][0]
            self.htmler(str(self.first_sub))

    def resulter(self):
        self.sec_sub = Substance(self.temp_list)
        self.htmler(' => ' + str(self.first_sub + self.sec_sub))

    def pluser(self):
        self.htmler(' + ')
        self.first_sub = Substance(self.temp_list)
        self.temp_list.clear()

    def clearer(self):
        self.textBrowser.setHtml(None)
        self.first_sub, self.sec_sub = None, None
        self.temp_list = list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Chem_calc()
    ex.show()
    sys.exit(app.exec_())