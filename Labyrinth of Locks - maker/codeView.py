from functools import partial

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QLabel, QLineEdit, QMessageBox, \
    QPlainTextEdit


class CodeView:
    def __init__(self):
        self.app = QApplication([])
        self.codeViewWindow = QWidget()
        self.iconsViewWindow = QWidget()

        self.label = QLabel('Mode:\t\t Rows:\t\t  Cols:', self.codeViewWindow)
        self.modeComboBox = QComboBox(self.codeViewWindow)
        self.rowsComboBox = QComboBox(self.codeViewWindow)
        self.colsComboBox = QComboBox(self.codeViewWindow)
        self.label2 = QLabel('Message:', self.codeViewWindow)
        self.messageLineEdit = QLineEdit('', self.codeViewWindow)
        self.button = QPushButton('Enter the Labyrinth', self.codeViewWindow)

        self.iconButtons = None
        self.finishButton = QPushButton('Show Code', self.iconsViewWindow)

        self.iconValues = None
        self.icons = []

        self.mode = 0
        self.rows = 0
        self.cols = 0
        self.intMessage = 0

        self.initialize_window()

    def initialize_window(self):
        self.codeViewWindow.setWindowTitle('Labyrinth of Locks - maker')
        self.iconsViewWindow.setWindowTitle('Labyrinth of Locks - maker')

        self.label.setGeometry(25, 10, 435, 50)

        self.modeComboBox.addItems(['2', '3'])
        self.modeComboBox.setCurrentIndex(0)
        self.modeComboBox.setGeometry(25, 60, 90, 40)

        self.rowsComboBox.addItems(['2', '3', '4', '5', '6', '7', '8', '9'])
        self.rowsComboBox.setCurrentIndex(2)
        self.rowsComboBox.setGeometry(192, 60, 90, 40)

        self.colsComboBox.addItems(['2', '3', '4', '5', '6', '7', '8', '9'])
        self.colsComboBox.setCurrentIndex(2)
        self.colsComboBox.setGeometry(360, 60, 90, 40)

        self.label2.setGeometry(25, 105, 435, 50)

        self.messageLineEdit.setGeometry(25, 155, 425, 50)

        self.button.setGeometry(250, 220, 200, 50)
        self.button.clicked.connect(self.code_view_on_click)

        # self.iconsViewWindow tło dodać

        self.codeViewWindow.setFixedSize(475, 290)
        self.codeViewWindow.show()
        self.app.exec_()

    def code_view_on_click(self):
        self.codeViewWindow.hide()
        self.create_icons_view()
        self.iconsViewWindow.show()
        self.intMessage = int.from_bytes(self.messageLineEdit.text().encode('utf-8'), byteorder='big')

    def create_icons_view(self):
        self.mode = int(self.modeComboBox.currentText())
        self.rows = int(self.rowsComboBox.currentText())
        self.cols = int(self.colsComboBox.currentText())

        self.iconButtons = [[QPushButton('', self.iconsViewWindow) for _ in range(self.cols)] for _ in range(self.rows)]
        self.iconValues = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        button_width = 150
        button_height = 150

        self.icons.append(QIcon('images/img1.png'))
        self.icons.append(QIcon('images/img2.png'))
        self.icons.append(QIcon('images/img3.png'))

        for i in range(self.rows):
            for j in range(self.cols):
                self.iconButtons[i][j].setGeometry(j * button_width, i * button_height, button_width, button_height)
                self.iconButtons[i][j].setIcon(self.icons[0])
                self.iconValues[i][j] = 0
                self.iconButtons[i][j].setIconSize(self.iconButtons[i][j].size())
                self.iconButtons[i][j].clicked.connect(partial(self.on_click_icon, i, j))

        self.finishButton.setGeometry(self.cols * 150 / 2 - 100, self.rows * 150, 200, 50)
        self.finishButton.clicked.connect(self.finish_button)

        self.iconsViewWindow.setFixedSize(self.cols * 150, self.rows * 150 + 50)

    def on_click_icon(self, x, y):
        self.change_icon(x, y)
        if x > 0:
            self.change_icon(x - 1, y)
        if y > 0:
            self.change_icon(x, y - 1)
        if x < self.rows-1:
            self.change_icon(x + 1, y)
        if y < self.cols-1:
            self.change_icon(x, y + 1)
        self.get_code()

    def change_icon(self, x, y):
        future_value = (self.iconValues[x][y] + 1) % self.mode
        self.iconValues[x][y] = future_value
        self.iconButtons[x][y].setIcon(self.icons[future_value])

    def finish_button(self):
        msg = QMessageBox()
        msg.setWindowTitle('Code for true Labyrinth')
        # msg.setText(str(self.get_code()))

        text_edit = QPlainTextEdit(msg)
        text_edit.setPlainText(str(self.get_code()))
        text_edit.setReadOnly(False)
        text_edit.setBaseSize(300, 40)

        msg.exec_()

    def get_code(self):
        code = self.intMessage
        for i in reversed(range(self.rows)):
            for j in reversed(range(self.cols)):
                code *= self.mode
                code += self.iconValues[i][j]
                print(code)
        return code
