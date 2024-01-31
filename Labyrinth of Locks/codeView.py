from functools import partial

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox
from _decimal import getcontext, Decimal


class CodeView:
    def __init__(self):
        self.app = QApplication([])
        self.codeViewWindow = QWidget()
        self.iconsViewWindow = QWidget()

        self.label = QLabel('Enter your code', self.codeViewWindow)
        self.line = QLineEdit('', self.codeViewWindow)
        self.button = QPushButton('Enter the Labyrinth', self.codeViewWindow)
        self.iconButtons = None
        self.iconValues = None
        self.icons = []

        self.mode = 0
        self.rows = 0
        self.cols = 0
        self.message = ''

        self.initialize_window()

    def initialize_window(self):
        self.codeViewWindow.setWindowTitle('Labyrinth of Locks')
        self.iconsViewWindow.setWindowTitle('Labyrinth of Locks')

        self.label.setGeometry(25, 10, 435, 50)

        self.line.setGeometry(25, 60, 425, 50)

        self.button.setToolTip('This is an example button xx')
        self.button.setGeometry(250, 130, 200, 50)
        self.button.clicked.connect(self.code_view_on_click)

        # self.iconsViewWindow tło dodać

        self.codeViewWindow.setFixedSize(475, 200)
        self.codeViewWindow.show()
        self.app.exec_()

    def code_view_on_click(self):
        if self.line.text().__sizeof__() > 6 and self.line.text().isnumeric():
            print(self.line.text())
            self.codeViewWindow.hide()
            self.create_icons_view()
            self.iconsViewWindow.show()

    def create_icons_view(self):
        seed = self.get_icons_attributes()

        self.iconButtons = [[QPushButton('', self.iconsViewWindow) for _ in range(self.cols)] for _ in range(self.rows)]
        self.iconValues = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        button_width = 150
        button_height = 150

        getcontext().prec = 100

        self.icons.append(QIcon('images/img1.png'))
        self.icons.append(QIcon('images/img2.png'))
        if self.mode == 3:
            self.icons.append(QIcon('images/img3.png'))

        for i in range(self.rows):
            for j in range(self.cols):
                self.iconButtons[i][j].setGeometry(j * button_width, i * button_height, button_width, button_height)
                self.iconButtons[i][j].setIcon(self.icons[seed % self.mode])
                self.iconValues[i][j] = seed % self.mode
                seed = int(Decimal(seed) / Decimal(self.mode))
                self.iconButtons[i][j].setIconSize(self.iconButtons[i][j].size())
                self.iconButtons[i][j].clicked.connect(partial(self.on_click_icon, i, j))
        self.message = seed.to_bytes(((seed.bit_length() + 7) // 8), byteorder="big").decode("utf-8)")
        print(seed)

    def get_icons_attributes(self):
        line_value = self.line.text()

        if line_value[0] in ('2', '3', '5', '7'):
            self.mode = 2
        else:
            self.mode = 3

        self.rows = (int(line_value[1]) + int(line_value[2])) % 9
        self.cols = (int(line_value[3]) + int(line_value[4])) % 9

        return int(line_value[5::1])

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
        self.check_for_victory()

    def change_icon(self, x, y):
        future_value = (self.iconValues[x][y] + 1) % self.mode
        self.iconValues[x][y] = future_value
        self.iconButtons[x][y].setIcon(self.icons[future_value])

    def check_for_victory(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.iconValues[row][col] != 0:
                    return False
        msg = QMessageBox()
        msg.setWindowTitle('Answer for Labyrinth')
        msg.setText(self.message)
        msg.exec_()
    