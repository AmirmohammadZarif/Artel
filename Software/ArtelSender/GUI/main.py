import tkinter as tk
import tkinter.ttk as ttk
import serial.tools.list_ports
import serial
import time
import math
import pygame
import sys
import pandas as pd
from tabulate import tabulate

# Initalizing Machine values and parameters required in UI
Machine = None
Connected = None
port = None
step = 1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5
 
# Offset 
GRID_OFF_TOP = 10
GRID_OFF_LEFT = 380

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
grid_Width = 8
grid_Height = 8
for row in range(grid_Height):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(grid_Width):
        grid[row].append(0)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[0][0] = 1

# Initalizing XYZ origins and Variables
X = 0
Y = 0
Z = -190

# Initializing ROW and COL values of Index selector, 1 based matrix index
ROW = 1
COL = 1
l_ROW = 1
l_COL = 1
MatrixRows = grid_Height
MatrixCols = grid_Width

# Variables to check up limit and down limit is occured
UpLimit = False
DownLimit = False

# Colored Printing on output
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))

# Initalizing the fundamentals of math values and variables
# - Used in kinematics 
# - Don't change these values
sqrt3  = math.sqrt(3.0)
pi     = 3.141592653
sin120 = sqrt3 / 2.0
cos120 = -0.5
tan60  = sqrt3
sin30  = 0.5
tan30  = 1.0 / sqrt3


# Initializing Physical Parameters
# - rf : Distance from motor shaft to elbow
# - f  : Base radius - Distance from center of machine base to center of each motor shaft. 
#         More than likely this is the middle of the side of a triangle, NOT the corner.
# - re : Distrance from elbow to the wrist
# - e : Distance from wrists to the center of the hand
# - b : Base to floor distance
j  = 0
s  = 165 * 2
e  =  40.0
f  =  50.0
re =  270.0 # 275.5
rf =  110.0
bp = 400
cp = 0


# Connect to machine
time.sleep(1)
Machine = None
Connected = True
Port = '/dev/cu.usbmodem14201'
try:
    Machine = serial.Serial(Port, 57600)
    time.sleep(0.2)
    # Machine.write(("C," + "0" + "\n").encode())
    time.sleep(0.2)
    Machine.write(("H," + "0" + "\n").encode())
    print("Successfully Connected to" + Port)
    print(serial.readline())
except:
    Connected = False
    print("Arduino not found !")

time.sleep(1)

pygame.init()

