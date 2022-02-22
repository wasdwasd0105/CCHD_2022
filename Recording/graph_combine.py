import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import time

import os
import csv
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import random
from collections import deque

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


fileName = os.path.join(DATA_DIR, patient_id, patient_id + '_rpi_pleth_hand_file.csv')
fileName2 = os.path.join(DATA_DIR, patient_id, patient_id + '_rpi_pulseox_hand_file.csv')

fileName3 = os.path.join(DATA_DIR, patient_id, patient_id + '_rpi_pleth_foot_file.csv')
fileName4 = os.path.join(DATA_DIR, patient_id, patient_id + '_rpi_pulseox_foot_file.csv')

#to let the bluetooth connect and collect some data points
#time.sleep(10)

'''
#instead of making it sleep just check if the file is made so when the file is made then start the graph after a sleep of 2 sec
x = 0
y = 0
while x == 0 or y == 0:
    if os.path.exists(fileName) and x == 0:
        with open(fileName, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row1 in reader:
                if row1:
                    x = 1
                    break
        csvFile.close()
    if os.path.exists(fileName2) and y == 0:
        with open(fileName2, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row2 in reader:
                if row1:
                    y = 1
                    break
        csvFile.close()
'''
time.sleep(15)

def make_ticklabels_invisible(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        for tl in ax.get_xticklabels() + ax.get_yticklabels():
            tl.set_visible(False)


gs = GridSpec(4, 2)
# build a rectangle in axes coords
left, width = .25, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

global i
global xar
global yar
global ih
global xarh
global yarh


#all graph variables for foot

xar = deque(maxlen = 500) # forces x array to fixed sz
yar = deque(maxlen = 500) # forces y array to fixed sz
xar1 = deque(maxlen = 500) # forces x array to fixed sz
yar1 = deque(maxlen = 500) # forces y array to fixed sz
xar2 = deque(maxlen = 500) # forces x array to fixed sz
yar2 = deque(maxlen = 500) # forces y array to fixed sz
i = 0

xarh = deque(maxlen = 500) # forces x array to fixed sz
yarh = deque(maxlen = 500) # forces y array to fixed sz
xar1h = deque(maxlen = 500) # forces x array to fixed sz
yar1h = deque(maxlen = 500) # forces y array to fixed sz
xar2h = deque(maxlen = 500) # forces x array to fixed sz
yar2h = deque(maxlen = 500) # forces y array to fixed sz
ih = 0
#j = 0

fig = plt.figure()
ax1 = fig.add_subplot(412)
axr = fig.add_axes([0.5,0.75,0.5,0.25])
axl = fig.add_axes([0,0.75,0.5,0.25])

pl = patches.Rectangle(
    (left, bottom), width, height,
    fill=False, transform=axl.transAxes, clip_on=False
    )
pr = patches.Rectangle(
    (left, bottom), width, height,
    fill=False, transform=axr.transAxes, clip_on=False
    )

axr.add_patch(pr)
axl.add_patch(pl)

axr.set_xticklabels([])
axl.set_xticklabels([])

axr.axis('off')
axl.axis('off')

#all graph variable for hand
ax1h = fig.add_subplot(414)
axrh = fig.add_axes([0.5,0.25,0.5,0.25])
axlh = fig.add_axes([0,0.25,0.5,0.25])
plh = patches.Rectangle(
    (left, bottom), width, height,
    fill=False, transform=axlh.transAxes, clip_on=False
    )
prh = patches.Rectangle(
    (left, bottom), width, height,
    fill=False, transform=axrh.transAxes, clip_on=False
    )
axrh.add_patch(prh)
axlh.add_patch(plh)

axrh.set_xticklabels([])
axlh.set_xticklabels([])

axrh.axis('off')
axlh.axis('off')
#plt.suptitle("Health-Care")

def animate(i):
    #create graph
    try:
        #pull data from the file
        pullData = open(fileName,"r").read() #pleth-hand
        pullData2 = open(fileName2,"r").read() #pulse-ox-hand
        '''
        pullData3 = open(fileName3,"r").read() #pleth-hand
        pullData4 = open(fileName4,"r").read() #pulse-ox-hand
        '''
        #print('Pulling Data Successful')

        #Splitting up the data
        dataArray = pullData.split('\n')
        dataArray2 = pullData2.split('\n')
        '''
        dataArray3 = pullData3.split('\n')
        dataArray4 = pullData4.split('\n')
        '''
        #print('Splitting data successful')

        #for the big plot in the bottom
        xar.clear()
        yar.clear()



        for eachLine in dataArray:
            if len(eachLine)>1:
                row = eachLine.split(',')
                idx = 1
                for val in [x + i * 23 for x in range(1,24)]:
                    xar.append(val)
                    yar.append(int(row[idx]))
                    idx += 1
                i += 1

        ax1.clear()
        ax1.plot(xar,yar)

        #print('Plot big')
        # rescales window to create the 'sliding window' effect
        ax1.relim()
        ax1.autoscale()
        '''
        for eachLineh in dataArray3:
            if len(eachLineh)>1:
                rowh = eachLineh.split(',')
                idx = 1
                for val in [x + ih * 23 for x in range(1,24)]:
                    xarh.append(val)
                    yarh.append(int(rowh[idx]))
                    idx += 1
                ih += 1

        ax1h.clear()
        ax1h.plot(xarh,yarh)
        ax1h.relim()
        ax1h.autoscale()
        '''
        #---------------------------------------------------------------------------
        #for the two plots in row one
        xar1.clear()
        yar1.clear()
        xar2.clear()
        yar2.clear()
        '''
        xar1h.clear()
        yar1h.clear()
        xar2h.clear()
        yar2h.clear()
        '''
        for eachLine1 in dataArray2:
            if len(eachLine1) > 1:
                row1 = eachLine1.split(',')
                xar1.append(i)
                yar1.append(int(row1[5])) #SPO2
                xar2.append(i)
                yar2.append(int(row1[3])) #PAI

        axl.clear()
        axr.clear()
        '''
        for eachLine1h in dataArray4:
            if len(eachLine1h) > 1:
                row1h = eachLine1h.split(',')
                xar1h.append(ih)
                yar1h.append(int(row1h[5])) #SPO2 -  hand
                xar2h.append(ih)
                yar2h.append(int(row1h[3])) #PAI  - hand

        axlh.clear()
        axrh.clear()
        '''
        #SPO2
        axl.text(0.5*(left+right), 0.5*(bottom+top), str(yar1[-1]),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10, color='red',
            transform=axl.transAxes)
        '''
        axlh.text(0.5*(left+right), 0.5*(bottom+top), str(yar1[-1]),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, color='red',
            transform=axlh.transAxes)
        '''
        axl.text(0.75 * right, top, 'SPO2 - hand',
            horizontalalignment='right',
            verticalalignment='top',
            transform=axl.transAxes)
        '''
        axlh.text(0.75 * right, top, 'SPO2 - foot',
            horizontalalignment='right',
            verticalalignment='top',
            transform=axlh.transAxes)
        '''
        #PAI
        axr.text(0.5*(left+right), 0.5*(bottom+top), str(yar2[-1]),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10, color='red',
            transform=axr.transAxes)
        '''
        axrh.text(0.5*(left+right), 0.5*(bottom+top), str(yar2[-1]),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, color='red',
            transform=axrh.transAxes)
        '''
        axr.text(0.75 * right, top, 'PAI - hand',
            horizontalalignment='right',
            verticalalignment='top',
            transform=axr.transAxes)
        '''
        axrh.text(0.75 * right, top, 'PAI - foot',
            horizontalalignment='right',
            verticalalignment='top',
            transform=axrh.transAxes)
        '''
        axr.set_axis_off()
        axl.set_axis_off()
        #axrh.set_axis_off()
        #axlh.set_axis_off()
        #print('plots up')
        print(yar1[-1])
        print(yar2[-1])
    except:
        print('File not found')


def animateh(ih):
    #create graph
    try:
        #pull data from the file

        pullData3 = open(fileName3,"r").read() #pleth-foot
        pullData4 = open(fileName4,"r").read() #pulse-ox-foot
        axr.set_xticklabels([])
        axl.set_xticklabels([])

        axr.axis('off')
        axl.axis('off')

        #Splitting up the data

        dataArray3 = pullData3.split('\n')
        dataArray4 = pullData4.split('\n')

        #for the big plot in the bottom

        xarh.clear()
        yarh.clear()

        for eachLineh in dataArray3:
            if len(eachLineh)>1:
                rowh = eachLineh.split(',')
                idx = 1
                for val in [x + ih * 23 for x in range(1,24)]:
                    xarh.append(val)
                    yarh.append(int(rowh[idx]))
                    idx += 1
                ih += 1

        ax1h.clear()
        ax1h.plot(xarh,yarh)
        ax1h.relim()
        ax1h.autoscale()

        #---------------------------------------------------------------------------
        #for the two plots in row one

        xar1h.clear()
        yar1h.clear()
        xar2h.clear()
        yar2h.clear()


        for eachLine1h in dataArray4:
            if len(eachLine1h) > 1:
                row1h = eachLine1h.split(',')
                xar1h.append(ih)
                yar1h.append(int(row1h[5])) #SPO2 -  foot
                xar2h.append(ih)
                yar2h.append(int(row1h[3])) #PAI  - foot

        axlh.clear()
        axrh.clear()

        #SPO2

        axlh.text(0.5*(left+right), 0.5*(bottom+top), str(yar1h[-1]),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10, color='red',
            transform=axlh.transAxes)

        axlh.text(0.75 * right, top, 'SPO2 - foot',
            horizontalalignment='right',
            verticalalignment='top',
            transform=axlh.transAxes)

        #PAI

        axrh.text(0.5*(left+right), 0.5*(bottom+top), str(yar2h[-1]),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10, color='red',
            transform=axrh.transAxes)


        axrh.text(0.75 * right, top, 'PAI - foot',
            horizontalalignment='right',
            verticalalignment='top',
            transform=axrh.transAxes)

        axrh.set_axis_off()
        axlh.set_axis_off()

    except:
        print('Foot File not found')




ani = animation.FuncAnimation(fig, animate, interval=500)
anih = animation.FuncAnimation(fig, animateh, interval=500)
#make_ticklabels_invisible(plt.gcf())
plt.show()
