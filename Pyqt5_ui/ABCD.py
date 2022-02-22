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
ABCD_FILENAME = "abcd_rpi.csv"


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.stack = [2, 1]

        layout = QVBoxLayout()
        self.unlock_button = self.create_button('Unlock')
        layout.addWidget(self.unlock_button)
        self.unlock_button.pressed.connect(self.unlock)
        #self.lcd = QLCDNumber()
        #self.lcd.setDigitCount(2)
        #self.lcd.display(self.stack[0] * 10 + self.stack[1])
        #layout.addWidget(self.lcd)
        self.grid_layout = QGridLayout()
        self.locked = True
        # Attributes are (text, row, col)
        buttons = [
            (0, 4, 0),
            (1,4,1),
            (2,4,2),
            (1, 3, 0),
            (2, 3, 1),
            (3, 3, 2),
            (4, 2, 0),
            (5, 2, 1),
            (6, 2, 2),
            (7, 1, 0),
            (8, 1, 1),
            (9, 1, 2),
            (10,0,0),
            (11,0,1),
            (12,0,2)
        ]
        for text, row, col in buttons:
            button = self.create_number_button(text)
            self.grid_layout.addWidget(button, row, col, 1, 1)
        # XXX from a UI standpoint I'm worried that this button is too close
        # Press A1,A2 and so on .. look at a1 button and same everywhere
        a1_button = self.create_button('A1')
        a1_button.pressed.connect(self.input_btn_pressed_a1)
        self.grid_layout.addWidget(a1_button, 0, 0, 1, 1)

        a2_button = self.create_button('A2')
        a2_button.pressed.connect(self.input_btn_pressed_a2)
        self.grid_layout.addWidget(a2_button, 0, 1, 1, 1)

        a3_button = self.create_button('A3')
        a3_button.pressed.connect(self.input_btn_pressed_a3)
        self.grid_layout.addWidget(a3_button, 0, 2, 1, 1)

        b1_button = self.create_button('B1')
        b1_button.pressed.connect(self.input_btn_pressed_b1)
        self.grid_layout.addWidget(b1_button, 1, 0, 1, 1)

        b2_button = self.create_button('B2')
        b2_button.pressed.connect(self.input_btn_pressed_b2)
        self.grid_layout.addWidget(b2_button, 1, 1, 1, 1)

        b3_button = self.create_button('B3')
        b3_button.pressed.connect(self.input_btn_pressed_b3)
        self.grid_layout.addWidget(b3_button, 1, 2, 1, 1)

        c1_button = self.create_button('C1')
        c1_button.pressed.connect(self.input_btn_pressed_c1)
        self.grid_layout.addWidget(c1_button, 2, 0, 1, 1)

        c2_button = self.create_button('C2')
        c2_button.pressed.connect(self.input_btn_pressed_c2)
        self.grid_layout.addWidget(c2_button, 2, 1, 1, 1)

        c3_button = self.create_button('C3')
        c3_button.pressed.connect(self.input_btn_pressed_c3)
        self.grid_layout.addWidget(c3_button, 2, 2, 1, 1)

        d1_button = self.create_button('D1')
        d1_button.pressed.connect(self.input_btn_pressed_d1)
        self.grid_layout.addWidget(d1_button, 3, 0, 1, 1)

        d2_button = self.create_button('D2')
        d2_button.pressed.connect(self.input_btn_pressed_d2)
        self.grid_layout.addWidget(d2_button, 3, 1, 1, 1)

        d3_button = self.create_button('D3')
        d3_button.pressed.connect(self.input_btn_pressed_d3)
        self.grid_layout.addWidget(d3_button, 3, 2, 1, 1)

        e1_button = self.create_button('E1')
        e1_button.pressed.connect(self.input_btn_pressed_e1)
        self.grid_layout.addWidget(e1_button, 4, 0, 1, 1)

        e2_button = self.create_button('E2')
        e2_button.pressed.connect(self.input_btn_pressed_e2)
        self.grid_layout.addWidget(e2_button, 4, 1, 1, 1)

        e3_button = self.create_button('E3')
        e3_button.pressed.connect(self.input_btn_pressed_e3)
        self.grid_layout.addWidget(e3_button, 4, 2, 1, 1)

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

    def input_btn_pressed_a1(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'A1'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_a2(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'A2'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_a3(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'A3'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_b1(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'B1'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_b2(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'B2'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_b3(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'b3'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_c1(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'C1'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_c2(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'C2'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_c3(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'C3'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_d1(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'D1'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_d2(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'D2'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_d3(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'D3'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_e1(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'E1'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_e2(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'E2'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()

    def input_btn_pressed_e3(self):
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

        #fio2 = self.stack[0] * 10 + self.stack[1]
        abcd = 'E3'
        #filename = os.path.join(DATA_DIR, ABCD_FILENAME)
        filename = os.path.join(DATA_DIR,  ABCD_FILENAME)
        filename2 = os.path.join(DATA_DIR, patient_id, patient_id+'_'+ ABCD_FILENAME)
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))

        if os.path.exists(filename2):
            with open(filename2, "a") as f:
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        else:
            with open(filename2, "w") as f:
                f.write("Patient_ID,time,abcd\n")
                f.write("{},{},{}\n".format(patient_id,time, abcd))
        self.lock()
        exit()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    fio2 = MainWindow()
    fio2.show()
    sys.exit(app.exec_())