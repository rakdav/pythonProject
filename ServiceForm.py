from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QTableWidgetItem

from Connect import Connect


class ServiceForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(500, 300, 400, 300)
        table = QtWidgets.QTableWidget()
        table.setGeometry(QtCore.QRect(10, 10, 380, 280))
        table.setColumnCount(4)

        self.db_connect = self.connect_to_sql_server()
        self.db_connect.open()
        query = QSqlQuery(self.db_connect)
        query.prepare("SELECT Title,Cost,DurationInSeconds,Discount from Service")
        query.exec()
        if query.isActive():
            query.first()
            i = 0
            while query.isValid():
                table.setRowCount(i)
                table.insertRow(i)
                table.setItem(i, 0, QTableWidgetItem(str(query.value('Title'))))
                table.setItem(i, 1, QTableWidgetItem(str(query.value('Cost'))))
                table.setItem(i, 2, QTableWidgetItem(str(query.value('DurationInSeconds'))))
                table.setItem(i, 3, QTableWidgetItem(str(query.value('Discount'))))
                i = i + 1
                query.next()
        self.db_connect.close()
        form = QtWidgets.QFormLayout()
        form.addRow(table)
        self.setLayout(form)

    def connect_to_sql_server(self):
        db = Connect("HOMEPC\SQLEXPRESS", "db2", "user2", "user2").get_connect()
        return db
