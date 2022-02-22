import csv
import datetime
import os
import time
import struct

from datetime import datetime
from bluepy.btle import DefaultDelegate, Peripheral
import configparser

NONIN_SERVICE_UUID = '46a970e00d5f11e28b5e0002a5d5c51b'
PULSE_OX_CHAR_UUID = '34e2786376ff4f8e96f19e3993aa6199'
PLETH_CHAR_UUID = 'ec0a883a4d2411e7b114b2f933d5fe66'
PULSE_OX_CHAR_UUID = '0aad7ea00d6011e28e3c0002a5d5c51b'

curdir = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(curdir, '..', 'Data', 'Recorded')
PATIENT_DATA_FILENAME = "patient_info.csv"
FIO2_DATA_FILENAME = "fio2_rpi_file.csv"
ABCD_FILENAME = "abcd_rpi.csv"

config = configparser.ConfigParser()
config.read(os.path.join(curdir, '..', 'Config', 'config.ini'))
MAC =  config['Nonin']['Hand_MAC']

class Delegate(DefaultDelegate):
    def __init__(self):
        
        #getting the Patient ID
        with open(os.path.join(DATA_DIR, PATIENT_DATA_FILENAME), 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                print(row)
        patient_id = row[1]
        csvFile.close()

        #findng abcd value here
        with open(os.path.join(DATA_DIR, patient_id, patient_id + '_abcd_rpi.csv'), 'r') as csvFile1:
            reader = csv.reader(csvFile1)
            for row in reader:
                print(row)
        abcd = row[2]
        csvFile1.close()

        PLETH_FILE = os.path.join(DATA_DIR, patient_id, patient_id + '_rpi_pleth_hand_file.csv')
        PULSE_OX_FILE = os.path.join(DATA_DIR, patient_id, patient_id + '_rpi_pulseox_hand_file.csv')

        self.abcd = abcd
        self.patient_id = patient_id
        self.PLETH_FILE = PLETH_FILE
        self.PULSE_OX_FILE = PULSE_OX_FILE

    def handleNotification(self, cHandle, data):
        time2 = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
        print(time2)

        if os.path.exists(self.PULSE_OX_FILE):
            f1 = open(self.PULSE_OX_FILE, 'a')
        else:
            f1 = open(self.PULSE_OX_FILE, 'w')

        if os.path.exists(self.PLETH_FILE):
            f2 = open(self.PLETH_FILE, 'a')
        else:
            f2 = open(self.PLETH_FILE, 'w')

        pulse_ox_writer = csv.writer(f1)
        pleth_writer = csv.writer(f2)

        if cHandle == 29:
            try:
                # the output format here is length:
                # 0: (# bytes),
                # 1: status (is defined by different sub-bits)
                # 2: voltage
                # 3-4: pulse amplitude index
                # 5-6: counter
                # 7: SpO2
                # 8-9: pulse rate
                #
                # The ? is left for bytes we are currently unable to exploit
                output = struct.unpack('>b?bhhbh', data) # >b?b??hbh
                output = list(output)
                output.append(time2)
                output.append(self.abcd)
                print(output)
                pulse_ox_writer.writerow(output)

                f1.flush()

            except:
                pass
        elif cHandle == 41:
            try:
                print('writing pleth here')
                output = struct.unpack('>b{}h'.format('H'*25), data)
                output = list(output)
                output.append(time2)
                output.append(self.abcd)
                print(output)
                pleth_writer.writerow(output)
                f2.flush()

            except:
                # print('in except')
                pass


def connect():
    # If can't connect then continually retry
    while True:
        try:
            print('b4 Peripheral')
            dev = Peripheral(MAC)
            print('after Peripheral')
            dev.setMTU(60)

            dev.setDelegate(Delegate())
            service = dev.getServiceByUUID(NONIN_SERVICE_UUID)
            char1 = service.getCharacteristics(PULSE_OX_CHAR_UUID)[0]
            char2 = service.getCharacteristics(PLETH_CHAR_UUID)[0]

            return dev, char1, char2
        except Exception as err:
            # this disconnect logic needs to be overhauled for the 3150
            print("Connection Error: {}".format(err))
            time.sleep(1)


def get_data(dev, pulse_ox_char, pleth_char):
    # The +1 means to only get notifications from the notify service
    dev.writeCharacteristic(pulse_ox_char.valHandle+1, b'\x01\x00')
    dev.writeCharacteristic(pleth_char.valHandle+1, b'\x01\x00')
    while True:
        if dev.waitForNotifications(1.0):
            print('waitForNotifications==true')
            continue
        else:

            dev.writeCharacteristic(pulse_ox_char.valHandle+1, b'\x01\x00')
            dev.writeCharacteristic(pleth_char.valHandle+1, b'\x01\x00')
            # print('pulse_ox_char.valHandle ', pulse_ox_char.valHandle)
            # print('pleth_char.valHandle ', pleth_char.valHandle)

def main():

    while True:
        # if not os.stat(PLETH_FILE).st_size == 0

        dev, pulse_ox_char, pleth_char = connect()
        try:
            get_data(dev, pulse_ox_char, pleth_char)
            print('<---end get data!!!--->')

        except:
            time.sleep(1)

if __name__ == '__main__':
    main()
