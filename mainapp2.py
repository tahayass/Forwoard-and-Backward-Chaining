# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from module import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(691, 653)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.staticImg = QtWidgets.QLabel(self.centralwidget)
        self.staticImg.setGeometry(QtCore.QRect(0, 0, 321, 631))
        self.staticImg.setText("")
        self.staticImg.setPixmap(QtGui.QPixmap("img2.png"))
        self.staticImg.setObjectName("staticImg")
        self.label_bf = QtWidgets.QLabel(self.centralwidget)
        self.label_bf.setGeometry(QtCore.QRect(340, 50, 181, 16))
        self.label_bf.setObjectName("label_bf")
        self.bf_input = QtWidgets.QLineEdit(self.centralwidget)
        self.bf_input.setGeometry(QtCore.QRect(340, 80, 261, 22))
        self.bf_input.setObjectName("bf_input")
        self.label_br = QtWidgets.QLabel(self.centralwidget)
        self.label_br.setGeometry(QtCore.QRect(340, 110, 201, 16))
        self.label_br.setObjectName("label_br")
        self.br_input = QtWidgets.QLineEdit(self.centralwidget)
        self.br_input.setGeometry(QtCore.QRect(340, 140, 261, 22))
        self.br_input.setObjectName("br_input")
        self.conf_res = QtWidgets.QGroupBox(self.centralwidget)
        self.conf_res.setGeometry(QtCore.QRect(330, 190, 281, 111))
        self.conf_res.setObjectName("conf_res")
        self.first_rule_button = QtWidgets.QRadioButton(self.conf_res)
        self.first_rule_button.setGeometry(QtCore.QRect(50, 20, 95, 20))
        self.first_rule_button.setObjectName("first_rule_button")
        self.last_rule_button = QtWidgets.QRadioButton(self.conf_res)
        self.last_rule_button.setGeometry(QtCore.QRect(50, 50, 95, 20))
        self.last_rule_button.setObjectName("last_rule_button")
        self.random_button = QtWidgets.QRadioButton(self.conf_res)
        self.random_button.setGeometry(QtCore.QRect(50, 80, 95, 20))
        self.random_button.setObjectName("random_button")
        self.label_goal = QtWidgets.QLabel(self.centralwidget)
        self.label_goal.setGeometry(QtCore.QRect(340, 310, 191, 21))
        self.label_goal.setObjectName("label_goal")
        self.goal_input = QtWidgets.QLineEdit(self.centralwidget)
        self.goal_input.setGeometry(QtCore.QRect(340, 340, 261, 21))
        self.goal_input.setObjectName("goal_input")
        self.log_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.log_checkbox.setGeometry(QtCore.QRect(340, 380, 241, 20))
        self.log_checkbox.setObjectName("log_checkbox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 520, 281, 91))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.checked) #when pushed function check runs
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(330, 410, 291, 91))
        self.groupBox.setObjectName("groupBox")
        self.CAvant_button = QtWidgets.QRadioButton(self.groupBox)
        self.CAvant_button.setGeometry(QtCore.QRect(30, 30, 201, 20))
        self.CAvant_button.setObjectName("CAvant_button")
        self.CArriere_button = QtWidgets.QRadioButton(self.groupBox)
        self.CArriere_button.setEnabled(True)
        self.CArriere_button.setGeometry(QtCore.QRect(30, 60, 151, 20))
        self.CArriere_button.setObjectName("CArriere_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_bf.setText(_translate("MainWindow", "Chemin de la base des faits :"))
        self.label_br.setText(_translate("MainWindow", "Chemin de la base des règles :"))
        self.conf_res.setTitle(_translate("MainWindow", "choix de la résolution des conflits :"))
        self.first_rule_button.setText(_translate("MainWindow", "First rule"))
        self.last_rule_button.setText(_translate("MainWindow", "last rule"))
        self.random_button.setText(_translate("MainWindow", "random"))
        self.label_goal.setText(_translate("MainWindow", "But:"))
        self.log_checkbox.setText(_translate("MainWindow", "écrire dans un fichier log"))
        self.pushButton.setText(_translate("MainWindow", "Démarrer l\'algorithme"))
        self.groupBox.setTitle(_translate("MainWindow", "type d\'algorithme"))
        self.CAvant_button.setText(_translate("MainWindow", "chainage avant"))
        self.CArriere_button.setText(_translate("MainWindow", "chainage arrière"))

    def checked(self):      #### function to run when pushing the button
        if self.log_checkbox.isChecked() == True : 
            log_check=True
        else:
            log_check=False
        
        path1=self.br_input.text()
        path_BR=abs_path(path1)
        BR=extract_BR(path_BR)
        i=0
        print('La base des règles : ')
        for i in range(len(BR)):
            print(BR[i].premisses,' ---> ',BR[i].conclusion,';    ruleID = ',BR[i].ruleID)
        path2=self.bf_input.text()
        path_BF=abs_path(path2)
        BF=extract_BF(path_BF)
        temp=[]
        for j in range(len(BF)):
            temp.append(BF[j].fait)
        print('La base des faits')
        print(temp)                #temporary list for fait without flags
        goal=self.goal_input.text()
        if self.first_rule_button.isChecked() :
            confRes=''
        if self.last_rule_button.isChecked() :
            confRes='Reverse'
        if self.random_button.isChecked() :
            confRes='Random'
        if self.CAvant_button.isChecked():
            chainage_avant(BR,BF,temp,goal,confRes,log_check)
        if self.CArriere_button.isChecked():
            chainage_arriere(BR,temp,goal,confRes,log_check)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
