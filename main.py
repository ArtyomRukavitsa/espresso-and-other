import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
from PyQt5 import uic
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.pushButton_2.clicked.connect(self.newForm)

    def select(self):
        req = f"SELECT * FROM Cof WHERE id = {int(self.spinBox.text())}"
        cur = self.con.cursor()
        result = cur.execute(req).fetchone()
        if result:
            for i in range(len(result)):
                self.tableWidget.setItem(0, i, QTableWidgetItem(str(result[i])))

    def newForm(self):
        self.new = NewWidget()
        self.new.show()


class NewWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.change)
        self.show()
        self.con = sqlite3.connect("coffee.sqlite3")
        self.titles = None

    def change(self):
        self.modified = {}
        if self.lineEdit.text():
            self.modified['name'] = self.lineEdit.text()
        if self.spinBox_2.text():
            self.modified['degree'] = int(self.spinBox_2.text())
        if self.lineEdit_2.text():
            self.modified['beansOrGround'] = self.lineEdit_2.text()
        if self.lineEdit_3.text():
            self.modified['taste'] = self.lineEdit_3.text()
        if self.lineEdit_4.text():
            self.modified['price'] = int(self.lineEdit_4.text())
        if self.lineEdit_5.text():
            self.modified['volume'] = int(self.lineEdit_5.text())
        cur = self.con.cursor()
        que = "UPDATE Cof SET\n"
        for key in self.modified.keys():
            que += "{}='{}',\n".format(key, self.modified.get(key))
        que = que[:-2]
        que += f"WHERE id = {int(self.spinBox.text())}"
        cur.execute(que)
        self.con.commit()

    def add(self):
        cur = self.con.cursor()
        que = f"INSERT into Cof(id, name, degree, beansOrGround, " \
            f"taste, price, volume) VALUES ({int(self.spinBox.text())}, " \
            f"'{self.lineEdit.text()}', {int(self.spinBox_2.text())}," \
            f"'{self.lineEdit_2.text()}', '{self.lineEdit_3.text()}', " \
            f"{int(self.lineEdit_4.text())}, {int(self.lineEdit_5.text())})"
        cur.execute(que)
        self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())