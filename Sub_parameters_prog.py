import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui

from Substance import Substance
from Theory import up, under
from Class_father import Class_father


class Sub_parameters(Class_father):
    def __init__(self, parent=None, *args):
        super().__init__()
        uic.loadUi('Sub_parameters.ui', self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        self.parenter = parent
        self.initUI()

    def resulter(self):
        self.sub = Substance(self.temp_list)
        self.Valence_Oxidation.setHtml(f'Valence: {self.sub.get_valence}<br>Oxidation state: {self.sub.get_oxi}')

    def clearer(self):
        self.textBrowser.setHtml(None)
        self.Valence_Oxidation.setHtml('Valence: <br>Oxidation state:')
        self.temp_list = list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Sub_parameters()
    ex.show()
    sys.exit(app.exec_())