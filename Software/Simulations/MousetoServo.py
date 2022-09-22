import pyautogui 
import serial 
import time
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

Machine = serial.Serial('/dev/cu.usbmodem1411',57600)
time.sleep(1)
while True:
    # (1679, 1049)
    # print(pyautogui.position())
    X = pyautogui.position()[0]
    Y = pyautogui.position()[1]
    X = int(translate(X,0,1679,0,180))
    Y = int(translate(Y,0,1049,0,180))
    XMachine = str(int(X))
    YMachine = str(int(Y))
    Machine.write("X," + XMachine + "\n")
    Machine.write("Y," + YMachine + "\n")
    print("X," + XMachine)
    print("Y," + XMachine + "\n")
    time.sleep(0.1)
    

