from PyQt5 import QtWidgets

from ServiceForm import ServiceForm


class AdminAutorizeWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        labelPassword = QtWidgets.QLabel()
        labelPassword.setText("Введите пароль")
        self.textPassword = QtWidgets.QLineEdit()
        self.textPassword.setEchoMode(QtWidgets.QLineEdit.Password)

        btnOk = QtWidgets.QPushButton("OK")
        btnOk.resize(btnOk.sizeHint())
        btnOk.move(50, 50)
        btnOk.clicked.connect(self.btnOKClicked)

        form = QtWidgets.QFormLayout()
        form.addRow(labelPassword)
        form.addRow(self.textPassword)
        form.addRow(btnOk)
        self.setLayout(form)

    def btnOKClicked(self):
        if self.textPassword.text() == "0000":
            serviceForm = ServiceForm(self)
            serviceForm.exec()
