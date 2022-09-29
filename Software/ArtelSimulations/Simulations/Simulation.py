from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import mpl_toolkits.mplot3d.art3d as art3d

def lineCalc(startX, startY, startZ, angle, length):
    
    widthX = np.sin(np.deg2rad(angle)) * length
    endX = widthX + startX
    print(round(endX))

    widthZ = np.cos(np.deg2rad(angle)) * length
    endZ = widthZ + startZ
    print(round(endZ))
    
    endY = startY
    # Checking that the result are ok!
    check = (endY**2) + (endX**2)
    print("Check",check)
    return [endX,endY,endZ]

def line2Calc(startX, startY, startZ, angle, length, le, width):
    

    widthX = np.cos(np.deg2rad(le)) * width
    widthY = np.sin(np.deg2rad(le)) * width
    widthZ = np.cos(np.deg2rad(angle)) * length

    

    
    


    endX = widthX + startX
    endY = widthY+ startY
    endZ = widthZ + startZ
    
    return [endX,endY,endZ]
    
e  =  24.0
f  =  75.0
re =  300.0
rf =  100.0
bp = 400
cp = 0

# Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize Lists
VecStart_x = []
VecStart_y = []
VecStart_z = []



point1posX = np.cos(np.deg2rad(0)) * 75
point1posY = np.sin(np.deg2rad(0)) * 75
point1posZ = bp

point2posX = np.cos(np.deg2rad(120)) * 75
point2posY = np.sin(np.deg2rad(120)) * 75
point2posZ = bp

point3posX = np.cos(np.deg2rad(240)) * 75
point3posY = np.sin(np.deg2rad(240)) * 75
point3posZ = bp

######## 
for i in range(3):
    VecStart_x.append(0)
    VecStart_y.append(0)
    VecStart_z.append(bp)

VecEnd_x = [point1posX,point2posX,point3posX]
VecEnd_y = [point1posY,point2posY,point3posY]
VecEnd_z = [point1posZ,point2posZ,point3posZ]
######## 

VecStart_x.append(point2posX)
VecStart_y.append(point2posY)
VecStart_z.append(bp)



lineouts1 = lineCalc(VecStart_x[3],VecStart_y[3],VecStart_z[3],135,rf)
lineouts2 = line2Calc(VecStart_x[3],VecStart_y[3],VecStart_z[3],135,rf,120,lineouts1[0] - point2posX)

VecEnd_x.append(lineouts2[0])
VecEnd_y.append(lineouts2[1])
VecEnd_z.append(lineouts2[2])

print()



# Draw a circle on the x=0 'wall'
p = Circle((0, 0), 75)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=bp, zdir="z")

# Draw a Line
for i in range(4):
    ax.plot([VecStart_x[i], VecEnd_x[i]], [VecStart_y[i],VecEnd_y[i]],zs=[VecStart_z[i],VecEnd_z[i]],color="r",marker="o")
    
ax.set_xlim(-150, 150)
ax.set_ylim(-150, 150)
ax.set_zlim(0, bp)

plt.show()

