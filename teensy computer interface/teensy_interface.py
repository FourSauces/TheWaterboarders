import time
import serial
from serial.tools import list_ports

ser = None
def initSerial(comport):
    global ser
    ser = serial.Serial(comport)
    ser.baudrate = 115200
    print("Serial initialized")


def closeSerial():
    global ser
    ser.close()

def chooseDevice():
    serialdevices = []
    comports = list_ports.comports()
    potentialports = []
    for port in comports:
        if port.description != "n/a":
            potentialports.append(port)
    if(len(potentialports)>1):
        for index, serialport in enumerate(potentialports):
            print(str(index+1)+": '"+serialport.description+"'")
            serialdevices.append(serialport.device)
        serialindex = int(input("Choose the serial port to use (Enter the number) "))
        comport = serialdevices[serialindex-1]
    else:
        comport = potentialports[0].device
        print("Port selected as "+str(comport))
    return comport

def sendByte(byteint):
    global ser
    ser.write(bytes(chr(byteint), 'utf-8'))

def startPump():
    sendByte(65)
    print("Pump turned on")

def stopPump():
    sendByte(66)
    print("Pump turned off")

def ledRedOn():
    sendByte(67)
    print("Red LEDs turned on")

def ledRedOff():
    sendByte(68)
    print("Red LEDs turned off")

def ledGreenOn():
    sendByte(69)
    print("Green LEDs turned on")

def ledGreenOff():
    sendByte(70)
    print("Green LEDs turned off")

def ledBlueOn():
    sendByte(71)
    print("Blue LEDs turned on")

def ledBlueOff():
    sendByte(72)
    print("Blue LEDs turned off")

def setXServo(position):
    sendByte(73)
    sendByte(position)
    print("X Servo set to position:", position)

def setYServo(position):
    sendByte(74)
    sendByte(position)
    print("Y Servo set to position:", position)


initSerial(chooseDevice())


if(__name__ == "__main__"):
    startPump()
    ledRedOn()
    time.sleep(.5)
    stopPump()
    ledRedOff()
    ledGreenOn()
    setXServo(128)
    setYServo(128)
    time.sleep(.5)
    ledGreenOff()
    setXServo(0)
    setYServo(0)
    time.sleep(.5)
    ledBlueOn()
    time.sleep(.5)
    ledBlueOff()
