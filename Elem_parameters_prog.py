import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui
from Theory import elem_parameters


def under(stroke):
    return f'<sub>{str(stroke)}</sub>'


def up(stroke):
    return f'<sup>{str(stroke)}</sup>'


class Elem_parameters(QMainWindow):
    def __init__(self, parent=None, *args):
        super().__init__()
        uic.loadUi('Elem_parameters.ui', self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        #self.recolour()
        self.parenter = parent
        print(self.parenter)
        self.initUI()
        self.connect_menu()

    def recolour(self):
        palette = QtGui.QPalette()
        for Q in [QtGui.QPalette.Active, QtGui.QPalette.Inactive, QtGui.QPalette.Disabled]:
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.WindowText, brush)

            brush = QtGui.QBrush(QtGui.QColor('#3c3f41'))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Button, brush)

            brush = QtGui.QBrush(QtGui.QColor(84, 88, 91))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Light, brush)

            brush = QtGui.QBrush(QtGui.QColor(66, 69, 72))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Midlight, brush)

            brush = QtGui.QBrush(QtGui.QColor(49, 51, 53))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Dark, brush)

            brush = QtGui.QBrush(QtGui.QColor(70, 73, 76))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Mid, brush)

            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Text, brush)

            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.ButtonText, brush)

            brush = QtGui.QBrush(QtGui.QColor(43, 43, 43))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Base, brush)

            brush = QtGui.QBrush(QtGui.QColor(43, 43, 43))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Window, brush)

            brush = QtGui.QBrush(QtGui.QColor(29, 29, 29))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Shadow, brush)

            brush = QtGui.QBrush(QtGui.QColor(198, 135, 24))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Highlight, brush)

            brush = QtGui.QBrush(QtGui.QColor(255, 162, 47))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.Link, brush)

            brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.AlternateBase, brush)

            brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.NoRole, brush)

            brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.ToolTipBase, brush)

            brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(Q, QtGui.QPalette.ToolTipText, brush)
        self.setPalette(palette)

    def initUI(self):
        self.buttons = self.findChildren(QPushButton)
        for but in self.buttons:
            if but.text() != 'С':
                but.clicked.connect(self.printer)
        self.pushButton_59.clicked.connect(self.clearer)

        self.textBrowser.setHtml(None)
        self.Name.setText(' Name: ')
        self.Electronegativity.setText(' Electronegativity:    ')

    def connect_menu(self):
        self.actionFront_page.triggered.connect(self.backer)
        self.openers = [self.actionCalculation_of_chemical_reactions_2,
                        self.actionGetting_substance_name_2,
                        self.actionCalculation_of_substance_parameters_2,
                        self.actionCalculation_of_element_parameters_2]
        for elem in self.openers:
            elem.triggered.connect(self.just_open)

        self.arg_openers = [self.actionCalculation_of_chemical_reactions,
                        self.actionGetting_substance_name,
                        self.actionCalculation_of_substance_parameters,
                        self.actionCalculation_of_element_parameters]
        for elem in self.arg_openers:
            elem.triggered.connect(self.arg_open)

    def printer(self):
        text = self.sender().text().split('. ')[1]
        el_params = elem_parameters(text)
        self.textBrowser.setPlainText(text)
        self.Name.setText(' Name: ' + el_params[2])
        self.Atomic_weight.setText(' Atomic mass: ' + str(round(el_params[3], 2)))
        self.Electronegativity.setText(' Electronegativity: ' + str(round(el_params[4], 2)))
        self.htmler(self.elem_structure(el_params))

    def elem_structure(self, parameters):
        spdf = [('s', 2), ('p', 6), ('d', 10)]
        number = parameters[0]
        group = parameters[-2]
        period = parameters[-1]
        counter = 0
        res = str()
        if number in (24, 29, 47) or number in range(41, 46):
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
                res += ''.join(str(i + 1) + spdf[counter][0] + up(spdf[counter][1]))
                left -= spdf[counter][1]
                if counter == 2 or counter == i:
                    counter = 0
                    break
                else:
                    counter += 1
        if left != 0:
            res += ''.join(str(period - 1) + spdf[counter][0] + up(left))
        counter = 0
        while last_layer >= spdf[counter][1]:
            res += ''.join(str(period) + spdf[counter][0] + up(spdf[counter][1]))
            last_layer -= spdf[counter][1]
            counter += 1
        if last_layer != 0:
            res += ''.join(str(period) + spdf[counter][0] + up(last_layer))
        return res

    def clearer(self):
        self.textBrowser.setPlainText(None)
        self.Name.setText(' Name: ')
        self.Atomic_weight.setText(' Atomic mass: ')
        self.Electronegativity.setText(' Electronegativity: ')
        self.Electronic_structure.setHtml('Electronic structure: ')

    def htmler(self, text):
        self.Electronic_structure.setPlainText('')
        self.Electronic_structure.setHtml('Electronic structure: ' + text)

    def backer(self):
        self.parenter.show()
        self.hide()

    def just_open(self):
        if self.sender().text() == 'Calculation of chemical reactions':
            self.parenter.open_Chem_calc()
        elif self.sender().text() == 'Getting substance name':
            self.parenter.open_Sub_name()
        elif self.sender().text() == 'Calculation of substance parameters':
            self.parenter.open_Sub_parameters()
        elif self.sender().text() == 'Calculation of element parameters':
            self.parenter.open_Elem_parameters()
        self.hide()

    def arg_open(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Elem_parameters()
    ex.show()
    sys.exit(app.exec_())