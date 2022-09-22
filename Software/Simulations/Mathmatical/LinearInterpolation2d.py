import matplotlib.pyplot as plt
from statistics import mean
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def lineFromPoints(P,Q): 
    a = Q[1] - P[1] 
    b = P[0] - Q[0]  
    c = a * (P[0]) + b * (P[1])  
  
    if(b < 0):  
        print(a ,"x ",b ,"y = ",c ,"\n")  
        return [a, b, c]
    else: 
        print(a ,"x + " ,b ,"y = ",c ,"\n")  
        return [a, b, c]
        
def get_y(x, a, b, c):
    y = ((-a * x) + c) / b
    return y
 
x = [1,4]
y = [1,3]
z = [5,5]

S = [x[0], y[0]] 
E = [x[1], y[1]]

F = [z[0], z[0]]
D = [z[1], z[1]]

VecStart_x = [0,10,30,50]
VecStart_y = [20,20,50,50]
VecStart_z = [20,20,50,50]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# plt.xticks(range(1,250))
# ax.axis('equal') 
# ax.set_aspect(1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(xmin = -20, xmax = 20)
ax.set_ylim(-20, 20)
ax.set_zlim(-400, -200)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for j in range(0,len(VecStart_x)):
    if(j < len(VecStart_x)):

        S[0] = VecStart_x[j]
        S[1] = VecStart_y[j]
        E[0] = VecStart_x[j + 1]
        E[1] = VecStart_y[j + 1]

        F[0] = VecStart_x[j]
        F[1] = VecStart_z[j]

        D[0] = VecStart_x[j + 1]
        D[1] = VecStart_z[j + 1]
    
        print(S,E)
        print(lineFromPoints(S,E))
        Slope = lineFromPoints(S,E)

        SlopeZ = lineFromPoints(F,D)

        a = Slope[0]
        b = Slope[1]
        c = Slope[2]
        
        az = SlopeZ[0]
        bz = SlopeZ[1] + 1
        cz = SlopeZ[2]
        
        for i in range(S[0] * 10 ,E[0] * 10,5):
            x.append(i/10)
            yV = get_y(i / 10,a,b,c)
            # zV = get_y(i / 10,az,bz,cz)
            print(bz)
            y.append(yV)
            # z.append(zV)
            # plt.plot(x, y, zs=z, marker= 'o')
            # ax.plot(x, y, marker= 'o')
            plt.plot(x,y, marker= 'o')
            s = len(VecStart_x)
            # for n in range(0,s - 1,1):
                # ax.plot([x[n], x[n + 1]], [y[n], y[n + 1]],zs=[z[n], z[n + 1]],color="r",marker="o")
                # plt.pause(1)
           
            plt.pause(0.00002)
            
        for i in range(S[0] * 10 ,E[0] * 10,5):
            x.append(i/10)
            yV = get_y(i / 10,a,b,c)
            # zV = get_y(i / 10,az,bz,cz)
            print(bz)
            y.append(yV)
            # z.append(zV)
            # plt.plot(x, y, zs=z, marker= 'o')
            # ax.plot(x, y, marker= 'o')
            plt.plot(x,y, marker= 'o')
            s = len(VecStart_x)
            # for n in range(0,s - 1,1):
                # ax.plot([x[n], x[n + 1]], [y[n], y[n + 1]],zs=[z[n], z[n + 1]],color="r",marker="o")
                # plt.pause(1)
           
            plt.pause(0.00002)
            

        # plt.plot(x, y, z, marker= 'o')
        print(x,y)
        

        plt.show()
        
