import sys
import sqlite3
from PyQt6 import QtWidgets
from re1 import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox

class RestaurantManager(Ui_MainWindow):
    def __init__(self):
        self.res_id = None
        self.db_path = 'project.db'  # Update this with your SQLite database path
        
    def setupUi(self, MainWindow):
        """Override setupUi to add button connections"""
        super().setupUi(MainWindow)
        
        # Get restaurant ID for the logged-in user when the application starts
        if len(sys.argv) > 1:
            print()
            self.get_restaurant_id(sys.argv[1])
            
        
        # Connect buttons to their respective functions
        self.update.clicked.connect(self.update_meal)
        self.add.clicked.connect(self.add_meal)
        self.delete_2.clicked.connect(self.delete_meal)
        
    def get_restaurant_id(self, username):
        """Fetch restaurant ID for the logged-in user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """SELECT res_id FROM user 
                      JOIN restaurant ON user.user_name = restaurant.owner 
                      WHERE user_name = ?"""
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            
            if result:
                self.res_id = result[0]
            else:
                self.show_error("User not found or not associated with any restaurant")
                
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def check_meal_exists(self, meal_id):
        """Check if a meal ID already exists in the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT COUNT(*) FROM meal WHERE meal_id = ?"
            cursor.execute(query, (meal_id,))
            count = cursor.fetchone()[0]
            
            return count > 0
            
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    def update_meal(self):
        """Handle meal update operation"""
        if self.res_id is None:
            self.show_error("No restaurant ID found")
            return
            
        meal_id = self.meal_id.text().strip()
        price = self.price.text().strip()
        name = self.mealname.text().strip()
        
        # Validate all fields are filled
        if not all([meal_id, price, name]):
            self.show_error("All fields must be filled")
            return
            
        # Validate price is numeric
        try:
            price = float(price)
        except ValueError:
            self.show_error("Price must be a number")
            return
            
        if not self.check_meal_exists(meal_id):
            self.show_error("Meal ID does not exist")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """UPDATE meal
                      SET price = ?, name = ? 
                      WHERE meal_id = ? AND res_id = ?"""
            cursor.execute(query, (price, name, meal_id, self.res_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                self.show_success("Meal updated successfully")
                self.clear_fields()
            else:
                self.show_error("No meal was updated. Please check if the meal belongs to your restaurant.")
            
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def add_meal(self):
        """Handle meal addition operation"""
        if self.res_id is None:
            self.show_error("No restaurant ID found")
            return
            
        meal_id = self.meal_id.text().strip()
        price = self.price.text().strip()
        name = self.mealname.text().strip()
        
        # Validate all fields are filled
        if not all([meal_id, price, name]):
            self.show_error("All fields must be filled")
            return
            
        # Validate price is numeric
        try:
            price = float(price)
        except ValueError:
            self.show_error("Price must be a number")
            return
            
        if self.check_meal_exists(meal_id):
            self.show_error("Meal ID already exists")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """INSERT INTO meal (meal_id, name, price, res_id)
                      VALUES (?, ?, ?, ?)"""
            cursor.execute(query, (meal_id, name, price, self.res_id))
            conn.commit()
            
            self.show_success("Meal added successfully")
            self.clear_fields()
            
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def delete_meal(self):
        """Handle meal deletion operation"""
        if self.res_id is None:
            self.show_error("No restaurant ID found")
            return
            
        meal_id = self.meal_id.text().strip()
        
        if not meal_id:
            self.show_error("Meal ID is required")
            return
            
        if not self.check_meal_exists(meal_id):
            self.show_error("Meal ID does not exist")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "DELETE FROM meal WHERE meal_id = ? AND res_id = ?"
            cursor.execute(query, (meal_id, self.res_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                self.show_success("Meal deleted successfully")
                self.clear_fields()
            else:
                self.show_error("No meal was deleted. Please check if the meal belongs to your restaurant.")
            
        except sqlite3.Error as err:
            self.show_error(f"Database error: {str(err)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def clear_fields(self):
        """Clear all input fields"""
        self.meal_id.clear()
        self.price.clear()
        self.mealname.clear()

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
    if len(sys.argv) != 2:
        print("Usage: python restaurant_manager.py <username>")
        sys.exit(1)
        
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = RestaurantManager()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())