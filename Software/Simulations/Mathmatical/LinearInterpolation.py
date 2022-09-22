import matplotlib.pyplot as plt
from statistics import mean
import numpy as np

x = [1,4]
y = [1,3]

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
S = [1, 1] 
E = [4, 10]  

print(lineFromPoints(S,E))
Slope = lineFromPoints(S,E)

a = Slope[0]
b = Slope[1]
c = Slope[2]
plt.ylim(0,10)
for i in range(S[0] * 100 ,E[0] * 100,10):
    x.append(i/100)
    yV = get_y(i / 100,a,b,c)
    y.append(yV)
    plt.plot(x, y, 'o')
    plt.pause(0.00001)
print(x,y)

plt.show()