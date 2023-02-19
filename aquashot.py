import os
import time
import threading
from aptos_connection.aptos_testing import *
print("successfully imported aptos")
from aptos_connection.pinata_interface import *
print("successfully imported pinata")
from teensy_computer_interface.teensy_interface import *
print("successfully imported teensy interface")
from source_code.facerecord import *
print("successfully imported CV")


def maintainServoTracking():
    print("Servo tracking started")
    faces = []
    while True:
        time.sleep(1)
        faces = recorder.prevFaces
        xSum = 0
        ySum = 0
        numEntries = 0
        for (x, y) in faces:
            if x>=0 and y>=0:
                xSum+=x
                ySum+=y
                numEntries+=1
        if numEntries==0:
            numEntries=1
        xAvg = xSum/numEntries
        yAvg = ySum/numEntries
        height, width, channels = [1080,1920,3]

        print("height", height, "width", width, "xavg", xAvg, "yavg", yAvg)
        xmargin = .1
        ymargin = .1
        if xAvg < (width/2+width*(xmargin/2)) and xAvg>(width/2-width*(xmargin/2)):
            #x doesn't need moving
            pass
        elif xAvg-(width/2)>0:
            #move left
            setXServo(86)
            time.sleep(.1)
            setXServo(90)
            pass
        else:
            #move right
            setXServo(94)
            time.sleep(.1)
            setXServo(90)
            pass

        if yAvg < (height/2+height*(ymargin/2)) and yAvg>(height/2-height*(ymargin/2)):
            #y doesn't need moving
            pass
        elif xAvg-(width/2)>0:
            #move up
            setYServo(yServoPos+2)
            pass
        else:
            #move down
            setYServo(yServoPos-2)
            pass
        




if __name__ == "__main__":
    #init aptos wallet
    aptosWallet = Account.load("receiver.txt")
    print("Aptos wallet successfully initialized")

    #initializing the teensy interface
    initSerial(chooseDevice())
    stopPump()
    ledRedOff()
    ledGreenOff()
    ledBlueOff()
    print("Teensy successfully initialized")

    #initialize CV and tracking threads
 
    recorder = WebcamRecorder("output.mp4")
    print("recorder created")
    recorder.start()
    print("recorder started")
    #j = threading.Thread(target=maintainServoTracking)
    #j.start()
    while True:
        #check if there is a donation
        depAddress = getNextDepositorAddress(aptosWallet.address())
        if depAddress == "":
            time.sleep(1)
        else:
            #start recording
            recorder.isRecording = True
            startPump()
            ledGreenOff()
            ledRedOn()
            time.sleep(2)
            stopPump()
            ledRedOff()
            ledGreenOn()
            try:
                os.remove(str(os.getcwd())+"/output.mp4")
            except: 
                print("file does not exist")
            recorder._save()
            print("video saved")
            ipfshash = uploadToIPFS("output.mp4")
            print(ipfshash)
            sendNFT(aptosWallet, depAddress, "ipfs://"+ipfshash+".mp4")
        pass