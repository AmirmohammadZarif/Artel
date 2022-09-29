import matplotlib.pyplot as plt
from statistics import mean
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

x = [1,4,2]
y = [1,3,5]
S = [x[0], y[0]] 
E = [x[1], y[1]]  

S = [1, 1] 
E = [4, 3]
VecStart_x = [0,10,30,50]
VecStart_y = [20,20,50,50]
VecStart_z = [0,10,10,50]
VecEnd_x = [10,20,-10,60]
VecEnd_y = [30,10,-20,70]
VecEnd_z  =[10,0,40,90]


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

# print(x,y)

# print(lineFromPoints(S,E))
# Slope = lineFromPoints(S,E)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.set_aspect('equal')

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


for j in range(0,len(VecStart_x) - 1):
    
    S[0] = VecStart_x[j]
    E[0] = VecStart_x[j + 1]
    S[1] = VecStart_y[j]
    E[1] = VecStart_y[j + 1]
    # print(S,E)
    # print(lineFromPoints(S,E))
    Slope = lineFromPoints(S,E)
    a = Slope[0]
    b = Slope[1]
    c = Slope[2]
    # print(a,b,c)
    for i in range(S[0] * 100 ,E[0] * 100,1):
        VecStart_x.append(i/100)
        yV = get_y(i / 100,a,b,c)
        VecStart_y.append(yV)
        print(type(VecStart_x))
        
        print(VecStart_x[int(j)],VecStart_y[int(j)])
        # print(len(VecStart_x))
        # plt.plot(VecStart_x[int(j)], VecStart_y[int(j)], 'o')
        
        
        s = len(VecStart_x)
        print(s,VecStart_x)
        
        for n in range(0,s - 1,1):
            ax.plot([VecStart_x[int(n)], VecEnd_x[int(n)]], [VecStart_y[int(n)],VecEnd_y[int(n)]],zs=[VecStart_z[int(n)],VecEnd_z[int(n)]],color="r",marker="o")
            plt.pause(1)
        plt.show()








# Axes3D.plot()




plt.show()
