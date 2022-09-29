import serial
import time

Client = serial.Serial('/dev/cu.usbmodem1411',57600)

time.sleep(2)
Ang = 0
print(Ang)
Client.write('Y,' + str(Ang) + '\n')
time.sleep(0.01)
Client.write('X,' + str(Ang) + '\n')
time.sleep(1)

Ang = 90
print(Ang)
Client.write('Y,' + str(Ang) + '\n')
time.sleep(0.01)
Client.write('X,' + str(Ang) + '\n')
time.sleep(1)

Ang = 180
print(Ang)
Client.write('Y,' + str(Ang) + '\n')
time.sleep(0.01)
Client.write('X,' + str(Ang) + '\n')
time.sleep(1)