import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui
from Substance import Substance
from Class_father import Class_father
from Chem_calc import Ui_MainWindow


class Chem_calc(Ui_MainWindow, Class_father):
    def __init__(self, parent=None, *args):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        self.parenter = parent
        self.initUI()
        if args:
            print(args[0][0])
            self.first_sub = Substance(args[0][0])
            self.temp_list = args[0][0]
            self.htmler(str(self.first_sub))

    def resulter(self):
        self.sec_sub = Substance(self.temp_list)
        print(self.first_sub)
        tulip = self.first_sub + self.sec_sub
        print(' + '.join(map(str, tulip)))
        self.htmler(' => ' + ' + '.join(map(str, tulip)))
        if tulip[0] is Substance:
            self.temp_list = tulip[0].el_list

    def pluser(self):
        self.htmler(' + ')
        self.first_sub = Substance(self.temp_list.copy())
        print(self.first_sub)
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