# Set the width and height of the screen [width, height]
size = [700, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("DeltaRobot")
REFRESH_RATE = 20

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Game Loop
done = False
clock = pygame.time.Clock()

# Mapping the values from a range to another range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

# Kinematics
# - Forward and Inverse and reverse included
def forward(theta1, theta2, theta3):
    x0 = 0.0
    y0 = 0.0
    z0 = 0.0
    
    t = (f-e) * tan30 / 2.0
    dtr = pi / 180.0
    
    theta1 *= dtr
    theta2 *= dtr
    theta3 *= dtr
    
    y1 = -(t + rf*math.cos(theta1) )
    z1 = -rf * math.sin(theta1)
    
    y2 = (t + rf*math.cos(theta2)) * sin30
    x2 = y2 * tan60
    z2 = -rf * math.sin(theta2)
    
    y3 = (t + rf*math.cos(theta3)) * sin30
    x3 = -y3 * tan60
    z3 = -rf * math.sin(theta3)
    
    dnm = (y2-y1)*x3 - (y3-y1)*x2
    
    w1 = y1*y1 + z1*z1
    w2 = x2*x2 + y2*y2 + z2*z2
    w3 = x3*x3 + y3*y3 + z3*z3
    
    # x = (a1*z + b1)/dnm
    a1 = (z2-z1)*(y3-y1) - (z3-z1)*(y2-y1)
    b1= -( (w2-w1)*(y3-y1) - (w3-w1)*(y2-y1) ) / 2.0
    
    # y = (a2*z + b2)/dnm
    a2 = -(z2-z1)*x3 + (z3-z1)*x2
    b2 = ( (w2-w1)*x3 - (w3-w1)*x2) / 2.0
    
    # a*z^2 + b*z + c = 0
    a = a1*a1 + a2*a2 + dnm*dnm
    b = 2.0 * (a1*b1 + a2*(b2 - y1*dnm) - z1*dnm*dnm)
    c = (b2 - y1*dnm)*(b2 - y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - re*re)
    
    # discriminant
    d = b*b - 4.0*a*c
    if d < 0.0:
        return [1,0,0,0] # non-existing povar. return error,x,y,z
    
    z0 = -0.5*(b + math.sqrt(d)) / a
    x0 = (a1*z0 + b1) / dnm
    y0 = (a2*z0 + b2) / dnm

    return [0,x0,y0,z0]

def angle_yz(x0, y0, z0, theta=None):
    y1 = -0.5*0.57735*f # f/2 * tg 30
    y0 -= 0.5*0.57735*e # shift center to edge
    # z = a + b*y
    a = (x0*x0 + y0*y0 + z0*z0 + rf * rf - re*re - y1*y1) / (2.0*z0)
    b = (y1-y0) / z0

    # discriminant
    d = -(a + b*y1)*(a + b*y1) + rf * (b*b*rf + rf)
    if d<0:
        return [1,0] # non-existing povar.  return error, theta

    yj = (y1 - a*b - math.sqrt(d)) / (b*b + 1) # choosing outer povar
    zj = a + b*yj
    theta = math.atan(-zj / (y1-yj)) * 180.0 / pi + (180.0 if yj>y1 else 0.0)
    
    return [0,theta] # return error, theta

def inverse(x0, y0, z0):
    theta1 = 0
    theta2 = 0
    theta3 = 0
    status = angle_yz(x0,y0,z0)

    if status[0] == 0:
        theta1 = status[1]
        status = angle_yz(x0*cos120 + y0*sin120,
                                   y0*cos120-x0*sin120,
                                   z0,
                                   theta2)
    if status[0] == 0:
        theta2 = status[1]
        status = angle_yz(x0*cos120 - y0*sin120,
                                   y0*cos120 + x0*sin120,
                                   z0,
                                   theta3)
    theta3 = status[1]

    return [status[0],theta1,theta2,theta3]

# Button events
def up(x,y,z,step,axis,ser):

    global X
    global Y
    global Z
    global Connected
    global UpLimit
    
    l_X = X
    l_Y = Y
    l_Z = Z  

    f_X = X * 1.1
    f_Y = Y * 1.1
    f_Z = Z

    print(f_X, f_Y, f_Z)
    if(axis == "X"):
        f_X += step
    elif(axis == "Y"):
        f_Y += step
    elif(axis == "Z"):
        f_Z += step
    
    
    error = 25
    factor = abs(f_X / 170)
    d_Z = error * factor
    print("Delta Z",d_Z)
    print("Final Value",f_Z + min(d_Z,error))

    deltas = inverse(int(f_X),int(f_Y),int(f_Z + min(d_Z,error)))

    # and not(int(deltas[1]) < -45 or int(deltas[2]) < -45 or int(deltas[3]) < -45)
    if(not(int(deltas[1]) > 65 or int(deltas[2]) > 65 or int(deltas[3]) > 65) and not(int(deltas[1]) < -50 or int(deltas[2]) < -50 or int(deltas[3]) < -50)):
        if(axis == "X"):
            X += step
        elif(axis == "Y"):
            Y += step
        elif(axis == "Z"):
            Z += step
    else:
        l_X = X
        l_Y = Y
        l_Z = Z
        sys.stdout.write('\a')
        sys.stdout.flush()

    # if(axis == "X"):
    #     X += step
    # elif(axis == "Y"):
    #     Y += step
    # elif(axis == "Z"):
    #     Z += step
   

    # deltas = inverse(int(f_X),int(f_Y),int(f_Z))
    
 
    # print(int(X))
    prCyan('theta: : ' + str(int(deltas[1])) + " " + str(int(deltas[2])) + " " + str(int(deltas[3])))
    
    M1 = str(float(round(deltas[1], 2)))
    M2 = str(float(round(deltas[2], 2)))
    M3 = str(float(round(deltas[3], 2)))
    print(forward(int(deltas[1]),int(deltas[2]),int(deltas[3])))

    UpLimit = False
    print(int(deltas[1]),int(deltas[2]),int(deltas[3]))

    
    if(deltas[0] == 0):
        try:
            ser.write(("X," + M1 + "\n").encode())
            ser.write(("Y," + M2 + "\n").encode())
            ser.write(("Z," + M3 + "\n").encode())
        except:
            print("Failed to send data.")

        UpLimit = True
        print(deltas[0])
        print(M1,M2,M3, "Sent")
   
    # posText.set("X : " + str(X) + ", Y : " + str(Y) + ", Z : " + str(Z))


def down(x,y,z,step,axis,ser):

    global X
    global Y
    global Z
    global Connected
    global DownLimit

    if(axis == "X"):
        X -= step
    elif(axis == "Y"):
        Y -= step
    elif(axis == "Z"):
        Z -= step

    deltas = inverse(int(X),int(Y),int(Z))
    print(int(X))
    prCyan('\n \t theta: : ' + str(int(deltas[1])) + " " + str(int(deltas[2])) + " " + str(int(deltas[3])))
    
    M1 = str(float(round(deltas[1], 2)))
    M2 = str(float(round(deltas[2], 2)))
    M3 = str(float(round(deltas[3], 2)))
    DownLimit = False
    if(deltas[0] == 0):
        try:
            ser.write(("X," + M1 + "\n").encode())
            ser.write(("Y," + M2 + "\n").encode())
            ser.write(("Z," + M3 + "\n").encode())
        except:
            print("Failed to send data.")
        DownLimit = True
        print(deltas[0])
        print(M1,M2,M3, "Sent")
        
    # posText.set("X : " + str(X) + ", Y : " + str(Y) + ", Z : " + str(Z))
    
def suction(ser):
    try:
        ser.write(("M,3 \n").encode())
    except:
        print("Failed to send suction command.")

def release(ser):
    try:
        ser.write(("M,5 \n").encode())
    except:
        print("Failed to send suction command.")

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 30)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, WHITE)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 30

    def indent(self):
        self.x += 20

    def unindent(self):
        self.x -= 20

