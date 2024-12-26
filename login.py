from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
from PyQt6.QtWidgets import QMessageBox
import subprocess
import json

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-image: url('food-delivery-service-design-vector.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 20, 311, 101))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(48)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ff4500;")
        self.label.setObjectName("label")
        
        self.login = QtWidgets.QPushButton(parent=self.centralwidget)
        self.login.setGeometry(QtCore.QRect(270, 360, 101, 41))
        self.login.setObjectName("login")
        self.login.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;  /* Green */
                color: white;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.login.clicked.connect(self.handle_login)
        
        self.signup = QtWidgets.QPushButton(parent=self.centralwidget)
        self.signup.setGeometry(QtCore.QRect(410, 360, 101, 41))
        self.signup.setObjectName("signup")
        self.signup.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;  /* Blue */
                color: white;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        self.signup.clicked.connect(self.handle_signup)
        
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 245, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: black; text-shadow: 1px 1px 2px black;")
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 290, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: black; text-shadow: 1px 1px 2px black;")
        self.label_3.setObjectName("label_3")
        
        self.username = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.username.setGeometry(QtCore.QRect(330, 240, 200, 31))
        self.username.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #4caf50;
            }
        """)
        self.username.setObjectName("username")
        
        self.password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.password.setGeometry(QtCore.QRect(330, 280, 200, 31))
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #2196f3;
            }
        """)
        self.password.setObjectName("password")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.MainWindow = MainWindow

    def handle_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self.MainWindow, "Error", "Please fill in all fields!")
            return
        
        try:
            conn = sqlite3.connect('project.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM user WHERE user_name = ? AND password = ?", 
                         (username, password))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # Valid credentials - launch user interface
                if user[4]=='customer':
                    self.MainWindow.close()
                    chary = []
                    chart = json.dumps(chary)
                    subprocess.run([sys.executable, 'user.py',user[0],chart])
                elif user[4]=='admin':
                    self.MainWindow.close()
                    subprocess.run([sys.executable, 'admin.py'])
                elif user[4]=='owner':
                    self.MainWindow.close()
                    subprocess.run([sys.executable, 'owner.py',user[0]])
                else:
                    self.MainWindow.close()
                    subprocess.run([sys.executable, 'dorder.py',user[0]])    
            else:
                # Invalid credentials
                QMessageBox.warning(self.MainWindow, "Error", 
                                  "Invalid username or password!")
                self.password.clear()
        
        except sqlite3.Error as e:
            QMessageBox.critical(self.MainWindow, "Database Error",
                               f"Database error occurred: {str(e)}")
    
    def handle_signup(self):
        # Launch signup interface
        self.MainWindow.close()
        subprocess.run([sys.executable, 'signup.py'])

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Foodify"))
        self.label.setText(_translate("MainWindow", "FOODIFY"))
        self.login.setText(_translate("MainWindow", "LOG IN"))
        self.signup.setText(_translate("MainWindow", "SIGN UP"))
        self.label_2.setText(_translate("MainWindow", "Username"))
        self.label_3.setText(_translate("MainWindow", "Password"))

def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run()