# Copyright (c) Microdev, Co. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Sending Custom GCodes to NC Delta Robot
    - Through Serial
    - From .gcode file

Requirements:
    -> configuration File
    -> locations File
"""
from tkinter import filedialog
import DeltaRobotKinematics
from pygcode import Line
import tkinter as tk
import numpy as np
# import pylab as p
import argparse
import serial
import utils
import robot
import time

# Get argument wheather to get file from dialog or not
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--path", type=str, default=-1,
	help="whether or not the file dialog should be opened")
args = vars(ap.parse_args())

# Initialize kinematic class and utils
Utils = utils.Utils()
Log = utils.Log()
kinematicClass = DeltaRobotKinematics.kinematics()

# Initialize Robot class
Robot = robot.robot()
client = Robot.connect('/dev/cu.usbmodem14201', 115200)


P0 = [0,0,-200]
P1 = [0,0,0]

steps = 20
interpolationSleep = 0.02
endingSleep = 0.5

palettebase = -243
safebase = -240

colors = [[120, 30],[120, 40],[120, 50]]
paletteCorners = [[[-127.4, 134],[129, 138.8]],[[136.9, -127.7],[30, 48]]]

colorsName = {
    "1" : "1",
    "2" : "2",
    "3" : "3"
}

#Ask for the file
root = tk.Tk()
root.withdraw()

if(args["path"] == -1): file_path = filedialog.askopenfilename()
else: file_path = args["path"]

X = 0
j = 0
time.sleep(1)

with open(file_path, 'r') as fh:
    for line_text in fh.readlines():
        time.sleep(endingSleep)
        j += 1
        line = Line(line_text)
        
        Log.info("NC GCode Line = " + str(j))
        data = str(line).split(' ')
        
        if(data[0] != ''):
            #Gcode values to python Variables and value
            #X,Y Values in Gcode
            time.sleep(1)
            #Color Rack value
            data0len = len(data[0])
            ColorIndex = data[0][1:data0len]

            #X Value : Index of the value in X Axis
            data1len = len(data[1])
            XIndex = data[1][1:data1len]

            #Y Value : Index of the value in Y Axis
            data2len = len(data[2])
            YIndex = data[2][1:data2len]
            
            #Printing X, Y, Z from Gcode
            Log.info(f'\t C: : {ColorIndex}')
            Log.info(f'\t X: : {XIndex}')
            Log.info(f'\t Y: : {YIndex}')
            
            Robot.goToColor(colorsName[str(ColorIndex)], 20)

            Robot.goToCellAt(XIndex, YIndex, 0.5)

    Robot.setHome()
