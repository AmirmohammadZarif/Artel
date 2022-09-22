from matplotlib.patches import Circle, PathPatch
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib.text import TextPath
import matplotlib.pyplot as plt
from pygcode import Line
import numpy as np
import pylab as p
import pyautogui 
#import serial
import random
import math
import time

j = 0

s      = 165*2
sqrt3  = math.sqrt(3.0)
pi     = 3.141592653
sin120 = sqrt3 / 2.0
cos120 = -0.5
tan60  = sqrt3
sin30  = 0.5
tan30  = 1.0 / sqrt3
########  
e  =  24.0
f  =  75.0
re =  300.0
rf =  100.0
bp = 600
cp = 0

VecStart_x = [0]
VecStart_y = [0]
VecStart_z = [0]
VecEnd_x = [0]
VecEnd_y = [0]
VecEnd_z = [0]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.set_aspect('equal')

# plt.xticks(range(1,250))
# ax.axis('equal') 
# ax.set_aspect(1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(left = -30, right = 30)
ax.set_ylim(-30, 30)
ax.set_zlim(-400, -100)
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

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
#Machine = serial.Serial('/dev/tty.usbserial-A9OZB15P',57600)
time.sleep(1)
with open('/Users/amirmohammad/Documents/Projects/Robotics & Machine Learning/DeltaRobot/square.gcode', 'r') as fh:
    for line_text in fh.readlines():
        
        j += 1
        line = Line(line_text)
        print("I = " + str(j))
        data = str(line).split(' ')
        
        if(data[0] != ''):
            # print(data)
            # ax.cla()
            ax.set_xlim(left = -30, right = 30)
            ax.set_ylim(-30, 30)
            ax.set_zlim(-400, -100)
            data0len = len(data[0])
            data[0] = data[0][1:data0len]
            data1len = len(data[1])
            data[1] = data[1][1:data1len]
            data2len = len(data[2])
            data[2] = data[2][1:data2len]


            print('X: : ',data[0])
            print('Y: : ',data[1])
            print('Z: : ',data[2])
            
            deltas = inverse(int(data[0]),int(data[1]),int(data[2]))


            M1 = float(deltas[1])
            M2 = float(deltas[2])
            M3 = float(deltas[3])
            print('theta: : ',M1,M2,M3)


#            Head = forward(M1,M2,M3)
            M1 = int(translate(M1,-42,98,0,180))
            M2 = int(translate(M2,-49,98,0,180))
            M3 = int(translate(M3,-49,98,0,180))

            Machine1 = str(int(M1))
            Machine2 = str(int(M2))
            Machine3 = str(int(M3))
#            Machine.write("X," + Machine1 + "\n")
#            Machine.write("Y," + Machine2 + "\n")
#            Machine.write("Z," + Machine3 + "\n")
#            print("X," + Machine1)
#            print("Y," + Machine2 + "\n")
#            print("Z," + Machine3 + "\n")
            

            X = int(data[0])
            Y = int(data[1])
            Z = int(data[2])
            VecStart_x[0] = X
            VecStart_y[0] = Y
            VecStart_z[0] = Z
            VecEnd_x[0] = X
            VecEnd_y[0] = Y
            VecEnd_z[0] = Z
            print(X,Y,Z)
            

            
            
            plt.grid()
            # print(data)
            for i in range(1):
                print("Line #" + str(i) + " : " + str([VecStart_x[i],VecStart_y[i],VecStart_z[i]]))
                ax.plot([VecStart_x[i], VecEnd_x[i]], [VecStart_y[i],VecEnd_y[i]],zs=[VecStart_z[i],VecEnd_z[i]],color="r",marker="o")
            time.sleep(0.2)
            
            plt.pause(0.00001)
        
        # line.block.gcodes 
        # line.block.modal_params  
        # if line.comment:
        #     line.comment.text
