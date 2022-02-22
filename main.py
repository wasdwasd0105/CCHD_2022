# 1. Enter the patient ID
# 2. Enter the FiO2 value
# 3. Do you want to enter the MAC address ? (Yes/No) And if yes then enter the MAC address
# 4. Enter the minute time at which the nonions should start displaying and collecting the graph
# 5  While storing the data it should also append the patient ID & display and store the data

import os
curdir = os.path.dirname(os.path.realpath(__file__))

#Step 1 : To enter the patient ID and store it in a file
path = os.path.join(curdir, 'Pyqt5_ui', 'patient_id_input.py')
myCmd = 'python3 ' + path
os.system(myCmd)

#Step 2 : To enter the FiO2 value
path = os.path.join(curdir, 'Pyqt5_ui', 'fio2_num_input.py')
myCmd = 'python3 ' + path
os.system(myCmd)

#ABCD File
path = os.path.join(curdir, 'Pyqt5_ui', 'ABCD.py')
myCmd = 'python3 ' + path
os.system(myCmd)

#Step 4(Updated): Press start to move ahead
path = os.path.join(curdir, 'Pyqt5_ui', 'controller.py')
myCmd = 'python3 ' + path
os.system(myCmd)
