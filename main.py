from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QLineEdit,QComboBox,QDateEdit,QTableWidget,QVBoxLayout,QHBoxLayout,QMessageBox,QTableWidgetItem,QDialog
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate,Qt
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets,QtGui
import sys
#import pyqtgraph as pg
    
class exepenseApp(QWidget):
    def __init__(self):
        super().__init__()

        self.datelabel=QLabel("Date:")
        self.dateedit=QDateEdit()
        self.dateedit.setDisplayFormat("dd-MM-yyyy")
        self.dateedit.setDate(QDate.currentDate())
        
        self.categorylabel=QLabel("Category:")
        self.catgorycomb=QComboBox()
        self.catlist=["Food","Transport","Entertainment","Shopping","Rent","Study","Vacations","Others"]
        for i in (self.catlist):
            self.catgorycomb.addItem(i)
        
        self.amountleb=QLabel("Amount:")
        self.amounttext=QLineEdit()
    
        self.descLeb=QLabel("Description:")
        self.descText=QLineEdit()
    
        self.addbut=QPushButton("Add Expense")
        self.addbut.clicked.connect(self.addexpense)
        
        self.delbut=QPushButton("Delete Expense")
        self.delbut.clicked.connect(self.deleterow)
        
        self.plotdatabut=QPushButton("Show Plotted Data")
        self.plotdatabut.clicked.connect(self.plotdatafunc)
        
        self.table=QTableWidget()
        self.table.setColumnCount(5)
        self.heads=["ID","Date","Category","Amount","Description"]
        self.table.setHorizontalHeaderLabels(self.heads)
        #database create
        self.db=QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("expense.db")
        self.dbname=self.db.databaseName()
        if not self.db.open():
            QMessageBox.critical(None,"Error","Could not open your Database")
            sys.exit(1)
        query=QSqlQuery()
        query.exec_(''' CREATE TABLE IF NOT EXISTS expense(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT ,
            Category TEXT ,
            Amount REAL NOT NULL,
            Description TEXT 
            )
            ''')
        
        self.setStyleSheet("""
            QWidget{
                color:black;
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 255, 0.97), stop:1 rgba(138, 43, 226, 255));
            }
            QTableWidget,
            QMessageBox
            {   color:Yellow;
                font-size: 12px;
                font-family: Arial;
                background:black;
                
            }
        
            QLabel,QLineEdit,QComboBox,QDateEdit{
                font-weight: bold;
                color: balck;
                background: white;
            }
            QPushButton{
                background-color: rgba(52, 156, 3, 1);
                color: Black;
                font:bold 20px;
                border: 1px solid blue;
                border-radius: 5px;
                font-style:italic;
            }
            QPushButton:hover{
                background-color: rgba(15, 193, 229, 0.93);
                color: white;
                font:25px;
                font-style:italic;
                border: 1px solid blue;
                }
            QMessageBox{
                background-color: black;
                color: white;
                width:270px;
            }
            QHBoxLayout{
                spacing: 3px;
                height:60px;
            }
            QMessageBox
            {
                background-color: black;
                color: white;
                width:270px;
            }
        """)
        self.table.setStyleSheet("""
            
            QTableWidget{
                color:white;
                font-size: 12px;
                font-family: Arial;
                font-weight:bold;
                background:black;
            
            }""")
        self.datelabel.setAlignment(Qt.AlignCenter)
        self.categorylabel.setAlignment(Qt.AlignCenter)
        self.amountleb.setAlignment(Qt.AlignCenter)
        self.descLeb.setAlignment(Qt.AlignCenter)
        
        self.mLayout=QVBoxLayout()
        self.r1=QHBoxLayout()
        self.r2=QHBoxLayout()
        self.r3=QHBoxLayout()
        #self.r4=QHBoxLayout()
        self.r1.addWidget(self.datelabel)
        self.r1.addWidget(self.dateedit)
        self.r1.addWidget(self.categorylabel)
        self.r1.addWidget(self.catgorycomb)
        
        self.r2.addWidget(self.amountleb)
        self.r2.addWidget(self.amounttext)
        self.r2.addWidget(self.descLeb)
        self.r2.addWidget(self.descText)
        
        self.r3.addWidget(self.addbut)
        self.r3.addWidget(self.delbut)
        self.r3.addWidget(self.plotdatabut)
        #self.r4.addWidget(self.table)      
        self.mLayout.addLayout(self.r1)
        self.mLayout.addLayout(self.r2)
        self.mLayout.addLayout(self.r3)
        self.mLayout.addWidget(self.table)
        self.setLayout(self.mLayout)
        self.load_table()
        
    def addexpense(self):
        date=self.dateedit.date().toString("dd-MM-yyyy")
        category=self.catgorycomb.currentText()
        amount=self.amounttext.text()
        describsion=self.descText.text()
        #add row to table 
        query=QSqlQuery()
        query.prepare( '''
                        INSERT INTO expense(Date,Category,Amount,Description)
                        VALUES (?,?,?,?)
                        ''')
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(describsion)
     
        query.exec_()
        self.load_table()
        self.dateedit.setDate(QDate.currentDate())
        self.catgorycomb.setCurrentIndex(0)
        self.amounttext.clear()
        self.descText.clear()
        self.load_table()

    def load_table(self):
            self.table.setRowCount(0)
            query=QSqlQuery(''' SELECT * FROM expense ''')
            row =0
            while query.next():
                
                exID=query.value(0)
                date=query.value(1)
                cat=query.value(2)
                amount=query.value(3)
                desc=query.value(4)
                
                self.table.insertRow(row)
                self.table.setItem(row,0,QTableWidgetItem(str(exID)))
                self.table.setItem(row,1,QTableWidgetItem(date))
                self.table.setItem(row,2,QTableWidgetItem(cat))
                self.table.setItem(row,3,QTableWidgetItem(str(amount)))
                self.table.setItem(row,4,QTableWidgetItem(desc))
                row +=1
    
    def deleterow(self):
        row = self.table.currentRow()
        if row ==-1:
            QMessageBox.warning(self,"No Data is choosen","please Choose an expense to delete")
            return
        confirm=QMessageBox.question(self,"Are You Sure?","Do You want to Delete The Expense",QMessageBox.Yes | QMessageBox.No )
        if confirm==QMessageBox.No :return
        
        query = QSqlQuery()
        query.prepare('''DELETE FROM expense WHERE ID = ?''')
        query.addBindValue(self.table.item(row,0).text())
        query.exec_()
        self.load_table()
    
    
    def count_category_occurrences(self, db, category_name):
        query = QSqlQuery(db)
        query_string ="""
            SELECT COUNT(*) AS occurrence_count
            FROM expense
            WHERE Category = :category_name
        """
        query.prepare(query_string)

        # Bind the category name to the placeholder
        query.bindValue(":category_name", category_name)

        if query.exec_():
            if query.next():
                return query.value(0)
            else:
                print("No results found for the given category.")
                return 0
        else:
            print("Error executing query:", query.lastError().text())
            return 0

    
    
    def countcat(self):
        data = []  # List to store category counts
        category_to_count = self.catlist

    # Iterate through categories and count occurrences
        for category in category_to_count:
            count = self.count_category_occurrences(self.db, category)
            print(f"The category '{category}' occurs {count} times.")
            data.append(count)
        return data

    def plotdatafunc(self):
        data = self.countcat()  
        plt.figure(figsize=(12,6))

        plt.bar(self.catlist,data)
        plt.xlabel('Category')
        plt.ylabel('Count')
        plt.legend("CountNo")
        plt.title("No: of Spending Money  on Basis Categories ")
        plt.xlim(-1, 8)  
        plt.ylim(-2, 20)
        plt.show()
        
        return 
        
