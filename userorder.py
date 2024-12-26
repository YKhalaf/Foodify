from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
from datetime import datetime
import subprocess
import json

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Store MainWindow reference
        self.MainWindow = MainWindow  # Add this line at the start of setupUi
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Order Management System")
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-image: url('food-delivery-service-design-vector.jpg');
                background-position: center;
                background-repeat: no-repeat;
                background-color: #2C3E50;
            }
        """)

        # Add Back Button
        self.back_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(20, 20, 100, 40))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:pressed {
                background-color: #A93226;
            }
        """)
        self.back_button.setText("Back")
        self.back_button.clicked.connect(self.go_back)

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 20, 400, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(36)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(44, 62, 80, 0.8);
                border-radius: 20px;
                padding: 10px;
            }
        """)
        
        table_style = """
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                border: 2px solid #3498db;
                gridline-color: #BDC3C7;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #BDC3C7;
            }
            QHeaderView::section {
                background-color: #2980b9;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """
        
        self.pastorder = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.pastorder.setGeometry(QtCore.QRect(40, 110, 311, 281))
        self.pastorder.setStyleSheet(table_style)
        self.pastorder.setColumnCount(4)
        self.pastorder.setHorizontalHeaderLabels([
            "Order #", "Date", "Price", "Status"
        ])
        header = self.pastorder.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        
        self.currentorder = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.currentorder.setGeometry(QtCore.QRect(420, 110, 321, 281))
        self.currentorder.setStyleSheet(table_style)
        self.currentorder.setColumnCount(4)
        self.currentorder.setHorizontalHeaderLabels([
            "Order #", "Date", "Price", "Status"
        ])
        header = self.currentorder.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        
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
        
        # Load data from database
        self.load_order_data()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "WELCOME"))

    def go_back(self):
        import sys
        self.MainWindow.close()
        subprocess.run([sys.executable, 'user.py', sys.argv[1], sys.argv[2]])

    def load_order_data(self):
        try:
            conn = sqlite3.connect('project.db')
            cursor = conn.cursor()
            
            # Query for delivered orders
            delivered_query = """
                SELECT order_num, order_date, price, status 
                FROM orders 
                WHERE status = 'deliveried' and order_owner = ?
            """
            cursor.execute(delivered_query, (sys.argv[1],))  # Fixed parameter binding
            delivered_orders = cursor.fetchall()
            
            # Query for non-delivered orders
            current_query = """
                SELECT order_num, order_date, price, status 
                FROM orders 
                WHERE status <> 'deliveried' and order_owner = ?
            """
            cursor.execute(current_query, (sys.argv[1],))  # Fixed parameter binding
            current_orders = cursor.fetchall()
            
            # Populate past orders table
            self.pastorder.setRowCount(len(delivered_orders))
            for row, order in enumerate(delivered_orders):
                for col, value in enumerate(order):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.pastorder.setItem(row, col, item)
            
            # Populate current orders table
            self.currentorder.setRowCount(len(current_orders))
            for row, order in enumerate(current_orders):
                for col, value in enumerate(order):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.currentorder.setItem(row, col, item)
            
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.statusbar.showMessage(f"Error loading orders: {e}", 5000)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())