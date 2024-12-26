import sys
import sqlite3
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from re2 import Ui_MainWindow
import json 
import subprocess
class RestaurantSearch(Ui_MainWindow):
    def __init__(self):
        self.db_path = 'project.db'
        self.cart = json.loads(sys.argv[2]) 
        
    def setupUi(self, MainWindow):
        """Override setupUi to add button connections and initial data"""
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        
        self.back.clicked.connect(self.go_back)
        self.srestaurnat.clicked.connect(self.search_restaurant)
        self.smeal.clicked.connect(self.search_meal)
        self.adchart.clicked.connect(self.add_to_cart)
        
        self.load_all_meals()
        
    def load_all_meals(self):
        """Load all meals into the table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM search")
            results = cursor.fetchall()
            
            self.populate_table(results)
            
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def search_restaurant(self):
        """Search meals by restaurant name"""
        restaurant_name = self.restaurnat.text().strip()
        
        if not restaurant_name:
            self.show_error("Please enter a restaurant name")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM search WHERE restaurant like ?", ('%'+restaurant_name+'%',))
            results = cursor.fetchall()
            
            if not results:
                self.show_error("No restaurants found with that name")
                return
                
            self.populate_table(results)
            
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def search_meal(self):
        """Search by meal name"""
        meal_name = self.meal.text().strip()
        
        if not meal_name:
            self.show_error("Please enter a meal name")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM search WHERE name like ?", ('%'+meal_name+'%',))
            results = cursor.fetchall()
            
            if not results:
                self.show_error("No meals found with that name")
                return
                
            self.populate_table(results)
            
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def add_to_cart(self):
        """Add selected meal to cart"""
        meal_id = self.achart.text().strip()
        
        if not meal_id:
            self.show_error("Please enter a meal ID")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if meal exists in meal table
            cursor.execute("SELECT name, meal_id, price FROM meal WHERE meal_id = ?", (meal_id,))
            meal_data = cursor.fetchone()
            
            if not meal_data:
                self.show_error("Invalid meal ID")
                return
                
            # Add to cart list (sys.argv[1])
            self.cart.append({
                    'name': meal_data[0],
                    'meal_id': meal_data[1],
                    'price': meal_data[2]
                })
            self.show_success("Meal added to cart successfully")
            self.achart.clear()
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
    def populate_table(self, results):
        """Populate the table with search results"""
        self.search.setRowCount(0)  # Clear existing rows
        
        for row_number, row_data in enumerate(results):
            self.search.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.search.setItem(row_number, column_number, item)
                
    def go_back(self):
        """Return to user interface"""
        self.MainWindow.close()
        chary = []
        chart = json.dumps(self.cart)
        subprocess.run([sys.executable, 'user.py',sys.argv[1],chart])
            
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
    ui = RestaurantSearch()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())