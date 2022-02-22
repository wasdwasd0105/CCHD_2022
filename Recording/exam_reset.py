import time
from datetime import datetime
import os
import sys
import csv
import shutil

curdir = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(curdir, '..', 'Data', 'Recorded')
PATIENT_DATA_FILENAME = "patient_info.csv"
FIO2_DATA_FILENAME = "fio2_rpi_file.csv"
ABCD_FILENAME = "abcd_rpi.csv"

#getting the Patient ID
with open(os.path.join(DATA_DIR, PATIENT_DATA_FILENAME), 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        print(row)
        patient_id = row[1]
csvFile.close()

patient_folder = os.path.join(DATA_DIR, patient_id)
dest_folder = os.path.join(curdir, '..', 'Data', 'tmp', 'Recorded')

file_list = sorted(os.listdir(patient_folder))
print(file_list)
for file in file_list:
    match = file.split('_')[1]
    print(match)
    if (match == "fio2"):
        pass
    else :
        os.remove(os.path.join(patient_folder, file))