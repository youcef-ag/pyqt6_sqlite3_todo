from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        Form.resize(319, 547)
        Form.setMinimumSize(QtCore.QSize(200, 400))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setStyleSheet("background-color: rgb(168, 157, 167);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.task_input = QtWidgets.QLineEdit(parent=self.frame)
        self.task_input.setStyleSheet("background-color: rgb(222, 222, 222);")
        self.task_input.setObjectName("task_input")
        self.verticalLayout.addWidget(self.task_input)
        self.add_button = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        self.add_button.setFont(font)
        self.add_button.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.edit_button = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        self.edit_button.setFont(font)
        self.edit_button.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.edit_button.setObjectName("edit_button")
        self.verticalLayout.addWidget(self.edit_button)
        self.delete_button = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        self.delete_button.setFont(font)
        self.delete_button.setStyleSheet("background-color: rgb(213, 119, 88);")
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout.addWidget(self.delete_button)
        self.complete_button = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        self.complete_button.setFont(font)
        self.complete_button.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.complete_button.setObjectName("complete_button")
        self.verticalLayout.addWidget(self.complete_button)
        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.TextFormat.MarkdownText)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.task_list = QtWidgets.QListView(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Adobe Pi Std")
        font.setPointSize(11)
        font.setBold(False)
        font.setStrikeOut(False)
        self.task_list.setFont(font)
        self.task_list.setStyleSheet("background-color: rgb(211, 211, 211);")
        self.task_list.setModelColumn(0)
        self.task_list.setObjectName("task_list")
        self.verticalLayout.addWidget(self.task_list)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "list des tâches"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">Ajouter une tâche</span></p></body></html>"))
        self.add_button.setText(_translate("Form", "Ajouter une tâche"))
        self.edit_button.setText(_translate("Form", "Éditer une tâche"))
        self.delete_button.setText(_translate("Form", "Supprimer une tâche"))
        self.complete_button.setText(_translate("Form", "Marquer comme complétée"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"center\">List des tâche</p></body></html>"))


class TaskApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Connect buttons to their respective functions
        self.ui.add_button.clicked.connect(self.add_task)
        self.ui.edit_button.clicked.connect(self.edit_task)
        self.ui.delete_button.clicked.connect(self.delete_task)
        self.ui.complete_button.clicked.connect(self.complete_task)

        # Initialize SQLite database and create the tasks table
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Load tasks from the database
        self.load_tasks()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT,
            completed INTEGER
        )''')
        self.conn.commit()

    def load_tasks(self):
        model = self.get_task_list_model()
        self.ui.task_list.setModel(model)

    def get_task_list_model(self):
        model = QtGui.QStandardItemModel()
        self.cursor.execute("SELECT id, task_text, completed FROM tasks")
        for row in self.cursor.fetchall():
            item = QtGui.QStandardItem(row[1])
            item.setData(row[0], QtCore.Qt.ItemDataRole.UserRole)
            if row[2]:  # Check if the task is completed
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(QtGui.QColor(0, 128, 0))  # Set the text color to green
            model.appendRow(item)
        return model

    def add_task(self):
        task_text = self.ui.task_input.text()
        if task_text:
            self.cursor.execute("INSERT INTO tasks (task_text, completed) VALUES (?, 0)", (task_text,))
            self.conn.commit()
            self.load_tasks()
            self.ui.task_input.clear()

    def edit_task(self):
        selected_indexes = self.ui.task_list.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            task_id = selected_index.data(QtCore.Qt.ItemDataRole.UserRole)
            new_text, ok = QtWidgets.QInputDialog.getText(self, "Edit Task", "Edit Task:", text=selected_index.data())
            if ok and new_text:
                self.cursor.execute("UPDATE tasks SET task_text = ? WHERE id = ?", (new_text, task_id))
                self.conn.commit()
                self.load_tasks()

    def delete_task(self):
        selected_indexes = self.ui.task_list.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            task_id = selected_index.data(QtCore.Qt.ItemDataRole.UserRole)
            self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
            self.load_tasks()

    def complete_task(self):
        selected_indexes = self.ui.task_list.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            task_id = selected_index.data(QtCore.Qt.ItemDataRole.UserRole)
            self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
            self.conn.commit()
            
            self.load_tasks()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    task_app = TaskApp()
    task_app.show()
    sys.exit(app.exec())
