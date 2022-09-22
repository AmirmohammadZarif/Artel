from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch,Rectangle
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
VecStart_x = [1]
VecStart_y = [0]
VecStart_z = [0]

VecEnd_x = [1]
VecEnd_y = [10]
VecEnd_z = [0]

print()



# # Draw a circle on the x=0 'wall'
p = Rectangle((0, 0),4,10)

ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=0, zdir="y")

p2 = Rectangle((0, 0),4,10)
ax.add_patch(p2)
art3d.pathpatch(p2)
# Draw a Line
for i in range(1):
    ax.plot([VecStart_x[i], VecEnd_x[i]], [VecStart_y[i],VecEnd_y[i]],zs=[VecStart_z[i],VecEnd_z[i]],color="r",marker="o")

ax.set_zlim(0, bp)

plt.show()

