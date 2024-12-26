import sys
import sqlite3
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from re3 import Ui_MainWindow
import json 
import subprocess
class CartManager(Ui_MainWindow):
    def __init__(self):
        self.db_path = 'project.db'
        self.cart_list = json.loads(sys.argv[2])
        self.username = sys.argv[1]
        
    def setupUi(self, MainWindow):
        """Override setupUi to add button connections and initial data"""
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow            
        # Connect buttons to their respective functions
        self.back.clicked.connect(self.go_back)
        self.delete_2.clicked.connect(self.delete_item)
        self.order.clicked.connect(self.process_order)
        
        # Display initial cart contents
        self.update_cart_display()
        
    def update_cart_display(self):
        """Update the table widget with current cart contents"""
        self.chart.setRowCount(0)  # Clear existing rows
        
        for row_number, item in enumerate(self.cart_list):
            self.chart.insertRow(row_number)
            # Item Number (1-based indexing for user-friendly display)
            self.chart.setItem(row_number, 0, QtWidgets.QTableWidgetItem(str(row_number + 1)))
            # Meal Name
            self.chart.setItem(row_number, 1, QtWidgets.QTableWidgetItem(item['name']))
            # Meal ID
            self.chart.setItem(row_number, 2, QtWidgets.QTableWidgetItem(str(item['meal_id'])))
            # Price
            self.chart.setItem(row_number, 3, QtWidgets.QTableWidgetItem(str(item['price'])))
            
    def delete_item(self):
        """Delete item from cart based on item number"""
        item_number = self.id.text().strip()
        
        if not item_number:
            self.show_error("Please enter an item number")
            return
            
        try:
            item_number = int(item_number)
            if item_number < 1 or item_number > len(self.cart_list):
                self.show_error("Invalid item number")
                return
                
            # Remove item from cart list (adjust for 0-based indexing)
            self.cart_list.pop(item_number - 1)
            
            # Update display
            self.update_cart_display()
            self.id.clear()
            self.show_success("Item removed from cart")
            
        except ValueError:
            self.show_error("Please enter a valid number")
            
    def process_order(self):
        """Process the order and save to database"""
        if not self.cart_list:
            self.show_error("Cart is empty")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate total price
            total_price = sum(item['price'] for item in self.cart_list)
            
            # Insert order
            cursor.execute("INSERT INTO orders (price, order_owner) VALUES (?, ?)",
                         (total_price, self.username))
            conn.commit()
            
            # Get order number (last inserted row id)
            cursor.execute("SELECT COUNT(*) FROM orders")
            order_num = cursor.fetchone()[0]
            
            # Insert order meals
            for item in self.cart_list:
                cursor.execute("INSERT INTO order_meal VALUES (?, ?)",
                             (order_num, item['meal_id']))
            conn.commit()
            
            # Clear cart
            self.cart_list = []
            sys.argv[2] = str(self.cart_list)
            self.update_cart_display()
            
            self.show_success(f"Order #{order_num} placed successfully!")
            
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def go_back(self):
        self.MainWindow.close()
        subprocess.run([sys.executable, 'user.py',self.username,json.dumps(self.cart_list)])
            
    def show_error(self, message):
        """Display error message box"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec()
        
    def show_success(self, message):
        """Display success message box"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Success")
        msg.setInformativeText(message)
        msg.setWindowTitle("Success")
        msg.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = CartManager()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())