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
PATIENT_DATA_FILENAME = "patient_info.csv"
FIO2_DATA_FILENAME = "fio2_rpi_file.csv"


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.stack = [2, 1]

        layout = QVBoxLayout()
        self.unlock_button = self.create_button('Unlock')
        layout.addWidget(self.unlock_button)
        self.unlock_button.pressed.connect(self.unlock)
        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(2)
        self.lcd.display(self.stack[0] * 10 + self.stack[1])
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
        # XXX from a UI standpoint I'm worried that this button is too close
        # together with the number buttons
        eq_button = self.create_button('Input FiO2')
        eq_button.pressed.connect(self.input_btn_pressed)
        self.grid_layout.addWidget(eq_button, 3, 1, 1, 2)

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
        self.lcd.display(self.stack[0] * 10 + self.stack[1])

    def input_btn_pressed(self):
        if self.locked:
            return
        #getting the Patient ID
        with open(os.path.join(DATA_DIR, PATIENT_DATA_FILENAME), 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                print(row)
        patient_id = row[1]
        csvFile.close()
        #creating directory with patient_id inside data
        dirName = os.path.join(DATA_DIR,  patient_id)
        try:
            # Create target Directory
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ") 
        except FileExistsError:
            print("Directory " , dirName ,  " already exists")

        fio2 = self.stack[0] * 10 + self.stack[1]
        #filename = os.path.join(DATA_DIR, FIO2_DATA_FILENAME)
        filename = os.path.join(DATA_DIR,  FIO2_DATA_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id + '_' + FIO2_DATA_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, fio2))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,fio2\n")
                f.write("{},{},{}\n".format(patient_id,time, fio2))
        
        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, fio2))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,fio2\n")
                f.write("{},{},{}\n".format(patient_id,time, fio2))
        self.lock()
        exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fio2 = MainWindow()
    fio2.show()
    sys.exit(app.exec_())
