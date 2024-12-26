from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
from PyQt6.QtWidgets import QMessageBox
import subprocess
import json
userchart=[]
user_name=''
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-image: url('food-delivery-service-design-vector.jpg');
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }
        """)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 50, 400, 100))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(48)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.label.setStyleSheet("""
            QLabel {
                color: #FF6B6B;
                background-color: rgba(255, 255, 255, 0.85);
                border-radius: 20px;
                padding: 10px;
            }
        """)
        
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow.setOffset(5, 5)
        self.label.setGraphicsEffect(shadow)
        
        # Button styles with food-themed colors
        button_style = """
            QPushButton {
                font-family: 'Segoe UI';
                font-size: 16px;
                font-weight: bold;
                color: white;
                border-radius: 15px;
                padding: 12px;
                min-width: 140px;
                border: none;
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                transform: scale(1.05);
            }
        """
        
        self.search = QtWidgets.QPushButton(parent=self.centralwidget)
        self.search.setGeometry(QtCore.QRect(170, 380, 140, 55))
        self.search.setObjectName("search")
        self.search.setStyleSheet(button_style + """
            QPushButton {
                background-color: #FF6B6B;
            }
            QPushButton:hover {
                background-color: #FF8787;
            }
        """)
        self.search.clicked.connect(self.handle_search)

        self.orders = QtWidgets.QPushButton(parent=self.centralwidget)
        self.orders.setGeometry(QtCore.QRect(330, 380, 140, 55))
        self.orders.setObjectName("orders")
        self.orders.setStyleSheet(button_style + """
            QPushButton {
                background-color: #4ECDC4;
            }
            QPushButton:hover {
                background-color: #6EE7DE;
            }
        """)
        self.orders.clicked.connect(self.handle_order)

        self.chart = QtWidgets.QPushButton(parent=self.centralwidget)
        self.chart.setGeometry(QtCore.QRect(490, 380, 140, 55))
        self.chart.setObjectName("chart")
        self.chart.setStyleSheet(button_style + """
            QPushButton {
                background-color: #FFB900;
            }
            QPushButton:hover {
                background-color: #FFC830;
            }
        """)
        self.chart.clicked.connect(self.handle_chart)

        for button in [self.search, self.orders, self.chart]:
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            shadow = QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setColor(QtGui.QColor(0, 0, 0, 80))
            shadow.setOffset(3, 3)
            button.setGraphicsEffect(shadow)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menubar.setStyleSheet("""
            QMenuBar {
                background-color: rgba(255, 255, 255, 0.9);
                color: #2C3E50;
            }
        """)
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("""
            QStatusBar {
                background-color: rgba(255, 255, 255, 0.9);
                color: #2C3E50;
            }
        """)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.MainWindow = MainWindow

    def handle_order(self):
        self.MainWindow.close()
        subprocess.run([sys.executable, 'userorder.py',user_name,json.dumps(userchart)])
    def handle_search(self):
        self.MainWindow.close()
        subprocess.run([sys.executable, 'search.py', user_name, json.dumps(userchart)])

    def handle_chart(self):
        self.MainWindow.close()
        subprocess.run([sys.executable, 'chart.py',user_name,json.dumps(userchart)])    
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Welcome to Foodify"))
        self.label.setText(_translate("MainWindow", "WELCOME"))
        self.search.setText(_translate("MainWindow", "Search"))
        self.orders.setText(_translate("MainWindow", "Orders"))
        self.chart.setText(_translate("MainWindow", "Cart"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    user_name =sys.argv[1]
    userchart =json.loads(sys.argv[2])
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())