import os
import time

from aptos_connection.aptos_testing import *
print("successfully imported aptos")
from aptos_connection.pinata_interface import *
print("successfully imported pinata")
from teensy_computer_interface.teensy_interface import *
print("successfully imported teensy interface")
#import source_code.face+record
print("successfully imported CV")



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
    

    while True:
        #check if there is a donation
        depAddress = getNextDepositorAddress(aptosWallet.address())
        if depAddress == "":
            time.sleep(1)
        else:
            #start recording
            startPump()
            time.sleep(2)
            stopPump()
        
            #stop recording
            #find video
            ipfshash = uploadToIPFS("output.mp4")
            sendNFT(aptosWallet, depAddress, "ipfs://"+ipfshash)
        pass