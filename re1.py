from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        # Set background image 
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-image: url('food-delivery-service-design-vector.jpg');
                background-position: center;
                background-repeat: no-repeat;
                background-color: #2C3E50;  /* Fallback color */
            }
        """)
        
        # Welcome Label with enhanced styling
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 30, 400, 101))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(42)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: #ECF0F1;
                background-color: rgba(44, 62, 80, 0.7);
                border-radius: 20px;
                padding: 10px;
            }
        """)
        
        # Styled input fields
        input_style = """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid #3498DB;
                border-radius: 10px;
                padding: 5px 10px;
                font-size: 14px;
                color: #2C3E50;
                height: 25px;
            }
            QLineEdit:focus {
                border: 2px solid #E74C3C;
                background-color: white;
            }
        """
        
        # Input field setup with consistent styling
        self.meal_id = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.meal_id.setGeometry(QtCore.QRect(180, 330, 113, 35))
        self.meal_id.setStyleSheet(input_style)
        
        self.price = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.price.setGeometry(QtCore.QRect(320, 330, 113, 35))
        self.price.setStyleSheet(input_style)
        
        self.mealname = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.mealname.setGeometry(QtCore.QRect(470, 330, 113, 35))
        self.mealname.setStyleSheet(input_style)
        
        # Label styling
        label_style = """
            QLabel {
                color: white;
                background-color: rgba(44, 62, 80, 0.7);
                border-radius: 10px;
                padding: 5px 15px;
            }
        """
        
        # Labels setup
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 290, 71, 26))
        self.label_2.setFont(QtGui.QFont("Segoe UI", 12))
        self.label_2.setStyleSheet(label_style)
        
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(350, 290, 59, 26))
        self.label_3.setFont(QtGui.QFont("Segoe UI", 12))
        self.label_3.setStyleSheet(label_style)
        
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(480, 290, 101, 26))
        self.label_4.setFont(QtGui.QFont("Segoe UI", 12))
        self.label_4.setStyleSheet(label_style)
        
        # Button styling
        button_style = """
            QPushButton {
                background-color: %s;
                color: white;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: %s;
            }
            QPushButton:pressed {
                background-color: %s;
            }
        """
        
        # Buttons setup with different colors
        self.update = QtWidgets.QPushButton(parent=self.centralwidget)
        self.update.setGeometry(QtCore.QRect(170, 410, 111, 61))
        self.update.setStyleSheet(button_style % ('#2980B9', '#3498DB', '#216A9E'))
        
        self.add = QtWidgets.QPushButton(parent=self.centralwidget)
        self.add.setGeometry(QtCore.QRect(330, 410, 111, 61))
        self.add.setStyleSheet(button_style % ('#27AE60', '#2ECC71', '#219A52'))
        
        self.delete_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.delete_2.setGeometry(QtCore.QRect(474, 410, 111, 61))
        self.delete_2.setStyleSheet(button_style % ('#C0392B', '#E74C3C', '#962D22'))
        
        # Menu and status bar styling
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2C3E50;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #34495E;
            }
        """)
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setStyleSheet("color: white; background-color: #2C3E50;")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Restaurant Menu Manager"))
        self.label.setText(_translate("MainWindow", "WELCOME"))
        self.delete_2.setText(_translate("MainWindow", "Delete"))
        self.add.setText(_translate("MainWindow", "ADD"))
        self.update.setText(_translate("MainWindow", "Update"))
        self.label_2.setText(_translate("MainWindow", "Meal ID"))
        self.label_3.setText(_translate("MainWindow", "Price"))
        self.label_4.setText(_translate("MainWindow", "Meal Name"))
        
        # Set placeholders for input fields
        self.meal_id.setPlaceholderText("Enter ID...")
        self.price.setPlaceholderText("Enter price...")
        self.mealname.setPlaceholderText("Enter name...")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())