from PyQt5 import QtWidgets, QtCore
import sys

from PyQt5.QtGui import QIcon

from AdminAutorize import AdminAutorizeWindow


class RegisterWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        btnUser = QtWidgets.QPushButton("Обычный режим")
        btnUser.resize(btnUser.sizeHint())
        btnUser.move(50, 50)


        btnAdmin = QtWidgets.QPushButton("Режим администратора")
        btnAdmin.resize(btnAdmin.sizeHint())
        btnAdmin.move(50, 50)
        btnAdmin.clicked.connect(self.btnUserClicked)

        form = QtWidgets.QFormLayout()
        form.addRow(btnUser)
        form.addRow(btnAdmin)
        self.setLayout(form)

    def btnUserClicked(self):
        dialog = AdminAutorizeWindow(self)
        dialog.exec()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    application = RegisterWindow()
    application.setWindowTitle("Окно регистрации")
    application.setGeometry(300, 250, 200, 200)
    application.setWindowFlags(QtCore.Qt.Window)
    application.setFixedSize(200, 100)
    application.setWindowIcon(QIcon('beauty_logo.ico'))
    application.show()
    sys.exit(app.exec())
