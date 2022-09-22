import pyautogui 
import serial 
import time
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

Machine = serial.Serial('/dev/cu.usbmodem1411',115200)

while True:
    # (1679, 1049)
    # print(pyautogui.position())
    X = pyautogui.position()[0]
    Y = pyautogui.position()[1]
    X = int(translate(X,0,1679,0,180))
    Y = int(translate(Y,0,1049,0,180))
    XMachine = "X" + str(int(X)) + "\n"
    YMachine = "Y" + str(int(Y)) + "\n"
    Machine.write(XMachine.encode())
    # Machine.write(bytes(YMachine, 'utf-8'))
    print(XMachine.encode())
    time.sleep(0.1)
    

