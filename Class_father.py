from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtGui
from Theory import under


class Class_father(QMainWindow):
    def initUI(self):
        try:
            self.buttons = self.findChildren(QPushButton)
            for but in self.buttons:
                if but.text() not in ['+', 'С', '=>']:
                    but.clicked.connect(self.printer)
            self.clearer()
            self.create_menu()
            self.label.hide()
            self.pushButton_59.clicked.connect(self.clearer)
            self.enterButton.clicked.connect(self.resulter)
            self.plusButton.clicked.connect(self.pluser)
        except AttributeError:
            pass

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

    def htmler(self, text):
        self.html = self.textBrowser.toHtml().split('<')
        self.html[-4] += text
        self.textBrowser.setHtml('<'.join(self.html))

    def create_menu(self):
        self.menubar.clear()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 25))
        self.menubar.setObjectName("menubar")
        self.menuBack = QtWidgets.QMenu(self.menubar)
        self.menuBack.setObjectName("menuBack")
        self.menuImportto = QtWidgets.QMenu(self.menubar)
        self.menuImportto.setObjectName("menuImportto")
        Class_father.setMenuBar(self, self.menubar)
        self.actionCalculation_of_chemical_reactions = QtWidgets.QAction()
        self.actionCalculation_of_chemical_reactions.setObjectName("actionCalculation_of_chemical_reactions")
        self.actionGetting_substance_name = QtWidgets.QAction()
        self.actionGetting_substance_name.setObjectName("actionGetting_substance_name")
        self.actionCalculation_of_substance_parameters = QtWidgets.QAction()
        self.actionCalculation_of_substance_parameters.setObjectName("actionCalculation_of_substance_parameters")
        self.actionCalculation_of_element_parameters = QtWidgets.QAction()
        self.actionCalculation_of_element_parameters.setObjectName("actionCalculation_of_element_parameters")
        self.actionFront_page = QtWidgets.QAction()
        self.actionFront_page.setObjectName("actionFront_page")
        self.actionCalculation_of_chemical_reactions_2 = QtWidgets.QAction()
        self.actionCalculation_of_chemical_reactions_2.setObjectName("actionCalculation_of_chemical_reactions_2")
        self.actionGetting_substance_name_2 = QtWidgets.QAction()
        self.actionGetting_substance_name_2.setObjectName("actionGetting_substance_name_2")
        self.actionCalculation_of_substance_parameters_2 = QtWidgets.QAction()
        self.actionCalculation_of_substance_parameters_2.setObjectName("actionCalculation_of_substance_parameters_2")
        self.actionCalculation_of_element_parameters_2 = QtWidgets.QAction()
        self.actionCalculation_of_element_parameters_2.setObjectName("actionCalculation_of_element_parameters_2")
        self.menuBack.addAction(self.actionFront_page)
        self.menuBack.addSeparator()
        self.menuBack.addAction(self.actionCalculation_of_chemical_reactions_2)
        self.menuBack.addAction(self.actionGetting_substance_name_2)
        self.menuBack.addAction(self.actionCalculation_of_substance_parameters_2)
        self.menuBack.addAction(self.actionCalculation_of_element_parameters_2)
        self.menuImportto.addAction(self.actionCalculation_of_chemical_reactions)
        self.menuImportto.addAction(self.actionGetting_substance_name)
        self.menuImportto.addAction(self.actionCalculation_of_substance_parameters)
        self.menuImportto.addAction(self.actionCalculation_of_element_parameters)
        self.menubar.addAction(self.menuBack.menuAction())
        self.menubar.addAction(self.menuImportto.menuAction())

        self.menuBack.setTitle("Перейти в...")
        self.menuImportto.setTitle("Импортировать в...")
        self.actionCalculation_of_chemical_reactions.setText("Расчёт химических реакций")
        self.actionGetting_substance_name.setText("Получение названия вещества")
        self.actionCalculation_of_substance_parameters.setText("Расчёт параметров вещества")
        self.actionCalculation_of_element_parameters.setText("Расчёт параметров элемента")
        self.actionFront_page.setText("Главная страница")
        self.actionCalculation_of_chemical_reactions_2.setText("Расчёт химических реакций")
        self.actionGetting_substance_name_2.setText("Получение названия вещества")
        self.actionCalculation_of_substance_parameters_2.setText("Расчёт параметров вещества")
        self.actionCalculation_of_element_parameters_2.setText("Расчёт параметров элемента")

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

    def backer(self):
        self.parenter.show()
        self.hide()

    def just_open(self):
        if self.sender().text() == 'Расчёт химических реакций':
            self.parenter.open_Chem_calc()
        elif self.sender().text() == 'Получение названия вещества':
            self.parenter.open_Sub_name()
        elif self.sender().text() == 'Расчёт параметров вещества':
            self.parenter.open_Sub_parameters()
        elif self.sender().text() == 'Расчёт параметров элемента':
            self.parenter.open_Elem_parameters()
        self.hide()

    def arg_open(self):
        if self.sender().text() == 'Расчёт химических реакций':
            self.parenter.open_Chem_calc(self.temp_list)
        elif self.sender().text() == 'Получение названия вещества':
            self.parenter.open_Sub_name(self.temp_list)
        elif self.sender().text() == 'Расчёт параметров вещества':
            self.parenter.open_Sub_parameters(self.temp_list)
        elif self.sender().text() == 'Расчёт параметров элемента':
            self.parenter.open_Elem_parameters(self.temp_list)
        self.hide()
