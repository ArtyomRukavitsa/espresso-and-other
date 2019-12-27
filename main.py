import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem
from PyQt5 import uic
import sqlite3


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite3")
        self.pushButton.clicked.connect(self.select)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'название сорта', 'степень обжарки',
                                                    'молотый/зерна', 'вкус', 'цена', 'объем упаковки'])

    def select(self):
        req = f"SELECT * FROM Cof WHERE id = {int(self.spinBox.text())}"
        cur = self.con.cursor()
        result = cur.execute(req).fetchone()
        for i in range(len(result)):
            self.tableWidget.setItem(0, i, QTableWidgetItem(str(result[i])))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())