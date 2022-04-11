# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fenetre_main.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!

from Fenetre_RX_ui import Window_RX
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Window_main(object):
    def openRX(self):
    	self.RX_Dialog.show()

    def closeWindow(self):
    	Dialog.close()
    	self.RX_Dialog.close()

    def setupUi(self, Dialog):
        self.RX_Dialog = QtWidgets.QDialog()
        self.RX_ui = Window_RX()
        self.RX_ui.setupUi(self.RX_Dialog)
        Dialog.setObjectName("Dialog")
        Dialog.resize(389, 531)
        Dialog.setMinimumSize(QtCore.QSize(389, 531))
        Dialog.setMaximumSize(QtCore.QSize(389, 531))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 10, 91, 21))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(20, 10, 111, 23))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(160, 70, 61, 23))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(99, 220, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 130, 80, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 100, 61, 23))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 100, 61, 21))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(10, 190, 371, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 230, 61, 23))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 70, 80, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(230, 220, 111, 21))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(230, 240, 121, 21))
        self.checkBox_2.setObjectName("checkBox_2")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(100, 280, 121, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.checkBox_3 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 380, 331, 21))
        self.checkBox_3.setObjectName("checkBox_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(120, 420, 81, 21))
        self.label_3.setObjectName("label_3")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(20, 420, 91, 23))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 470, 91, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(150, 470, 51, 41))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.openRX)
        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(280, 470, 71, 41))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.closeWindow)
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 130, 61, 23))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setDisabled(self, True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Circuit teste"))
        self.comboBox.setItemText(0, _translate("Dialog", "ATMega128"))
        self.comboBox.setItemText(1, _translate("Dialog", "ATMega32"))
        self.lineEdit.setText(_translate("Dialog", "FF"))
        self.pushButton.setText(_translate("Dialog", "Initialiser la RAM"))
        self.pushButton_2.setText(_translate("Dialog", "Lire"))
        self.lineEdit_2.setText(_translate("Dialog", "3190"))
        self.label_2.setText(_translate("Dialog", "Adresse"))
        self.lineEdit_3.setText(_translate("Dialog", "FF"))
        self.pushButton_3.setText(_translate("Dialog", "Ecrire"))
        self.checkBox.setText(_translate("Dialog", "Incrementale"))
        self.checkBox_2.setText(_translate("Dialog", "Complemente"))
        self.pushButton_4.setText(_translate("Dialog", "Dumper la RAM"))
        self.checkBox_3.setText(_translate("Dialog", "Afficher le resultat de la relecture (EditPlus 2)"))
        self.label_3.setText(_translate("Dialog", "Baudrate"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "9600"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "19200"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "38400"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "1000000"))
        self.pushButton_5.setText(_translate("Dialog", "Test_RS232"))
        self.pushButton_6.setText(_translate("Dialog", "RX"))
        self.pushButton_7.setText(_translate("Dialog", "Exit"))



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	Dialog = QtWidgets.QDialog()
	ui = Window_main()
	ui.setupUi(Dialog)
	Dialog.show()
	sys.exit(app.exec_())
