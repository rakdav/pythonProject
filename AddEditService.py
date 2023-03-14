from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlQuery

from Connect import Connect


class AddEditService(QtWidgets.QDialog):
    def __init__(self, role, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        label_image = QtWidgets.QLabel()
        btn_load = QtWidgets.QPushButton("Загрузить")
        self.title = QtWidgets.QLineEdit()
        self.cost = QtWidgets.QLineEdit()
        self.duration = QtWidgets.QLineEdit()
        self.desc = QtWidgets.QLineEdit()
        self.Disc = QtWidgets.QLineEdit()
        btn_ok=QtWidgets.QPushButton("Сохранить")
        btn_ok.clicked.connect()

    def connect_to_sql_server(self):
        db = Connect("HOMEPC\SQLEXPRESS", "db2", "user2", "user2").get_connect()
        return db

    def insert_to_db(self):
        self.db_connect = self.connect_to_sql_server()
        self.db_connect.open()
        query = QSqlQuery(self.db_connect)
        query.prepare(f"INSERT INTO Services values ('{self.title}',{self.cost})")
        query.exec(

