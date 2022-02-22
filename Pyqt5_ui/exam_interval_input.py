#Code for inputting the patient ID

from datetime import datetime
import os
import sys
import csv

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLCDNumber,
    QPushButton,
    QVBoxLayout,
    QWidget
)
curdir = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(curdir, '..', 'Data', 'Recorded')
TIME_FILENAME = "interval_rpi.csv"


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.stack = [0, 0, 0, 0, 0, 0]

        layout = QVBoxLayout()
        self.unlock_button = self.create_button('Unlock')
        layout.addWidget(self.unlock_button)
        self.unlock_button.pressed.connect(self.unlock)
        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(6)
        self.lcd.display(self.stack[0] * 100000 + self.stack[1] * 10000 + self.stack[2] * 1000 + self.stack[3] * 100 + self.stack[4] * 10 + self.stack[5])
        layout.addWidget(self.lcd)
        self.grid_layout = QGridLayout()
        self.locked = True
        # Attributes are (text, row, col)
        buttons = [
            (0, 3, 0),
            (1, 2, 0),
            (2, 2, 1),
            (3, 2, 2),
            (4, 1, 0),
            (5, 1, 1),
            (6, 1, 2),
            (7, 0, 0),
            (8, 0, 1),
            (9, 0, 2),
        ]
        for text, row, col in buttons:
            button = self.create_number_button(text)
            self.grid_layout.addWidget(button, row, col, 1, 1)
        
        n_button = self.create_button('Confirm')
        n_button.pressed.connect(self.input_btn_pressed_c)
        self.grid_layout.addWidget(n_button, 3, 2, 1, 1)        

        layout.addLayout(self.grid_layout)
        self.setLayout(layout)
        self.resize(700, 400)

    def create_button(self, text):
        button = QPushButton()
        button.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(27)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setStyleSheet("QPushButton {color: rgb(255, 0, 0);}")
        button.setText(str(text))
        return button

    def unlock(self):
        for i in range(self.grid_layout.count()):
            button = self.grid_layout.itemAt(i).widget()
            button.setStyleSheet('QPushButton {color: rgb(0, 0, 255);}')
        self.unlock_button.setStyleSheet('QPushButton {color: rgb(0, 0, 255);}')
        self.locked = False

    def lock(self):
        for i in range(self.grid_layout.count()):
            button = self.grid_layout.itemAt(i).widget()
            button.setStyleSheet('QPushButton {color: rgb(255, 0, 0);}')
        self.unlock_button.setStyleSheet('QPushButton {color: rgb(255, 0, 0);}')
        self.locked = True

    def create_number_button(self, number):
        button = self.create_button(number)
        button.pressed.connect(lambda: self.number_btn_pressed(int(number)))
        return button

    def number_btn_pressed(self, number):
        if self.locked:
            return
        self.stack.pop(0)
        self.stack.append(number)
        self.lcd.display(self.stack[0] * 100000 + self.stack[1] * 10000 + self.stack[2] * 1000 + self.stack[3] * 100 + self.stack[4] * 10 + self.stack[5])

    def input_btn_pressed_c(self):
        if self.locked:
            return
        #getting the Patient ID
        patient_interval = self.stack[0] * 100000 + self.stack[1] * 10000 + self.stack[2] * 1000 + self.stack[3] * 100 + self.stack[4] * 10 + self.stack[5]
        patient_interval = str(patient_interval)
        
        filename = os.path.join(DATA_DIR, TIME_FILENAME)

        with open(filename, "w") as f:
                f.write("{}\n".format(patient_interval))

        self.lock()
        exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    patient = MainWindow()
    patient.show()
    sys.exit(app.exec_())
