'''
Copyright 2021 Amirmohammad Zarif
Created @ 13 Jul 2021
'''
from collections import namedtuple
from math import sqrt
import DeltaRobotKinematics
import numpy as np
import serial
import utils
import time
import csv
import os
from easing_functions import *

# Get the current working directory
cwd = os.getcwd()
Log = utils.Log()

# Parameters
SHOW_VERBOSE = True

class robot:

    def __init__(self):
        self.movementSpeedFactor = 0.8

        self.theta1 = 0
        self.theta2 = 0
        self.theta3 = 0

        self.kinematic = DeltaRobotKinematics.kinematics()

        self.x = 0
        self.y = 0
        self.z = -450

        self.serial = None
        self.connected = False

        self.properties = {
            "name" : "NC Delta Robot",
            "version" : "1.2.0",
            "homePos" : {"x" : 0, "y" : 0, "z" : -440},
            "locationsFilePath" : f"{cwd}/locations.csv",
            "paletteLocationsFilePath" : f"{cwd}/paletteLocations.csv"
        }

        self.cellsMatrix = []

        self.colorsPos = {
            "1" : [72, 135, -440],
            "2" : [100, 136, -440],
            "3" : [133, 129, -440],
            "4" : [38, 130, -440],
            "5" : [38, 130, -440]
        }

        self.basePlane = -440
        self.touchPlane = -450

        self.pickTime = 0.5

        self.p_point = 2

        self.loadConfig()
         
    def getCurrentPosition(self):
        '''
        Get Current Position of head
        '''

        return [self.x, self.y, self.z]

    def setCurrentPosition(self, x, y, z):
        '''
        Get Current Position of head
        '''
        self.x = x
        self.y = y
        self.z = z
        
    def connect(self, port, baudrate):
        '''
        Creates an Instance of serial and establishes the connection
        between client and Arduino
        '''

        self.connected = True
        try:
            self.serial = serial.Serial(port, baudrate)
            Log.info(f"Connected to Artel Controller on {port} @ {baudrate}")
            time.sleep(3)

            self.setHome()
            return self.serial
        except:
            self.connected = False
            Log.error(f"Unable to connect to Artel Controller on {port} @ {port}")

    def setHome(self):
        '''
        Sets all axes to their default home values.
        Uses Properties
        '''

        homeX, homeY, homeZ = self.properties["homePos"]["x"], \
                            self.properties["homePos"]["y"], \
                            self.properties["homePos"]["z"]


        # self.goToPosition(homeX, homeY, homeZ, 0.2)
        self.serial.write(("$H\n").encode())
        self.serial.write(("$X\n").encode())
        self.serial.write(("G10 P0 L20 X70 Y70 Z70\n").encode())
        
        Log.info("Home!")
        time.sleep(2)

    def loadConfig(self):
        '''
        Loads a .csv file that contains x, y, z value of each cell in the palete
        Also fills a matrix which can be used.
        '''
        try:
            with open(self.properties["locationsFilePath"], 'r') as locationsFile:
                csvData = csv.reader(locationsFile, delimiter=',')
                for row in csvData:
                    self.cellsMatrix.append(row)

                Log.info(f'Successfully loaded configuration file : {self.properties["locationsFilePath"]}')
        except:
            Log.error(f'Failed to Load configuration file : {self.properties["locationsFilePath"]}')

    class toolHead:
        '''
        Handles suction and release.
        '''
        def pick(ser):
            try:  
                # ser.write(("M,3").encode())
                print("M03 Action")
            except:
                Log.error("Failed to pick tile")
            
        def place(ser):
            try:  
                # ser.write(("M,5").encode())
                print("M05 Action")

            except:
                Log.error("Failed to place tile")


    def getCellValueAt(self, i, j, transform=[1,1]):
        '''
        Takes the i and j indexes of the cell and returns the X, Y, Z values of that index in the palete.
        -> Transform takes a 1 x 2 matrix which is a linear transformation matrix for i and j that helps us rotate the palete.
        '''

        i = i * transform[0]
        j = j * transform[1]

        X, Y, Z = list(map(float,(self.cellsMatrix[j][i]).split()))
        return [X, Y, Z]
        
    def motionEaseQuint(self, t):
        if t < 0.5:
            return 16 * t * t * t * t * t
        p = (2 * t) - 2
        return 0.5 * p * p * p * p * p + 1

    def motionEaseCubic(self, t):
        if t < 0.5:
            return 4 * t * t * t
        p = 2 * t - 2
        return 0.5 * p * p * p + 1
    
    def motionEaseQuad(self, t):
        return -(t * (t - 2))

    def goToPosition(self, X, Y, Z, feed):
        '''
        Go to a specific position in working area.
        -> X, Y, Z of Destination position
        -> feed : in the range of [0, 100]
        '''

        interpolationSleep = 0.1
        
        steps = 2
        head_X, head_Y, head_Z = self.getCurrentPosition()
        # steps = int(sqrt(pow(X - head_X, 2) + pow(Y - head_Y, 2) + pow(Z - head_Z, 2)))
        for t in np.linspace(0, 1, steps):
            # while True:
            quint_t = self.motionEaseQuad(t)
            Log.verbose(f'\t Quint t {round(quint_t,self.p_point)}')

            Xt = head_X + ((X - head_X) * round(quint_t, 2))
            Yt = head_Y + ((Y - head_Y) * round(quint_t, 2))
            Zt = head_Z + ((Z - head_Z) * round(quint_t, 2))
            
            deltas = self.kinematic.inverse(float(Xt), float(Yt), float(Zt))

            M1 = float(deltas[1])
            M2 = float(deltas[2])
            M3 = float(deltas[3])
            Machine1 = str(int(M1))
            Machine2 = str(int(M2))
            Machine3 = str(int(M3))
            
            if(self.connected):
                self.serial.write((f"G21 G90 G00 X{Machine1} Y{Machine2} Z{Machine3} F200\n").encode())
    
                Log.info("Data Sent!")
            
            self.setCurrentPosition(Xt, Yt, Zt)

            if(SHOW_VERBOSE):
                Log.verbose(f'\t Step {round(t,self.p_point)} | X:{round(Xt,self.p_point)}, Y:{round(Yt,self.p_point)}, Z:{round(Zt,self.p_point)}')
                Log.verbose(f'\t Theta : θ₁{round(deltas[1], self.p_point)}, θ₂:{round(deltas[2],self.p_point)}, θ₃:{round(deltas[3],self.p_point)}')
                Log.verbose(f'\t Motor : M1:{round(M1,self.p_point)}, M2:{round(M2,self.p_point)}, M3:{round(M3,self.p_point)}')

            time.sleep(interpolationSleep)

            Log.info(f'\t End Pos : X{round(Xt, self.p_point)}, Y:{round(Yt, self.p_point)}, Z:{round(Zt, self.p_point)}')
                # try:
                #     if(str(self.serial.readline()) == "ok"):
                #         break
                # except:
                #     print("failed")


    def goToCellAt(self, i, j, speed, placeTile=True):
        '''
        Go to a specific position in working area.
        -> X, Y, Z of Destination position
        -> Speed : in the range of [0, 1]
        '''
        speed = self.movementSpeedFactor * speed
        
        X, Y, Z = self.getCellValueAt(int(i), int(j))
        
        if(placeTile):
            self.goToPosition(X, Y, self.basePlane, speed)
            time.sleep(1)
            self.goToPosition(X, Y, self.touchPlane, speed)
            self.toolHead.place(self.serial)
            time.sleep(1)
            self.goToPosition(X, Y, self.basePlane, speed)
        else:
            self.goToPosition(X, Y, Z, speed)

    def goToColor(self, colorName, speed, pickTile=True):
        '''
        Picks up a color from color rack by the name of the color.
        '''
        speed = self.movementSpeedFactor * speed
    
        X, Y, Z = self.colorsPos[colorName][0], self.colorsPos[colorName][1], self.basePlane
        self.goToPosition(X, Y, Z, speed)   
        
        time.sleep(1)
        self.goToPosition(X, Y, self.colorsPos[colorName][2], speed)
        if(pickTile):
            self.toolHead.pick(self.serial)

        time.sleep(self.pickTime)

        self.goToPosition(X, Y, Z, speed)