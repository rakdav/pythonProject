from operator import itemgetter

from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QTableWidgetItem

from Connect import Connect


class ServiceForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.sorting=False
        self.setGeometry(500, 300, 400, 300)
        self.table = QtWidgets.QTableWidget()
        self.table.setGeometry(QtCore.QRect(10, 10, 380, 280))
        self.table.setColumnCount(4)
        self.table.clicked.connect(self.sort_by_cost)

        self.db_connect = self.connect_to_sql_server()
        self.db_connect.open()
        query = QSqlQuery(self.db_connect)
        query.prepare("SELECT Title,Cost,DurationInSeconds,Discount from Service")
        query.exec()
        self.services = []
        if query.isActive():
            query.first()
            i = 0
            while query.isValid():
                self.table.setRowCount(i)
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(str(query.value('Title'))))
                self.table.setItem(i, 1, QTableWidgetItem(str(query.value('Cost'))))
                self.table.setItem(i, 2, QTableWidgetItem(str(query.value('DurationInSeconds'))))
                self.table.setItem(i, 3, QTableWidgetItem(str(query.value('Discount'))))
                temp = {"Title": query.value('Title'), "Cost": query.value('Cost'),
                        "DurationInSeconds": query.value('DurationInSeconds'), "Discount": query.value('Discount')}
                self.services.append(temp)
                i = i + 1
                query.next()
        self.db_connect.close()

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.table)
        btn_layout = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("Добавить")
        btn_del = QtWidgets.QPushButton("Удалить")
        btn_record = QtWidgets.QPushButton("Запись на услуги")
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_del)
        btn_layout.addWidget(btn_record)
        left_layout.addLayout(btn_layout)

        right_layout = QtWidgets.QVBoxLayout()
        btn_test = QtWidgets.QPushButton("Добавить")
        right_layout.addWidget(btn_test)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def connect_to_sql_server(self):
        db = Connect("HOMEPC\SQLEXPRESS", "db2", "user2", "user2").get_connect()
        return db

    def sort_by_cost(self):
        self.sorting = not self.sorting
        mas = sorted(self.services, key=itemgetter('Cost'), reverse=self.sorting)
        self.table.clear()
        i = 0
        while i < len(mas):
            self.table.setRowCount(i)
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(mas[i]["Title"]))
            self.table.setItem(i, 1, QTableWidgetItem(str(mas[i]["Cost"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(mas[i]["DurationInSeconds"])))
            self.table.setItem(i, 3, QTableWidgetItem(str(mas[i]["Discount"])))
            i = i + 1
