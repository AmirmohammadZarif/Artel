from matplotlib.patches import Circle, PathPatch
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib.text import TextPath
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import pylab as p
import random
import math
import time


def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk)) 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

print('\033c')
def printCopyright():
    prCyan("_____________________________________________")
    prCyan("                                             ")
    prCyan(" NovinCeram Delta Robot Simulator            ")
    prCyan(" Ver Code : #2                               ")
    prCyan(" Sep, 2019                                   ")
    prCyan(" Optimized Final Version Without Serial      ")
    prCyan(" Ultimate Edition                            ")
    prCyan("_____________________________________________")
    prCyan("                                             ")

printCopyright()

time.sleep(2)
print('\033c')

DashedLines = ""

for i in range(38):
    per = translate(i,0,38,0,100)
    prCyan("◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎")
    prCyan("                                      ")
    prCyan("Code & Algorithm by Amirmohammad Zarif")
    prCyan("                                      ")
    prCyan("◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎")
    prCyan("                                      ")
    DashedLines += "◼︎"
    prLightGray(DashedLines)
    prLightGray("Loading " + str(per) + "%")
    time.sleep(0.01)
    print('\033c')
########################################################################################

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
    a = (x0*x0 + y0*y0 + z0*z0 + rf*rf - re*re - y1*y1) / (2.0*z0)
    b = (y1-y0) / z0

    # discriminant
    d = -(a + b*y1)*(a + b*y1) + rf*(b*b*rf + rf)
    if d<0:
        return [1,0] # non-existing povar.  return error, theta

    yj = (y1 - a*b - math.sqrt(d)) / (b*b + 1) # choosing outer povar
    zj = a + b*yj
    theta = math.atan(-zj / (y1-yj)) * 180.0 / pi + (180.0 if yj>y1 else 0.0)
    
    return [0,theta] # return error, theta

def lineCalc(startX, startY, startZ, angle, length):
    angle = angle + 90
    widthX = np.sin(np.deg2rad(angle)) * length
    endX = widthX + startX

    widthZ = np.cos(np.deg2rad(angle)) * length
    endZ = widthZ + startZ
    
    endY = startY
    
    check = (endY**2) + (endX**2)
    prCyan("Check " + str(angle) + "deg : " + str(check))
    prPurple("Sin" + str(angle) + " : " + str(np.sin(np.deg2rad(angle))))
    prPurple("Cos" + str(angle) + " : " + str(np.cos(np.deg2rad(angle))))
    prLightGray("lineCalc "  + str(angle) + "deg : " + str([endX,endY,endZ]))
    return [endX,endY,endZ]

def line2Calc(startX, startY, startZ, angle, length, le, width):
    angle = angle + 90

    widthX = np.cos(np.deg2rad(le)) * width
    widthY = np.sin(np.deg2rad(le)) * width
    widthZ = np.cos(np.deg2rad(angle)) * length

    endX = widthX + startX
    endY = widthY+ startY
    endZ = widthZ + startZ
    prCyan("Check : " + str([widthX,widthY,widthZ]))
    prLightGray('lineCalc #2 : ' + str([endX,endY,endZ]))
    return [endX,endY,endZ]

########################################################################################
# Trigonometric constants
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
########################################################################################

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.set_aspect('equal')

# plt.xticks(range(1,250))
# ax.axis('equal') 
# ax.set_aspect(1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(xmin = -250, xmax = 250)
ax.set_ylim(-250, 250)
ax.set_zlim(-400, bp)

########################################################################################
# Initialize Lists
VecStart_x = []
VecStart_y = []
VecStart_z = []

########
toolX = 0
toolY = 0
toolZ = 0

########
Hand1XStart = 0
Hand1YStart = 0
Hand1ZStart = 0 

Hand2XStart = 0
Hand2YStart = 0
Hand2ZStart = 0 

Hand3XStart = 0
Hand3YStart = 0
Hand3ZStart = 0 

Hand1XEnd = 0
Hand1YEnd = 0
Hand1ZEnd = 0 

Hand2XEnd = 0
Hand2YEnd = 0
Hand2ZEnd = 0 

Hand3XEnd = 0
Hand3YEnd = 0
Hand3ZEnd = 0 

