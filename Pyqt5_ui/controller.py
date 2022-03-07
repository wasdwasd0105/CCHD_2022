from datetime import datetime
import os
import sys
import csv
import subprocess
import time
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLCDNumber,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.operate)
        self.timeer = 0

        layout = QVBoxLayout()
        self.unlock_button = self.create_button('Unlock')
        layout.addWidget(self.unlock_button)
        self.unlock_button.pressed.connect(self.unlock)
        
        self.grid_layout = QGridLayout()
        self.locked = True
        # Attributes are (text, row, col)

        # XXX from a UI standpoint I'm worried that this button is too close
        # together with the number buttons
        self.time_set = 0

        self.start_button = self.create_button('Start')
        self.start_button.pressed.connect(self.input_start_pressed)
        self.grid_layout.addWidget(self.start_button, 1, 1, 1, 2)

        self.interval_button = self.create_button('Set time')
        self.interval_button.pressed.connect(self.input_interval_pressed)
        self.grid_layout.addWidget(self.interval_button, 3, 1, 1, 2)

        self.stop_button = self.create_button('Reset')
        self.stop_button.pressed.connect(self.input_reset_pressed)
        self.grid_layout.addWidget(self.stop_button, 5, 1, 1, 2)

        self.stop_button = self.create_button('Stop')
        self.stop_button.pressed.connect(self.input_stop_pressed)
        self.grid_layout.addWidget(self.stop_button, 7, 1, 1, 2)

        self.patient_info = QLabel()
        self.read_patient_info()
        
        layout.addLayout(self.grid_layout)
        self.setLayout(layout)
        self.resize(300, 400)

    def operate(self):
        self.timeer -= 1
        if self.timeer > self.time_interval - 15:
            self.start_button.setText("Starting")
            return

        if self.timeer == 1:
            self.start_button.setStyleSheet('QPushButton {color: rgb(0, 255, 0);}')
            self.start_button.setText("Detecting")
        else:
            self.start_button.setStyleSheet('QPushButton {color: rgb(0, 255, 0);}')
            self.start_button.setText(str(self.timeer) + "s left")

        if self.timeer == 0:
            process_hand.kill()
            process_foot.kill()
            process_grapher.kill()
            self.timer.stop()
            global process_bridge
            global process_cchd_display
            process_bridge = subprocess.run(["python3", os.path.join(curdir, '..', 'Recording', 'exam_collect_bridge.py')])
            process_cchd_display = subprocess.Popen(["python3", os.path.join(curdir, 'CCHD_display.py')])
            self.start_button.setEnabled(True)
            self.start_button.setStyleSheet('QPushButton {color: rgb(0, 0, 255);}')
            self.start_button.setText("Continue")
            self.read_patient_info()


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
        if (self.locked):
            for i in range(self.grid_layout.count()):
                button = self.grid_layout.itemAt(i).widget()
                button.setStyleSheet('QPushButton {color: rgb(0, 0, 255);}')
            self.unlock_button.setStyleSheet('QPushButton {color: rgb(0, 0, 255);}')
            self.unlock_button.setText("Lock")
            self.locked = False
        else:
            for i in range(self.grid_layout.count()):
                button = self.grid_layout.itemAt(i).widget()
                button.setStyleSheet('QPushButton {color: rgb(255, 0, 0);}')
            self.unlock_button.setStyleSheet('QPushButton {color: rgb(255, 0, 0);}')
            self.unlock_button.setText("Unlock")
            self.locked = True

    def create_number_button(self, number):
        button = self.create_button(number)
        button.pressed.connect(lambda: self.number_btn_pressed(int(number)))
        return button


    def input_start_pressed(self):
        if self.locked:
            return
        if self.time_set == 0:
            self.input_interval_pressed()
        self.stop_button.setText("Stop")
        self.timeer = self.time_interval
        self.timer.start(1000)
        self.start_button.setEnabled(False)
        global process_hand 
        global process_foot
        global process_grapher
        process_hand = subprocess.Popen(["python3", os.path.join(curdir, '..', 'Recording', 'bluepy_nonin_3150_collect_foot.py')])
        process_foot = subprocess.Popen(["python3", os.path.join(curdir, '..', 'Recording', 'bluepy_nonin_3150_collect_hand.py')])
        process_grapher = subprocess.Popen(["python3", os.path.join(curdir, '..', 'Recording', 'graph_combine.py')])        
       
    def input_reset_pressed(self):
        if self.locked:
            return
        self.timer.stop()
        try:
            process_hand.kill()
            process_foot.kill()
            process_grapher.kill()
            process_bridge.kill()
        except:
            pass

        reply = QMessageBox.question(self, 'Reset option', 'Keep current data?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes: 
            subprocess.run(["python3", os.path.join(curdir, '..', 'Recording', 'exam_reset.py')])
        
        subprocess.run(["python3", os.path.join(curdir, 'ABCD.py')])
        
        self.read_patient_info()
        self.start_button.setEnabled(True)
        self.start_button.setStyleSheet('QPushButton {color: rgb(0, 0, 255);}')
        self.start_button.setText("Start")

        
    
    def input_stop_pressed(self):
        if self.locked:
            return
        self.timer.stop()
        try:
            process_hand.kill()
            process_foot.kill()
            process_grapher.kill()
            process_bridge.kill()
            
        except:
            pass

        self.start_button.setEnabled(True)
        self.start_button.setText("Stopped")

    def input_interval_pressed(self):
        subprocess.run(["python3", os.path.join(curdir, 'exam_interval_input.py')])
        filename = os.path.join(DATA_DIR, "interval_rpi.csv")
        with open(filename, "r") as f:
                time_interval = f.readline()
        self.time_interval = int(time_interval)
        self.interval_button.setText("Timer: " + str(self.time_interval) + "mins")
        self.time_interval = self.time_interval*60 + 15
        self.time_set = 1

        pass

    def read_patient_info(self):
        #getting the Patient ID
        with open(os.path.join(DATA_DIR, PATIENT_DATA_FILENAME), 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                patient_id = row[1]
        self.patient_id = patient_id
        csvFile.close()

        #getting the ABCD ID
        with open(os.path.join(DATA_DIR, ABCD_FILENAME), 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                abcd_id = row[2]
        self.abcd_id = abcd_id
        csvFile.close()

        self.patient_info.setText(self.patient_id + "  " + self.abcd_id)
        self.patient_info.setAlignment(Qt.AlignCenter)
        self.patient_info.setFont(QFont('Arial', 30))
        self.grid_layout.addWidget(self.patient_info, 0, 1, 1, 2)      
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fio2 = MainWindow()
    fio2.setWindowTitle('CCHD Controller')
    fio2.show()
    sys.exit(app.exec_())
