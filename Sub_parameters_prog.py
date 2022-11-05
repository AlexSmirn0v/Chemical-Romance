import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui

from Substance import Substance
from Theory import up, under, isSoluble
from Class_father import Class_father


class Sub_parameters(Class_father):
    def __init__(self, parent=None, *args):
        super().__init__()
        uic.loadUi('Sub_parameters.ui', self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        self.parenter = parent
        self.initUI()
        if args:
            self.first_sub = Substance(args[0][0])
            self.temp_list = args[0][0]
            self.htmler(str(self.first_sub))

    def resulter(self):
        self.sub = Substance(self.temp_list)
        res_oxi = self.sub.get_oxi()
        if self.sub.only_el_str == 'H2O':
            res_sol = 'Растворима ли вода в воде?'
        elif self.sub.only_el_str == 'OF2':
            res_sol = 'Вещество не растворимо в воде'
        else:
            is_sol = isSoluble(self.sub)
            if is_sol:
                res_sol = 'Вещество растворимо в воде'
            elif is_sol is None:
                res_sol = 'Ошибка ввода или несуществующее соединение'
            else:
                res_sol = 'Вещество не растворимо в воде'

        self.Valence_Oxidation.setHtml(f'Степень окисления: {res_oxi}<br>{res_sol}')

    def clearer(self):
        self.textBrowser.setHtml(None)
        self.Valence_Oxidation.setHtml('Степень окисления:<br>Растворимость в воде')
        self.temp_list = list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Sub_parameters()
    ex.show()
    sys.exit(app.exec_())