from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtSql import QSqlQuery

from Connect import Connect


class ServiceForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.db_connect = self.connect_to_sql_server()
        self.db_connect.open()
        table=QtWidgets.QTableWidget()
        table.setWindowTitle("Услуги")
        con=QtSql.QSqlDatabase.addDatabase("QMSSQL")
        sqm = QtSql.QSqlQueryModel(parent=table)
        sqm.setQuery("SELECT Title,Cost,DurationInSeconds,Discount FROM Service")
        sqm.setHeaderData(0, QtCore.Qt.Horizontal, "Название")
        sqm.setHeaderData(1, QtCore.Qt.Horizontal, "Стоимость")
        sqm.setHeaderData(2, QtCore.Qt.Horizontal, "Продолжительность")
        sqm.setHeaderData(3, QtCore.Qt.Horizontal, "Скидка")
        table.setModel(sqm)
        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 100)
        table.setColumnWidth(3, 100)
        table.show()
        self.db_connect.close()
        # query = QSqlQuery(self.db_connect)
        # query.prepare("SELECT Title,Cost,DurationInSeconds,Discount from Service")
        # query.exec()
        # while query.next():
        #     print(query.value(0), query.value(1), query.value(2), query.value(3), sep=" ")
        form = QtWidgets.QFormLayout()
        form.addRow(table)
        self.resize(450, 300)
        self.setLayout(form)

    def connect_to_sql_server(self):
        db = Connect("HOMEPC\SQLEXPRESS", "db2", "user2", "user2").get_connect()
        return db
