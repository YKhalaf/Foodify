from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Restaurant Search")
        
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

        self.search = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.search.setGeometry(QtCore.QRect(180, 60, 441, 371))
        self.search.setStyleSheet("""
            QTableWidget {
                background-color: rgba(255, 255, 255, 0.92);
                border-radius: 15px;
                border: 2px solid #3498db;
                gridline-color: #BDC3C7;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #BDC3C7;
            }
            QHeaderView::section {
                background-color: #2980b9;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        # Set up table columns
        self.search.setColumnCount(5)
        self.search.setHorizontalHeaderLabels(["Restaurant","Rating", "Meal", "Meal ID", "Price"])
        header = self.search.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Input field style
        input_style = """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 5px 10px;
                font-size: 14px;
                color: #2C3E50;
                height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #e74c3c;
                background-color: white;
            }
        """

        # Input fields setup
        self.restaurnat = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.restaurnat.setGeometry(QtCore.QRect(360, 450, 160, 30))
        self.restaurnat.setStyleSheet(input_style)
        self.restaurnat.setPlaceholderText("Enter restaurant name...")

        self.meal = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.meal.setGeometry(QtCore.QRect(360, 490, 160, 30))
        self.meal.setStyleSheet(input_style)
        self.meal.setPlaceholderText("Enter meal name...")

        self.achart = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.achart.setGeometry(QtCore.QRect(360, 530, 160, 30))
        self.achart.setStyleSheet(input_style)
        self.achart.setPlaceholderText("Enter quantity...")

        # Button style
        button_style = """
            QPushButton {
                background-color: %s;
                color: white;
                border-radius: 12px;
                font-size: 13px;
                font-weight: bold;
                border: none;
                padding: 8px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: %s;
            }
            QPushButton:pressed {
                background-color: %s;
            }
        """

        # Buttons setup
        self.back = QtWidgets.QPushButton(parent=self.centralwidget)
        self.back.setGeometry(QtCore.QRect(10, 10, 75, 30))
        self.back.setStyleSheet(button_style % ('#34495e', '#2c3e50', '#2c3e50'))

        self.srestaurnat = QtWidgets.QPushButton(parent=self.centralwidget)
        self.srestaurnat.setGeometry(QtCore.QRect(250, 450, 100, 30))
        self.srestaurnat.setStyleSheet(button_style % ('#2980b9', '#3498db', '#2475a8'))

        self.smeal = QtWidgets.QPushButton(parent=self.centralwidget)
        self.smeal.setGeometry(QtCore.QRect(250, 490, 100, 30))
        self.smeal.setStyleSheet(button_style % ('#27ae60', '#2ecc71', '#219a52'))

        self.adchart = QtWidgets.QPushButton(parent=self.centralwidget)
        self.adchart.setGeometry(QtCore.QRect(250, 530, 100, 30))
        self.adchart.setStyleSheet(button_style % ('#e67e22', '#f39c12', '#d35400'))

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
        self.back.setText(_translate("MainWindow", "Back"))
        self.srestaurnat.setText(_translate("MainWindow", "Restaurant"))
        self.smeal.setText(_translate("MainWindow", "Meal"))
        self.adchart.setText(_translate("MainWindow", "Add to chart"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())