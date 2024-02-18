# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MenuWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MenuWindow(object):
    def setupUi(self, MenuWindow):
        MenuWindow.setObjectName("MenuWindow")
        MenuWindow.resize(506, 473)
        self.centralwidget = QtWidgets.QWidget(MenuWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 442, 401))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.MainMenuContainer = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.MainMenuContainer.setContentsMargins(0, 0, 0, 0)
        self.MainMenuContainer.setObjectName("MainMenuContainer")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.MainMenuContainer.addItem(spacerItem)
        self.labelTitle = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitle.setFont(font)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setObjectName("labelTitle")
        self.MainMenuContainer.addWidget(self.labelTitle)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.MainMenuContainer.addItem(spacerItem1)
        self.labelSubtitle = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(10)
        self.labelSubtitle.setFont(font)
        self.labelSubtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSubtitle.setObjectName("labelSubtitle")
        self.MainMenuContainer.addWidget(self.labelSubtitle)
        spacerItem2 = QtWidgets.QSpacerItem(20, 22, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.MainMenuContainer.addItem(spacerItem2)
        self.buttonStart = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonStart.setObjectName("buttonStart")
        self.MainMenuContainer.addWidget(self.buttonStart)
        self.buttonEdit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonEdit.setObjectName("buttonEdit")
        self.MainMenuContainer.addWidget(self.buttonEdit)
        MenuWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MenuWindow)
        QtCore.QMetaObject.connectSlotsByName(MenuWindow)

    def retranslateUi(self, MenuWindow):
        _translate = QtCore.QCoreApplication.translate
        MenuWindow.setWindowTitle(_translate("MenuWindow", "MainWindow"))
        self.labelTitle.setText(_translate("MenuWindow", "Welcome to the Warhammer: 40,000 simulation!"))
        self.labelSubtitle.setText(_translate("MenuWindow", "Please select one of the options below."))
        self.buttonStart.setText(_translate("MenuWindow", "Begin Game"))
        self.buttonEdit.setText(_translate("MenuWindow", "Edit Armies"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MenuWindow = QtWidgets.QMainWindow()
    ui = Ui_MenuWindow()
    ui.setupUi(MenuWindow)
    MenuWindow.show()
    sys.exit(app.exec_())

