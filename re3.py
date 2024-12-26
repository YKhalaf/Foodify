from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Restaurant Menu Chart")
        
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

        # Chart Label
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 30, 300, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(26)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(44, 62, 80, 0.8);
                border-radius: 15px;
                padding: 5px;
            }
        """)

        # Menu Chart Table
        self.chart = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.chart.setGeometry(QtCore.QRect(220, 110, 351, 281))
        self.chart.setStyleSheet("""
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
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
        """)
        
        # Set up table columns
        self.chart.setColumnCount(4)
        self.chart.setHorizontalHeaderLabels(["Item Number", "Meal Name", "Meal ID","Price"])
        header = self.chart.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Input field styling
        self.id = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.id.setGeometry(QtCore.QRect(390, 430, 113, 30))
        self.id.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px 10px;
                font-size: 14px;
                color: #2C3E50;
            }
            QLineEdit:focus {
                border: 2px solid #e74c3c;
                background-color: white;
            }
        """)
        self.id.setPlaceholderText("Enter ID...")

        # Button styling
        button_style = """
            QPushButton {
                background-color: %s;
                color: white;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: %s;
            }
            QPushButton:pressed {
                background-color: %s;
            }
        """

        # Back button
        self.back = QtWidgets.QPushButton(parent=self.centralwidget)
        self.back.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.back.setStyleSheet(button_style % ('#34495e', '#2c3e50', '#2c3e50'))

        # Delete button
        self.delete_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.delete_2.setGeometry(QtCore.QRect(280, 430, 75, 30))
        self.delete_2.setStyleSheet(button_style % ('#e74c3c', '#c0392b', '#c0392b'))

        # Order button
        self.order = QtWidgets.QPushButton(parent=self.centralwidget)
        self.order.setGeometry(QtCore.QRect(340, 490, 101, 41))
        self.order.setStyleSheet(button_style % ('#27ae60', '#2ecc71', '#27ae60'))

        # Menu and Status bar
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
        self.label.setText(_translate("MainWindow", "Menu Chart"))
        self.delete_2.setText(_translate("MainWindow", "Delete"))
        self.order.setText(_translate("MainWindow", "Order"))
        self.back.setText(_translate("MainWindow", "Back"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())