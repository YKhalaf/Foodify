from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
import sys 
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import subprocess
import json
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        MainWindow.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2980b9, stop:1 #8e44ad);
            }
        """)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Welcome Label with enhanced styling
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 40, 400, 100))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(48)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(255, 255, 255, 30);
                border-radius: 20px;
                padding: 10px;
            }
        """)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        
        # Add Table Widget
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(50, 150, 700, 300))
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                border: 1px solid #2980b9;
            }
        """)
        self.tableWidget.setAlternatingRowColors(True)
        
        # Styled query input
        self.query = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.query.setGeometry(QtCore.QRect(160, 480, 481, 45))
        self.query.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 200);
                border: 2px solid white;
                border-radius: 22px;
                padding: 10px 20px;
                font-size: 16px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                background-color: white;
                border: 2px solid #3498db;
            }
        """)
        self.query.setObjectName("query")
        self.query.setPlaceholderText("Enter your query here...")
        
        # Styled execute button
        self.execute = QtWidgets.QPushButton(parent=self.centralwidget)
        self.execute.setGeometry(QtCore.QRect(310, 550, 181, 51))
        self.execute.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219a52;
            }
        """)
        self.execute.setObjectName("execute")
        self.execute.clicked.connect(self.handle_execute)

        MainWindow.setCentralWidget(self.centralwidget)
        
        # Styled menubar
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setStyleSheet("""
            QMenuBar {
                background-color: rgba(255, 255, 255, 20);
                color: white;
            }
            QMenuBar::item:selected {
                background-color: rgba(255, 255, 255, 40);
            }
        """)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        # Styled statusbar
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setStyleSheet("color: white;")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Store MainWindow reference
        self.MainWindow = MainWindow
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Admin"))
        self.label.setText(_translate("MainWindow", "WELCOME"))
        self.execute.setText(_translate("MainWindow", "Execute"))

    def display_query_results(self, cursor, query_type):
        try:
            # Get results based on query type
            results = cursor.fetchall()
            
            # Clear previous results
            self.tableWidget.clear()
            
            if cursor.description:  # If the query returns any columns
                # Get column names from cursor description
                columns = [description[0] for description in cursor.description]
                
                # Set table dimensions
                self.tableWidget.setRowCount(len(results))
                self.tableWidget.setColumnCount(len(columns))
                
                # Set column headers
                self.tableWidget.setHorizontalHeaderLabels(columns)
                
                # Fill the table with data
                for row_idx, row in enumerate(results):
                    for col_idx, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.tableWidget.setItem(row_idx, col_idx, item)
                
                # Resize columns to content
                self.tableWidget.resizeColumnsToContents()
            else:
                # For queries that don't return results (INSERT, UPDATE, DELETE)
                self.tableWidget.setRowCount(1)
                self.tableWidget.setColumnCount(1)
                self.tableWidget.setHorizontalHeaderLabels(["Result"])
                item = QTableWidgetItem(f"{cursor.rowcount} row(s) affected")
                self.tableWidget.setItem(0, 0, item)
                self.tableWidget.resizeColumnsToContents()
                
        except sqlite3.Error as e:
            # Handle any errors in result display
            self.tableWidget.setRowCount(1)
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setHorizontalHeaderLabels(["Error"])
            item = QTableWidgetItem(str(e))
            self.tableWidget.setItem(0, 0, item)

    def handle_execute(self):
        query_text = self.query.text().strip()

        # Check if query is empty
        if not query_text:
            QMessageBox.warning(self.MainWindow, "Error", "Please enter a query!")
            return

        try:
            # Connect to database
            conn = sqlite3.connect('project.db')
            cursor = conn.cursor()
            
            # Execute the query
            cursor.execute(query_text)
            
            # Identify query type
            query_type = query_text.strip().split()[0].upper()
            
            # Display results for any type of query
            self.display_query_results(cursor, query_type)
            
            # Commit changes for modification queries
            if query_type in ('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER'):
                conn.commit()
            
            # Show success message
            QMessageBox.information(self.MainWindow, "Success", "Query executed successfully!")
            
            # Clear the query input after successful execution
            self.query.clear()
            
        except sqlite3.Error as e:
            # Show error message if query is invalid
            QMessageBox.critical(self.MainWindow, "Database Error",
                               f"Query error: {str(e)}")
        finally:
            # Always close the connection
            if 'conn' in locals():
                conn.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())