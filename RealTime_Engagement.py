"""
Mind Monitor - EEG OSC Receiver
Coded: James Clutterbuck (2022)
Requires: pip install python-osc
"""
from datetime import datetime
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from codrone_edu.drone import *


drone = Drone()
drone.pair() # pair automatically, may not always work
# drone.pair(port_name = 'COM3')    # pair with a specific port


ip = "10.122.27.205"
port = 5006
filePath = 'test.csv'
auxCount = -1
recording = False

theta = -1;
alpha = -1;
beta = -1;
engagement = -1;
inAir = False
blinkCounter = 0;
old_time = -1

f = open (filePath,'w+')

def writeFileHeader():
    global auxCount
    fileString = 'TimeStamp,RAW_TP9,RAW_AF7,RAW_AF8,RAW_TP10,'
    for x in range(0,auxCount):
        fileString += 'AUX'+str(x+1)+','
    fileString +='Marker\n'
    f.write(fileString)

def eeg_handler(address: str,*args):
    global recording
    global auxCount
    global theta
    global beta
    global alpha
    global engagement
    global inAir
    global blinkCounter
    global old_time
    
    if auxCount==-1:
        auxCount = len(args)-4
        writeFileHeader()
    if recording:
        if old_time == -1:
            old_time = time.time()
        if time.time()-old_time > 5:
            print("Blinks Counted: ", blinkCounter)
            if blinkCounter == 2:
                if inAir:
                    drone.land()
                    print("Landing")
                else:
                    drone.takeoff()
                    print("Taking off")
                inAir = not inAir
                
            if blinkCounter == 3:
                print("Moving forward")
                drone.move_forward(10, "cm", 0.5)
            if blinkCounter == 4:
                print("Turning right")
                drone.right()
            if blinkCounter == 5:
                print("Turning left")
                drone.left()
            blinkCounter = 0
            old_time = time.time() + 1
        timestampStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        fileString = timestampStr
        if address == "/muse/elements/theta_absolute":
            theta = args[0]
            # print("Theta: ", theta)
        elif address == "/muse/elements/beta_absolute":
            beta = args[0]
            # print("Beta: ", beta)
        elif address == "/muse/elements/alpha_absolute":
            alpha = args[0]
            # print("Alpha: ", alpha)
        elif address == "/muse/elements/jaw_clench":
            print("Jaw Clenched")
            # drone.flip("front")
#             if blinkCounter == 1:
#                 if inAir:
#                     # drone.takeoff()
#                     print("Taking off")
#                 else:
#                     # drone.land()
#                     print("Landing")
#                 inAir = not inAir
                
#             if blinkCounter == 2:
#                 print("Moving forward")
#                 # drone.move_forward(10, "cm", 0.5)
#             if blinkCounter == 3:
#                 print("Turning right")
#                 # drone.right()
#             if blinkCounter == 4:
#                 print("Turning left")
#                 # drone.left()
            # blinkCounter = 0
            # drone.turn_right() # make a 90 degree right turn.

        elif address == "/muse/elements/blink":
            
            blinkCounter += 1
            print("Blinked: ", blinkCounter)
                
            # drone.hover(1)
            # drone.land()
       
        # if theta != -1 and beta != -1 and alpha != -1:
        #     engagement = (beta) / (alpha + theta)
            # print("Engagement: ", engagement)
        
        # for arg in args:
        #     fileString += ","+str(arg)            
        # fileString+="\n"
        # # print(fileString)
        # f.write(fileString)
    
def marker_handler(address: str,i):
    global recording
    global auxCount
    timestampStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    markerNum = address[-1]
    if recording:
        fileString = timestampStr+',,,,,'
        for x in range (0,auxCount):
            fileString +=','
        fileString +='/Marker/'+markerNum+"\n"
        f.write(fileString)
    if (markerNum=="1"):        
        recording = True
        print("Recording Started.")
    if (markerNum=="2"):
        f.close()
        recording = False
        server.shutdown()
        print("Recording Stopped.")    

if __name__ == "__main__":
    try:
        dispatcher = dispatcher.Dispatcher()
        dispatcher.map("/muse/elements/theta_absolute", eeg_handler)
        dispatcher.map("/muse/elements/alpha_absolute", eeg_handler)
        dispatcher.map("/muse/elements/beta_absolute", eeg_handler)
        dispatcher.map("/muse/elements/jaw_clench", eeg_handler)
        dispatcher.map("/muse/elements/blink", eeg_handler)


        dispatcher.map("/Marker/*", marker_handler)

        server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
        print("Listening on UDP port "+str(port)+"\nSend Marker 1 to Start recording and Marker 2 to Stop Recording.")
        old_time = time.time()
        server.serve_forever()
        
            
    except KeyboardInterupt:
        drone.close()
    # drone.close()