def setHome(X,Y):
    print("Go Home")


# Get ready to print
textPrint = TextPrint()

# Read CSV File
matrixData = pd.read_csv('/Users/amirmohammad/Documents/Business/Projects/DeltaRobot/Main Project/config/locations_tmp.csv', header=None)

while done==False:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            setHome()
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # # Change the x/y screen coordinates to grid coordinates
            # print(pos)
            # column = (pos[0] - GRID_OFF_LEFT) // (WIDTH + MARGIN) 
            # row = (pos[1] - GRID_OFF_TOP) // (HEIGHT + MARGIN)
            # # Set that location to one
            # grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)

    # Drawing code
    screen.fill(BLACK)
    textPrint.reset()
    
    # Update the grid and set any item other than cursor to zero
    for row in range(MatrixRows):
        for column in range(MatrixCols):
            if(grid[row][column] != 2):
                grid[row][column] = 0
            
    if(grid[ROW - 1][COL - 1] != 2):
        grid[ROW - 1][COL - 1] = 1
    
    # Draw the grid
    for row in range(MatrixRows):
        for column in range(MatrixCols):
            color = WHITE
            if grid[row][column] == 1:
                color = RED
            elif grid[row][column] == 2:
                color = GRAY

            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN + GRID_OFF_LEFT,
                              (MARGIN + HEIGHT) * row + MARGIN + GRID_OFF_TOP,
                              WIDTH,
                              HEIGHT])
    
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()

    '''
    Axis 3 : X 
    Axis 4 : Y
    Axis 1 : Z
    Axis 5 : Suction
    Axis 2 : Suction
    Button 5 : home
    Button 8 : step up
    Button 9 : step down
    '''
    # for i in range(joystick_count):
    #     joystick = pygame.joystick.Joystick(i)
    #     joystick.init()
    #     # for j in range(pygame.joystick.Joystick(i).get_numaxes()):
    #     #     print("Axis",j,round(joystick.get_axis(j), 2))

    #     for j in range(pygame.joystick.Joystick(i).get_numbuttons()):
    #         print("Button",j,joystick.get_button(j))
    
    for i in range(joystick_count):
        # Initialize joystick 
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # Robot Teleoperation Buttons and Axis
        joystickXValue = round(joystick.get_axis(3), 2)
        joystickYValue = round(joystick.get_axis(2), 2)
        joystickZValue = round(joystick.get_axis(1), 2)
        joystickSuctionValue = round(joystick.get_axis(5), 2)
        homeButton = joystick.get_button(5)

        # Matrix Navigation Buttons
        setCellButton = joystick.get_button(0)
        goToCellButton = joystick.get_button(2)
        nextCellButton = joystick.get_button(3)
        saveButton = joystick.get_button(1)

        upButton = joystick.get_button(11)
        downButton = joystick.get_button(12)
        rightButton = joystick.get_button(14)
        leftButton = joystick.get_button(13)


        # Print Data on Screen
        textPrint.print(screen,"Step Axis")
        textPrint.indent()
        textPrint.print(screen,"X Step " + str(round(joystickXValue,2)))
        textPrint.print(screen,"Y Step " + str(round(joystickYValue,2)))
        textPrint.print(screen,"Z Step " + str(round(joystickZValue,2)))
        textPrint.unindent()

        textPrint.print(screen,"Position")
        textPrint.indent()
        textPrint.print(screen,"X " + str(round(X,2)))
        textPrint.print(screen,"Y " + str(round(Y,2)))
        textPrint.print(screen,"Z " + str(round(Z,2)))
        textPrint.unindent()

        textPrint.print(screen,"Matrix Navigation Buttons")
        textPrint.indent()
        textPrint.print(screen,"UP " + str(upButton))
        textPrint.print(screen,"DOWN " + str(downButton))
        textPrint.print(screen,"RIGHT " + str(rightButton))
        textPrint.print(screen,"LEFT " + str(leftButton))
        textPrint.unindent()

        textPrint.print(screen,"Matrix Selected Index")
        textPrint.indent()
        textPrint.print(screen,"ROW " + str(ROW))
        textPrint.print(screen,"COL " + str(COL))
        
        selectedIndex = (matrixData[COL - 1][ROW - 1]).split(' ')

        selectedIndex_X = selectedIndex[0]
        selectedIndex_Y = selectedIndex[1]
        selectedIndex_Z = selectedIndex[2]

        table = matrixData.to_markdown()
        # print(table)

        textPrint.print(screen,"X Value " + str(selectedIndex_X))
        textPrint.print(screen,"Y Value " + str(selectedIndex_Y))
        textPrint.print(screen,"Z Value " + str(selectedIndex_Z))
    
        textPrint.unindent()        

        flowStatus = "Release"
        #Fix errors
        if(joystickXValue != 0):
            up(X,Y,Z,joystickXValue * 2, "X" , Machine)
        elif(joystickZValue != 0):
            up(X,Y,Z,joystickZValue * -2, "Z" , Machine)
        elif(joystickYValue != 0):
            up(X,Y,Z,joystickYValue * -2, "Y" , Machine)
        elif(joystickSuctionValue > 0):
            suction(Machine)
            flowStatus = "Suction "
        elif(joystickSuctionValue <= 0):
            release(Machine)
            flowStatus = "Release "

        textPrint.print(screen, "Toggles")
        textPrint.indent()
        textPrint.print(screen, flowStatus + str(joystickSuctionValue))
        textPrint.print(screen, "Home " + str(homeButton))
        textPrint.unindent()

        # Buttons pressed
        if(homeButton == 1):
            Machine.write(("H," + "0" + "\n").encode())
            X = 0
            Y = 0
            Z = -190

        if(downButton == 1):
            if(ROW < MatrixRows):
                ROW = ROW + 1
                time.sleep(0.1)
                l_ROW = ROW 

        if(upButton == 1):
            if(ROW > 1):
                ROW = ROW - 1
                time.sleep(0.1)
                l_ROW = ROW
                
        if(rightButton == 1):
            if(COL < MatrixCols):
                COL = COL + 1
                time.sleep(0.1)
                l_COL = COL
            
        if(leftButton == 1):
            if(COL > 1):
                COL = COL - 1
                time.sleep(0.1)
                l_COL = COL

        if(setCellButton == 1):
            matrixData[COL - 1][ROW - 1] = str(round(X,2)) + " " + str(round(Y,2)) + " " + str(round(Z,2))
            grid[ROW - 1][COL - 1] = 2

        if(goToCellButton == 1):
            print("Go to")
            X = int(float(selectedIndex_X))
            Y = int(float(selectedIndex_Y))
            Z = int(float(selectedIndex_Z))
            up(selectedIndex_X,selectedIndex_Y,selectedIndex_Z,0, "X" , Machine)
            time.sleep(0.5)
        
        if(saveButton == 1): 
            print("Changes Saved")
            matrixData.to_csv('locations_tmp.csv',index=False,header=None)
            time.sleep(0.5)

        if(nextCellButton == 1):
            matrixData[COL - 1][ROW - 1] = str(round(X,2)) + " " + str(round(Y,2)) + " " + str(round(Z,2))
            grid[ROW - 1][COL - 1] = 2
            if(COL < MatrixCols):
                COL = COL + 1
            else:
                if(ROW < MatrixRows):
                    COL = 1
                    ROW = ROW + 1
            time.sleep(0.2)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    clock.tick(REFRESH_RATE)

pygame.quit()
