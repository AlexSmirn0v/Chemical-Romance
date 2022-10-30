import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap

from Chem_calc_prog import Chem_calc
from Elem_parameters_prog import Elem_parameters


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Start_page.ui', self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        self.initUI()

    def initUI(self):
        self.logo.setPixmap(QPixmap('Chemical Romance reduced logo.jpg'))
        self.logoChemCalc.setPixmap(QPixmap('logo_Chem_calc.png'))
        self.logoSubName.setPixmap(QPixmap('logo_Sub_name.png'))
        self.logoSubParameters.setPixmap(QPixmap('logo_Sub_parameters.png'))
        self.logoElemParameters.setPixmap(QPixmap('logo_Elem_parameters.png'))

        self.chemReactions.clicked.connect(self.open_Chem_calc)
        self.subName.clicked.connect(self.open_Sub_name)
        self.subParameters.clicked.connect(self.open_Sub_parameters)
        self.elemParameters.clicked.connect(self.open_Elem_parameters)

    def open_Chem_calc(self):
        self.Chem_calc = Chem_calc()
        self.Chem_calc.show()
        self.hide()

    def open_Sub_name(self):
        print(self.sender().text())

    def open_Sub_parameters(self):
        print(self.sender().text())

    def open_Elem_parameters(self):
        self.Elem_parameters = Elem_parameters()
        self.Elem_parameters.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())