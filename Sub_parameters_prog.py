import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui
from Substance import Substance


def under(stroke):
    return f'<sub>{str(stroke)}</sub>'


def up(stroke):
    return f' <sup>{str(stroke)}</sup>'


class Sub_parameters(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('Sub_parameters.ui', self)
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
            if but.text() not in ['+', 'С', '=>']:
                but.clicked.connect(self.printer)
        self.enterButton.clicked.connect(self.resulter)
        self.pushButton_59.clicked.connect(self.clearer)

        self.textBrowser.setHtml(None)
        self.Valence_Oxidation.setHtml('Valence: <br>Oxidation state:')
        self.label.hide()
        self.temp_list = list()

    def printer(self):
        if str(self.sender().text()).isnumeric():
            if not self.temp_list:
                text = self.sender().text()
            else:
                text = under(self.sender().text())
            self.temp_list.append(int(self.sender().text()))
        elif self.sender().text() == '(' or self.sender().text() == ')':
            text = self.sender().text()
            self.temp_list.append(text)
        else:
            text = self.sender().text().split(' ')[1]
            self.temp_list.append(text)
        self.htmler(text)

    def resulter(self):
        self.sub = Substance(self.temp_list)
        self.Valence_Oxidation.setHtml(f'Valence: {self.sub.get_valence}<br>Oxidation state: {self.sub.get_oxi}')

    def clearer(self):
        self.textBrowser.setPlainText(None)
        self.Valence_Oxidation.setPlainText(None)
        self.temp_list.clear()

    def htmler(self, text):
        self.html = self.textBrowser.toHtml().split('<')
        self.html[-4] += text
        self.textBrowser.setHtml('<'.join(self.html))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Sub_parameters()
    ex.show()
    sys.exit(app.exec_())