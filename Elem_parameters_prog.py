import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui
from Theory import up, under, elem_parameters
from Class_father import Class_father


class Elem_parameters(Class_father):
    def __init__(self, parent=None, *args):
        super().__init__()
        uic.loadUi('Elem_parameters.ui', self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        self.parenter = parent
        self.initUI()
        if args:
            n = 0
            while type(args[0][0][n]) == int:
                n += 1
            text = args[0][0][n]
            el_params = elem_parameters(text)
            self.textBrowser.setPlainText(text)
            self.Name.setText(' Имя: ' + el_params['rusName'])
            self.Atomic_weight.setText(' Атомная масса: ' + str(round(el_params['weight'], 2)))
            self.Electronegativity.setText(' Эл-отрицательность: ' + str(round(el_params['electronegativity'], 2)))
            self.Electronic_structure.setHtml('Электронная структура: ' + self.elem_structure(el_params))

    def printer(self):
        text = self.sender().text().split('. ')[1]
        self.temp_list = [text]
        el_params = elem_parameters(text)
        self.textBrowser.setPlainText(text)
        self.Name.setText(' Имя: ' + el_params['rusName'])
        self.Atomic_weight.setText(' Атомная масса: ' + str(round(el_params['weight'], 2)))
        self.Electronegativity.setText(' Эл-отрицательность: ' + str(round(el_params['electronegativity'], 2)))
        self.Electronic_structure.setHtml('Электронная структура: ' + self.elem_structure(el_params))

    def elem_structure(self, parameters):
        spdf = [('s', 2), ('p', 6), ('d', 10)]
        number = parameters['number']
        group = parameters['group']
        period = parameters['period']
        counter = 0
        res = str()
        if number in (24, 29, 41, 42, 44, 45, 47):
            last_layer = 1
        elif number == 46:
            last_layer = 0
        elif group in range(3, 13) or number == 2:
            last_layer = 2
        elif group in (1, 2):
            last_layer = group
        else:
            last_layer = group - 10
        left = number - last_layer
        for i in range(period - 1):
            while left > spdf[counter][1]:
                res += ''.join([str(i + 1), spdf[counter][0], up(spdf[counter][1])])
                left -= spdf[counter][1]
                if counter == 2 or counter == i:
                    counter = 0
                    break
                else:
                    counter += 1
        if left != 0:
            res += ''.join([str(period - 1), spdf[counter][0], up(left)])
        counter = 0
        while last_layer >= spdf[counter][1]:
            res += ''.join([str(period), spdf[counter][0], up(spdf[counter][1])])
            last_layer -= spdf[counter][1]
            counter += 1
        if last_layer != 0:
            res += ''.join([str(period), spdf[counter][0], up(last_layer)])
        return res

    def clearer(self):
        self.textBrowser.setPlainText(None)
        self.Name.setText(' Имя: ')
        self.Atomic_weight.setText(' Атомная масса: ')
        self.Electronegativity.setText(' Эл-отрицательность: ')
        self.Electronic_structure.setHtml('Электронная структура: ')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Elem_parameters()
    ex.show()
    sys.exit(app.exec_())