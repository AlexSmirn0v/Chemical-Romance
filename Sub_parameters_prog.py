import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui

from Substance import Substance
from Theory import isSoluble
from Class_father import Class_father
from Sub_parameters import Ui_MainWindow


class Sub_parameters(Ui_MainWindow, Class_father):
    def __init__(self, parent=None, *args):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        self.parenter = parent
        self.initUI()
        if args:
            self.first_sub = Substance(args[0][0])
            self.temp_list = args[0][0]
            print(str(self.first_sub))
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