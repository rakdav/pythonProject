from operator import itemgetter

from PyQt5 import QtWidgets, QtCore, Qt, QtGui
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QTableWidgetItem

from Connect import Connect


class ServiceForm(QtWidgets.QDialog):
    def __init__(self, role, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.role = role
        self.count_label = QtWidgets.QLabel()
        self.sorting = False
        self.setGeometry(300, 300, 750, 300)

        # загрузка данных из БД
        self.db_connect = self.connect_to_sql_server()
        self.db_connect.open()
        query = QSqlQuery(self.db_connect)
        query.prepare("SELECT Title,Cost,DurationInSeconds,Discount from Service")
        query.exec()
        self.services = []
        if query.isActive():
            query.first()
            while query.isValid():
                temp = {"Title": query.value('Title'), "Cost": query.value('Cost'),
                        "DurationInSeconds": query.value('DurationInSeconds'), "Discount": query.value('Discount')}
                self.services.append(temp)
                query.next()
        self.db_connect.close()

        # формирование левого контейнера
        left_layout = QtWidgets.QVBoxLayout()

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Cost", "DurationInSeconds", "Discount"])
        self.table.horizontalHeaderItem(0).setToolTip("Title")
        self.table.horizontalHeaderItem(1).setToolTip("Cost")
        self.table.horizontalHeaderItem(2).setToolTip("DurationInSeconds")
        self.table.horizontalHeaderItem(3).setToolTip("Discount")
        self.table.setSortingEnabled(True)
        self.fill_table()
        self.table.resizeColumnsToContents()

        btn_layout = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("Добавить")
        btn_del = QtWidgets.QPushButton("Удалить")
        btn_del.clicked.connect(self.service_delete)
        btn_record = QtWidgets.QPushButton("Запись на услуги")
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_del)
        btn_layout.addWidget(btn_record)
        left_layout.addWidget(self.table)
        if self.role == "Admin":
            left_layout.addLayout(btn_layout)

        # формирование правого контейнера
        right_layout = QtWidgets.QVBoxLayout()

        group_box_disc = QtWidgets.QGroupBox("Фильтр по скидке")
        vbox_disc = QtWidgets.QVBoxLayout()
        group_box_disc.setLayout(vbox_disc)
        disc_procent = QtWidgets.QComboBox()
        disc_procent.addItem("Все")
        disc_procent.addItem("от 0 до 5%")
        disc_procent.addItem("от 5% до 15%")
        disc_procent.addItem("от 15% до 30%")
        disc_procent.addItem("от 30% до 70%")
        disc_procent.addItem("от 70% до 100%")
        disc_procent.activated.connect(self.activated)
        vbox_disc.addWidget(disc_procent)

        group_box_title = QtWidgets.QGroupBox("Поиск по названию")
        vbox_title = QtWidgets.QVBoxLayout()
        group_box_title.setLayout(vbox_title)
        title_text = QtWidgets.QLineEdit()
        title_text.textChanged.connect(self.fill_by_title)
        vbox_title.addWidget(title_text)

        group_box_desc = QtWidgets.QGroupBox("Поиск по описанию")
        vbox_desc = QtWidgets.QVBoxLayout()
        group_box_desc.setLayout(vbox_desc)
        title_desc = QtWidgets.QLineEdit()
        vbox_desc.addWidget(title_desc)

        right_layout.addWidget(group_box_disc)
        right_layout.addWidget(group_box_title)
        right_layout.addWidget(group_box_desc)
        right_layout.addWidget(self.count_label)

        # формирование главного контейнера
        main_layout = QtWidgets.QGridLayout()
        main_layout.setSpacing(10)
        main_layout.addLayout(left_layout, 1, 0)
        main_layout.addLayout(right_layout, 1, 1, 1, 5)
        self.setLayout(main_layout)

    def connect_to_sql_server(self):
        db = Connect("HOMEPC\SQLEXPRESS", "db2", "user2", "user2").get_connect()
        return db

    def activated(self, index):
        match index:
            case 0:
                self.fill_table()
            case 1:
                self.filter_by_discount(0, 0.05)
            case 2:
                self.filter_by_discount(0.05, 0.15)
            case 3:
                self.filter_by_discount(0.15, 0.30)
            case 4:
                self.filter_by_discount(0.30, 0.70)
            case 5:
                self.filter_by_discount(0.70, 1)

    # def sort_by_cost(self, e):
    #     column_text = self.table.horizontalHeaderItem(e).text()
    #     self.sorting = not self.sorting
    #     mas = sorted(self.services, key=itemgetter(column_text), reverse=self.sorting)
    #     self.table.clear()
    #     self.table.setHorizontalHeaderLabels(["Title", "Cost", "DurationInSeconds", "Discount"])
    #     i = 0
    #     while i < len(mas):
    #         self.table.setRowCount(i)
    #         self.table.insertRow(i)
    #         self.table.setItem(i, 0, QTableWidgetItem(mas[i]["Title"]))
    #         self.table.setItem(i, 1, QTableWidgetItem(str(mas[i]["Cost"])))
    #         self.table.setItem(i, 2, QTableWidgetItem(str(mas[i]["DurationInSeconds"])))
    #         self.table.setItem(i, 3, QTableWidgetItem(str(mas[i]["Discount"])))
    #         i = i + 1
    def filter_by_discount(self, start, finish):
        self.table.clear()
        self.table.setHorizontalHeaderLabels(["Title", "Cost", "DurationInSeconds", "Discount"])
        i = 0
        for serve in self.services:
            if start <= serve["Discount"] < finish:
                self.table.setRowCount(i)
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(serve["Title"]))
                self.table.setItem(i, 1, QTableWidgetItem(str(serve["Cost"])))
                self.table.setItem(i, 2, QTableWidgetItem(str(serve["DurationInSeconds"])))
                self.table.setItem(i, 3, QTableWidgetItem(str(serve["Discount"])))
                if serve["Discount"] > 0:
                    self.table.item(i, 0).setBackground(QtGui.QColor(127, 255, 0))
                    self.table.item(i, 1).setBackground(QtGui.QColor(127, 255, 0))
                    self.table.item(i, 2).setBackground(QtGui.QColor(127, 255, 0))
                    self.table.item(i, 3).setBackground(QtGui.QColor(127, 255, 0))
                i = i+1
        self.count_label.setText("Всего " + str(i) + " из " + str(len(self.services)))

    def fill_table(self):
        self.table.clear()
        self.table.setHorizontalHeaderLabels(["Title", "Cost", "DurationInSeconds", "Discount"])
        i = 0
        for serve in self.services:
            self.table.setRowCount(i)
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(serve["Title"]))
            self.table.setItem(i, 1, QTableWidgetItem(str(serve["Cost"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(serve["DurationInSeconds"])))
            self.table.setItem(i, 3, QTableWidgetItem(str(serve["Discount"])))
            if serve["Discount"] > 0:
                self.table.item(i, 0).setBackground(QtGui.QColor(127, 255, 0))
                self.table.item(i, 1).setBackground(QtGui.QColor(127, 255, 0))
                self.table.item(i, 2).setBackground(QtGui.QColor(127, 255, 0))
                self.table.item(i, 3).setBackground(QtGui.QColor(127, 255, 0))
            i = i + 1
        self.count_label.setText("Всего " + str(i) + " из " + str(len(self.services)))

    def fill_by_title(self, find_stroka):
        self.table.clear()
        self.table.setHorizontalHeaderLabels(["Title", "Cost", "DurationInSeconds", "Discount"])
        i = 0
        for serve in self.services:
            if find_stroka in serve["Title"]:
                self.table.setRowCount(i)
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(serve["Title"]))
                self.table.setItem(i, 1, QTableWidgetItem(str(serve["Cost"])))
                self.table.setItem(i, 2, QTableWidgetItem(str(serve["DurationInSeconds"])))
                self.table.setItem(i, 3, QTableWidgetItem(str(serve["Discount"])))
                if serve["Discount"] > 0:
                    self.table.item(i, 0).setBackground(QtGui.QColor(127, 255, 0))
                    self.table.item(i, 1).setBackground(QtGui.QColor(127, 255, 0))
                    self.table.item(i, 2).setBackground(QtGui.QColor(127, 255, 0))
                    self.table.item(i, 3).setBackground(QtGui.QColor(127, 255, 0))
                i = i + 1
        self.count_label.setText("Всего "+ str(i) + " из " + str(len(self.services)))

    def service_delete(self):
        pass