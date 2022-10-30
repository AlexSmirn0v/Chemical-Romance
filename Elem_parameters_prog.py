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
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('Elem_parameters.ui', self)
        self.setWindowIcon(QtGui.QIcon('Chemical Romance round logo.svg'))
        #self.recolour()
        self.initUI()

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

    def printer(self):
        text = self.sender().text().split('. ')[1]
        el_params = elem_parameters(text)
        self.textBrowser.setPlainText(text)
        self.Name.setText(' Name: ' + el_params[2])
        self.Atomic_weight.setText(' Atomic weight: ' + str(round(el_params[3], 2)))
        self.Electronegativity.setText(' Electronegativity: ' + str(round(el_params[4], 2)))
        self.htmler(self.el_structure(el_params))

    def el_structure(self, parameters):
        spdf = [('s', 2), ('p', 6), ('d', 10), ('f', 14), ('f', 14)]
        number = parameters[0]
        period = parameters[-1]
        full = 0
        res = ''
        for i in range(period):
            full += sum(map(lambda x: x[1], spdf[:i+1]))
            res += ''.join(map(lambda x: str(i + 1) + x[0] + up(x[1]), spdf[:i+1])) + ' '
            print(res)
        left = 2 * period ** 2 - number
        turner = 0
        while left >= spdf[turner][1]:
            res += spdf[turner][0] + up(spdf[turner][1])
            left -= spdf[turner][1]
            if turner != 3:
                turner += 1
            else:
                turner = 0
        return res

    def clearer(self):
        self.textBrowser.setPlainText(None)
        self.Name.setText(' Name: ')
        self.Atomic_weight.setText(' Atomic weight: ')
        self.Electronegativity.setText(' Electronegativity: ')
        self.Electronic_structure.setHtml('Electronic structure: ')

    def htmler(self, text):
        self.Electronic_structure.setPlainText('')
        self.Electronic_structure.setHtml('Electronic structure: ' + text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Elem_parameters()
    ex.show()
    sys.exit(app.exec_())