from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
from PyQt6.QtWidgets import QMessageBox
import subprocess

class Ui_signup(object):
    def setupUi(self, signup):
        signup.setObjectName("signup")
        signup.resize(800, 600)
        
        signup.setStyleSheet("""
            QMainWindow {
                background-image: url('food-delivery-service-design-vector.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)
        
        self.centralwidget = QtWidgets.QWidget(parent=signup)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 20, 311, 101))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(48)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ff4500;")
        self.label.setText("FOODIFY")
        
        labels_data = [
            ("Name", 230, 180),
            ("Address", 230, 225),
            ("Username", 230, 270),
            ("Password", 230, 315)
        ]
        
        for text, x, y in labels_data:
            label = QtWidgets.QLabel(text, parent=self.centralwidget)
            label.setGeometry(QtCore.QRect(x, y, 81, 21))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            label.setFont(font)
            label.setStyleSheet("color: black; text-shadow: 1px 1px 2px black;")
        
        self.name = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.address = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.username = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.password = QtWidgets.QLineEdit(parent=self.centralwidget)
        
        input_fields = [
            (self.name, 175),
            (self.address, 220),
            (self.username, 265),
            (self.password, 310)
        ]
        
        input_style = """
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
        """
        
        for field, y in input_fields:
            field.setGeometry(QtCore.QRect(330, y, 200, 31))
            field.setStyleSheet(input_style)
            
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signup_2 = QtWidgets.QPushButton("SIGN UP", parent=self.centralwidget)
        self.signup_2.setGeometry(QtCore.QRect(270, 380, 101, 41))
        self.signup_2.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        # Connect signup button to handler
        self.signup_2.clicked.connect(self.handle_signup)
        
        self.back = QtWidgets.QPushButton("BACK", parent=self.centralwidget)
        self.back.setGeometry(QtCore.QRect(410, 380, 101, 41))
        self.back.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        # Connect back button to handler
        self.back.clicked.connect(self.handle_back)
        
        signup.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=signup)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        signup.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(parent=signup)
        signup.setStatusBar(self.statusbar)
        
        self.retranslateUi(signup)
        QtCore.QMetaObject.connectSlotsByName(signup)
        
        # Store signup window reference
        self.signup_window = signup

    def handle_signup(self):
        # Get values from input fields
        name = self.name.text().strip()
        address = self.address.text().strip()
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        # Check if any field is empty
        if not all([name, address, username, password]):
            QMessageBox.warning(self.signup_window, "Error", 
                              "Please fill in all fields!")
            return
        
        try:
            # Connect to database
            conn = sqlite3.connect('project.db')
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute("SELECT * FROM user WHERE user_name = ?", (username,))
            if cursor.fetchone():
                QMessageBox.warning(self.signup_window, "Error", 
                                  "Username already exists! Please choose another username.")
                self.username.clear()
                return
            
            # Insert new user
            cursor.execute("""
                INSERT INTO user (user_name, password, name, address, kind)
                VALUES (?, ?, ?, ?, 'customer')
            """, (username, password, name, address))
            
            conn.commit()
            conn.close()
            
            # Show success message
            QMessageBox.information(self.signup_window, "Success", 
                                  "Sign up successful! Please log in.")
            
            # Return to login interface
            self.signup_window.close()
            subprocess.run([sys.executable, 'login.py'])
            
        except sqlite3.Error as e:
            QMessageBox.critical(self.signup_window, "Database Error",
                               f"An error occurred: {str(e)}")
            conn.close()
    
    def handle_back(self):
        # Return to login interface
        self.signup_window.close()
        subprocess.run([sys.executable, 'login.py'])

    def retranslateUi(self, signup):
        signup.setWindowTitle("Foodify - Sign Up")

def run():
    app = QtWidgets.QApplication(sys.argv)
    signup = QtWidgets.QMainWindow()
    ui = Ui_signup()
    ui.setupUi(signup)
    signup.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()