#######
point1posX = np.cos(np.deg2rad(0)) * 75
point1posY = np.sin(np.deg2rad(0)) * 75
point1posZ = bp

point2posX = np.cos(np.deg2rad(120)) * 75
point2posY = np.sin(np.deg2rad(120)) * 75
point2posZ = bp

point3posX = np.cos(np.deg2rad(240)) * 75
point3posY = np.sin(np.deg2rad(240)) * 75
point3posZ = bp

######################################################################################## First Datas (0,3) 
for i in range(3):
    VecStart_x.append(0)
    VecStart_y.append(0)
    VecStart_z.append(bp)

VecEnd_x = [point1posX,point2posX,point3posX]
VecEnd_y = [point1posY,point2posY,point3posY]
VecEnd_z = [point1posZ,point2posZ,point3posZ]

########################################################################################
# Motor Num1 Start Position
VecStart_x.append(point1posX)
VecStart_y.append(point1posY)
VecStart_z.append(bp)

# Motor Num2 Start Position
VecStart_x.append(point2posX)
VecStart_y.append(point2posY)
VecStart_z.append(bp)

# Motor Num3 Start Position
VecStart_x.append(point3posX)
VecStart_y.append(point3posY)
VecStart_z.append(bp)

# Motor Tool Start Position
VecStart_x.append(toolX)
VecStart_y.append(toolY)
VecStart_z.append(toolZ)

# Hand1 Start
VecStart_x.append(Hand1XStart)
VecStart_y.append(Hand1YStart)
VecStart_z.append(Hand1ZStart)

# Hand2 Start
VecStart_x.append(Hand2XStart)
VecStart_y.append(Hand2YStart)
VecStart_z.append(Hand2ZStart)

# Hand3 Start
VecStart_x.append(Hand3XStart)
VecStart_y.append(Hand3YStart)
VecStart_z.append(Hand3ZStart)

print("Start X : ", VecStart_x)
print("Start Y : ", VecStart_y)
print("Start Z : ", VecStart_z)

########################################################################################

lineouts1 = lineCalc(point1posX,point1posY,point1posZ,135,rf)

line2Helper = lineCalc(point2posX,point2posY,point2posZ,90,rf)
lineouts2 = line2Calc(point2posX,point2posY,point2posZ,90,rf,120,line2Helper[0] - point2posX)

line3Helper = lineCalc(point3posX,point3posY,point3posZ,135,rf)
lineouts3 = line2Calc(point3posX,point3posY,point3posZ,135,rf,240,line3Helper[0] - point3posX)

########################################################################################
# Motor Num1 End Position
VecEnd_x.append(lineouts1[0])
VecEnd_y.append(lineouts1[1])
VecEnd_z.append(lineouts1[2])

# Motor Num2 End Position
VecEnd_x.append(lineouts2[0])
VecEnd_y.append(lineouts2[1])
VecEnd_z.append(lineouts2[2])

# Motor Num3 End Position
VecEnd_x.append(lineouts3[0])
VecEnd_y.append(lineouts3[1])
VecEnd_z.append(lineouts3[2])

# Motor Tool End Position
VecEnd_x.append(toolX)
VecEnd_y.append(toolY)
VecEnd_z.append(toolZ)

# Hand1 End Position
VecEnd_x.append(Hand1XEnd)
VecEnd_y.append(Hand1YEnd)
VecEnd_z.append(Hand1ZEnd)

# Hand2 End Position
VecEnd_x.append(Hand2XEnd)
VecEnd_y.append(Hand2YEnd)
VecEnd_z.append(Hand2ZEnd)

# Hand3 End Position
VecEnd_x.append(Hand3XEnd)
VecEnd_y.append(Hand3YEnd)
VecEnd_z.append(Hand3ZEnd)

print("End X : ", VecEnd_x)
print("End Y : ", VecEnd_y)
print("End Z : ", VecEnd_z)

########
p = Circle((0, 0), 75,color="r")

ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=bp, zdir="z")

########
print("Legnth : ",len(VecEnd_x))

