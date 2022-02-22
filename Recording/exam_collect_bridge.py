import time
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
        patient_id = row[1]
csvFile.close()

#getting the ABCD ID
with open(os.path.join(DATA_DIR, ABCD_FILENAME), 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        abcd_id = row[2]
csvFile.close()

patient_folder = os.path.join(DATA_DIR, patient_id)
dest_folder = os.path.join(curdir, '..', 'Data', 'tmp', 'Recorded')

file_list = sorted(os.listdir(patient_folder))
for file in file_list:
    match = file.split('_')[1]
    if (match == "interval"):
        pass
    else :
        shutil.copy(os.path.join(patient_folder, file), os.path.join(dest_folder, abcd_id + '-' + file))

os.system('python3 ' + os.path.join(curdir, '..', 'Detection', 'CCHD_detection.py'))
