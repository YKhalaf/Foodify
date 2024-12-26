from PyQt6 import QtCore, QtGui, QtWidgets
from datetime import datetime
import sqlite3

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Order Management System")
        
        # Set up central widget with background
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
        self.pastorder.setColumnCount(5)
        self.pastorder.setHorizontalHeaderLabels([
            "Order #", "Date", "Address", "Price", "User"
        ])
        header = self.pastorder.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        
        self.currentorder = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.currentorder.setGeometry(QtCore.QRect(420, 110, 321, 281))
        self.currentorder.setStyleSheet(table_style)
        self.currentorder.setColumnCount(5)
        self.currentorder.setHorizontalHeaderLabels([
            "Order #", "Date", "Address", "Price", "User"
        ])
        header = self.currentorder.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        
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
        
        # Create order button
        self.order = QtWidgets.QPushButton(parent=self.centralwidget)
        self.order.setGeometry(QtCore.QRect(120, 420, 141, 51))
        self.order.setStyleSheet(button_style % ('#27AE60', '#2ECC71', '#219A52'))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.order.setFont(font)
        self.order.setText("TAKE ORDER")
        self.order.clicked.connect(self.handle_take_order)
        
        # Create deliver button
        self.deliver = QtWidgets.QPushButton(parent=self.centralwidget)
        self.deliver.setGeometry(QtCore.QRect(500, 420, 131, 51))
        self.deliver.setStyleSheet(button_style % ('#E67E22', '#F39C12', '#D35400'))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.deliver.setFont(font)
        self.deliver.setText("DELIVERED")
        self.deliver.clicked.connect(self.handle_deliver_order)
        
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

        # Load initial data
        self.load_table_data()

    def load_table_data(self):
        """Load data into both tables"""
        try:
            conn = sqlite3.connect('project.db')
            cursor = conn.cursor()
            
            # Query for pastorder table (in process orders)
            process_query = """
                SELECT order_num, order_date, address, price, name 
                FROM delivery 
                WHERE status = 'in process'
            """
            cursor.execute(process_query)
            process_orders = cursor.fetchall()
            
            # Query for currentorder table (in delivery orders)
            delivery_query = """
                SELECT order_num, order_date, address, price, name 
                FROM delivery 
                WHERE status = 'in delivery'
            """
            cursor.execute(delivery_query)
            delivery_orders = cursor.fetchall()
            
            # Populate pastorder table
            self.pastorder.setRowCount(len(process_orders))
            for row, order in enumerate(process_orders):
                for col, value in enumerate(order):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.pastorder.setItem(row, col, item)
            
            # Populate currentorder table
            self.currentorder.setRowCount(len(delivery_orders))
            for row, order in enumerate(delivery_orders):
                for col, value in enumerate(order):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.currentorder.setItem(row, col, item)
            
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.statusbar.showMessage(f"Error loading orders: {e}", 5000)

    def handle_take_order(self):
        """Handle Take Order button click"""
        try:
            # Get the first order number from pastorder table
            if self.pastorder.rowCount() > 0:
                order_num = self.pastorder.item(0, 0).text()
                
                conn = sqlite3.connect('project.db')
                cursor = conn.cursor()
                
                # Update order status to 'in delivery'
                update_query = """
                    UPDATE orders 
                    SET status = 'in delivery' , order_deliver = ?
                    WHERE order_num = ?
                """
                cursor.execute(update_query, (sys.argv[1],order_num,))
                conn.commit()
                # Reload table data
                self.load_table_data()
                
                conn.close()
                self.statusbar.showMessage("Order taken successfully", 3000)
            else:
                self.statusbar.showMessage("No orders available to take", 3000)
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.statusbar.showMessage(f"Error updating order: {e}", 5000)

    def handle_deliver_order(self):
        """Handle Delivered button click"""
        try:
            # Get the first order number from currentorder table
            if self.currentorder.rowCount() > 0:
                order_num = self.currentorder.item(0, 0).text()
                
                conn = sqlite3.connect('project.db')
                cursor = conn.cursor()
                
                # Update order status to 'delivered'
                update_query = """
                    UPDATE orders 
                    SET status = 'delivered' , order_deliver = ? 
                    WHERE order_num = ?
                """
                cursor.execute(update_query, (sys.argv[1],order_num,))
                conn.commit()
                
                # Reload table data
                self.load_table_data()
                
                conn.close()
                self.statusbar.showMessage("Order marked as delivered", 3000)
            else:
                self.statusbar.showMessage("No orders available to deliver", 3000)
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.statusbar.showMessage(f"Error updating order: {e}", 5000)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())