class Signup(QWidget):
    
    def __init__(self):

        self.welText=QLabel("Welcome to ExpenseTracker")
        self.welText.move(100, 100)
        self.welText.resize(100, 330)
        self.but=QPushButton("Enter")
        self.but.move(100, 100)
        self.but.clicked.connect(self.entry)
        super().__init__()
            
        self.welText=QLabel("Welcome to ExpenseTracker")
        self.welText.move(100, 100)
        self.welText.resize(200, 50)
        self.welText.setStyleSheet("color:black;")
        self.row1=QHBoxLayout()
        self.row1.addWidget(self.welText)
        self.welText.setAlignment(Qt.AlignCenter)

        # Set the stylesheet
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 192, 203, 255), stop:1 rgba(138, 43, 226, 255));
            }

            QLabel {
                font-weight: bold;
                color: white;
                text-align:center;
            }
            QPushButton{
                background-color: #4CAF50;
                color: white;
                font:bold 20px;
                border: 1px solid blue;
                border-radius: 5px;
                font-style:italic;
            }
            QPushButton:hover{
                background-color: #3e8e41;
                color: white;
                font:30px;
                font-style:italic;
                border: 1px solid blue;
                }
        """)
        self.row2=QHBoxLayout()
        self.row2.addWidget(self.but)
        
        self.mlayout=QVBoxLayout()
        self.mlayout.addLayout(self.row1)
        self.mlayout.addLayout(self.row2)
        self.setLayout(self.mlayout)
        
    def entry(self):
        self.close()
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.show()
    
if __name__ == "__main__":
    
    app=QApplication(sys.argv)
    widget=QtWidgets.QStackedWidget()
    signupwin=Signup()
    Ewindow = exepenseApp()
    Ewindow.resize(674,400)
    Ewindow.setWindowTitle("Expense Tracker")
    Ewindow.setWindowIcon(QIcon("expens.png"))
    
    widget.addWidget(signupwin)
    widget.addWidget(Ewindow)
    
    widget.resize(674,400)
    widget.setWindowTitle("Expense Tracker")
    widget.setWindowIcon(QIcon("expens.png"))
    
    widget.setStyleSheet("""
    QStackedWidget
    {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(138, 0, 108, 1), stop:1 rgba(0, 48, 255, 0.96));
        color: black;
        font: 20px;
        font-style: italic;
    }
    """)
    widget.show()
    app.exec_()
    
        