########################################################################################################
for i in range(10):

    print("Line #" + str(i) + " : " + str([VecStart_x[i],VecStart_y[i],VecStart_z[i]]))
    ax.plot([VecStart_x[i], VecEnd_x[i]], [VecStart_y[i],VecEnd_y[i]],zs=[VecStart_z[i],VecEnd_z[i]],color="r",marker="o")

plt.grid()
########################################################################################################

Angles = []

for i in range(-42,98):
    Range = []
    for b in range(0,140 - abs(i)):
        Range.append(b)
    print(i , random.sample(Range,  1))
            


for i in range(-42,98): 
#    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ########
    print("")
    prYellow("◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎")
    prYellow("▶︎ Step : " + str(i))
    ########
    ax.cla()
    ########
    p = Circle((0, 0), 75,color="b")
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=bp, zdir="z")
    ########
#    c1 = random.sample(Range,  1)
#    c1 = c1[0]
#    print(c1)
    lineouts1 = lineCalc(point1posX,point1posY,point1posZ,25,rf)
#    c2  = random.sample(Range,  1)
#    c2 = c2[0]
    line2Helper = lineCalc(point2posX,point2posY,point2posZ,25,rf)
    lineouts2 = line2Calc(point2posX,point2posY,point2posZ,25,rf,120,line2Helper[0] - point2posX)
#    c3  = random.sample(Range,  1)
#    c3 = c3[0]
    line3Helper = lineCalc(point3posX,point3posY,point3posZ,25,rf)
    lineouts3 = line2Calc(point3posX,point3posY,point3posZ,25,rf,240,line3Helper[0] - point3posX)
    
    ########
    VecEnd_x[3] = lineouts1[0]
    VecEnd_y[3] = lineouts1[1]
    VecEnd_z[3] = lineouts1[2]

    VecEnd_x[4] = lineouts2[0]
    VecEnd_y[4] = lineouts2[1]
    VecEnd_z[4] = lineouts2[2]

    VecEnd_x[5] = lineouts3[0]
    VecEnd_y[5] = lineouts3[1]
    VecEnd_z[5] = lineouts3[2]
    ########
    ToolPosition = forward(25,25, 25)
    VecStart_x[6] = ToolPosition[1]
    VecStart_y[6] = ToolPosition[2]
    VecStart_z[6] = ToolPosition[3]
    VecEnd_x[6] = ToolPosition[1]
    VecEnd_y[6] = ToolPosition[2]
    VecEnd_z[6] = ToolPosition[3]
    ########
    VecStart_x[7] = VecEnd_x[3]
    VecStart_y[7] = VecEnd_y[3]
    VecStart_z[7] = VecEnd_z[3]

    VecStart_x[8] = VecEnd_x[4]
    VecStart_y[8] = VecEnd_y[4]
    VecStart_z[8] = VecEnd_z[4]

    VecStart_x[9] = VecEnd_x[5]
    VecStart_y[9] = VecEnd_y[5]
    VecStart_z[9] = VecEnd_z[5]

    VecEnd_x[7] = ToolPosition[1]
    VecEnd_y[7] = ToolPosition[2]
    VecEnd_z[7] = ToolPosition[3]

    VecEnd_x[8] = ToolPosition[1]
    VecEnd_y[8] = ToolPosition[2]
    VecEnd_z[8] = ToolPosition[3]

    VecEnd_x[9] = ToolPosition[1]
    VecEnd_y[9] = ToolPosition[2]
    VecEnd_z[9] = ToolPosition[3]
    for j in range(6,10):
            print(j)
            VecEnd_z[j] = bp + VecEnd_z[j]
            VecStart_z[6] = VecEnd_z[6]

    for i in range(3,10):
        prLightPurple("Line #" + str(i) + " : " + str([VecStart_x[i],VecStart_y[i],VecStart_z[i]]))
        ax.plot([VecStart_x[i], VecEnd_x[i]], [VecStart_y[i],VecEnd_y[i]],zs=[VecStart_z[i],VecEnd_z[i]],color="r",marker="o")
    prYellow("◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎")
    plt.pause(0.00001)
    time.sleep(0.01)
    print('\033c')
    

prYellow("◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎")
prYellow("  I'm Done! :)")
prYellow("◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎◼︎")
# plt.show()

