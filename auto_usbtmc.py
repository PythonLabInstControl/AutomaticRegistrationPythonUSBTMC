"""
Created on 19.09.2014
Veronika Schrenk and Alexander Venuleth
Description: This program helps to automatically register USB-Devices in
the '/etc/udev/rules.d/usbtmc.rules'-file to be able to use them with python-usbtmc.

Usage: When starting the program wait until a messageBox tells you to
connect your new USB-device. Connect your new device and then click 'OK'.
"""

import subprocess
import os
import re

firstDeviceList = [100]
secondDeviceList = [100]
newDevice = ""

def reset_file(f):
    '''Delete previous data from file'''
    f.seek(0)
    f.truncate()

def read_file(f):
    f = open("devices.txt", "r");
    return f.read();

def writeInArray(array):
    '''Save the hexadecimal numbers from file in arrays'''
    f = open("devices.txt", "r");
    for i, line in enumerate(f):
        if len(line) > 1:
            line = line[23:]
            array.append(line)

def compareArrays():
    '''Compare the two arrays and save the new USB-device'''
    global newDevice
    for i in secondDeviceList:
        if i not in firstDeviceList:
            newDevice = str(i)

def writeHex():
    '''Write the hexadecimal numbers with their optinal description from lsusb into the file'''
    f = open("devices.txt", "w");
    reset_file(f) #Delete previous data from the file
    subprocess.call(["lsusb"], stdout=f) #Send the "lsusb" command to the kernel to get all connected USB-devices
    writeInArray(firstDeviceList) #Save the USB-devices in arrays

    reset_file(f)    
    subprocess.call(["echo $DISPLAY"], stdout=f, shell=True)
    display = read_file(f)
    
    respConsole = ""   
    respDisplay = -10
    if(display == "\n" or display is None or display == ""):
        hasDisplay = False
        while(respConsole != "Y" or respConsole != "n"):
            respConsole = raw_input("Connect USB-device NOW![Yn]")
            if(respConsole == "Y" or respConsole == "n"):
                break;
    else:
        hasDisplay = True
        respDisplay = subprocess.call(["zenity --warning --text \"Connect USB-device NOW Then click OK!\""], shell=True)
    
    if(respDisplay == 0 or respConsole == "Y"):
        reset_file(f);    
        subprocess.call(["lsusb"], stdout=f) 
        writeInArray(secondDeviceList) 
        compareArrays() #Check, if a new USB-device has been connected
        if(newDevice == ""): 
            if(hasDisplay):
                subprocess.call(["zenity --warning --text \"No new USB-device found!\nProgram aborted!\""], shell=True)
            else:
                print("No new USB-device found!\nProgram aborted!")
        else:
            f2 = open("/etc/udev/rules.d/usbtmc.rules", "r")
            output = f2.read()
            newDeviceArray = newDevice.split(':')
            idVendor = newDeviceArray[0]; #First hexadecimal number
            idProduct = newDeviceArray[1][:4]; #Second hexadecimal number
            bez = newDeviceArray[1][5:] #Optional description
            if((idVendor in output) and (idProduct in output)):
                 if(hasDisplay):                
                     subprocess.call(["zenity --warning --text \"USB-device already registered!\""], shell=True)
                 else:
                    print("USB-device already registered!")
            else: #Write the hexadeciaml numbers and the description into the file 
                f2 = open("/etc/udev/rules.d/usbtmc.rules", "a")
                f2.writelines("\n\n#" + bez + "\nSUBSYSTEMS==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\""  + idVendor + "\", ATTRS{idProduct}==\"" + idProduct + "\", GROUP=\"usbtmc\", MODE=\"0660\"\n")
                if(hasDisplay):
                    subprocess.call(["zenity --warning --text \"USB-device successfully registered!\""], shell=True)                
                else:
                    print("USB-device successfully registered!")
                f2.close();
                f.close();


writeHex()
