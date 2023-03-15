"""!
@file MasterMind.py
    This file contains a demonstration program that checks the specific states of the gun. This is the hub for all of our
    motor positioning/firing, and mainly interfaces with our thermal camera to get positioning and set the position and 
    fire if needed. This sets four states, 0, 1, 2, and 3. State 0 initializes.
    It also hardcodes in the KP and position. State 1 waits for data from the other code. State 2 gets positional data. State 3
    fires the gun. State 4 is an error state. 

@author Toby Darci, Tobias Thomas, Sydney Gothenquist
@date   2023-Mar-11 
    """

import time
import pyb

#yaw = [3.348585, 3.290483, 3.231351, 3.171584, 3.111602, 3.051835, 2.992703, 2.934601]
yaw = [2.9346, 2.9927, 3.0518, 3.1116, 3.1716, 3.2314, 3.2905, 3.3486]
#pitch = [0, 0.1016485, 0.06590443, 0.029991, -0.005999927, -0.04197533, 0, 0]
pitch = [0, 0.102, 0.066, 0.03, 0, 0, 0, 0]
for i in range(len(pitch)):
    pitch[i]+=0.01

#value is the number set by the camera from the 8x8 "x" matrix
buttonpin = pyb.Pin(pyb.Pin.board.PC13,pyb.Pin.IN,)
def angle(pos):
    posoct = oct(pos+int('10',8))[2:]
    position = [int(i) for i in posoct]
    yawindex = position[1]-1
    print(yawindex)
    pitchindex = position[0]-1
    print(pitchindex)
    yawang = yaw[yawindex]
    pitchang = pitch[pitchindex]
    return(yawang, pitchang)

def mastermind(shares):
    updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI = shares
    state = 0
    state1 = 0
    while True:
        if state == 0:
            state = 1
            KP.put(0)
            KI.put(0)
            ready.put(0b00)
            fired.put(0)
        elif state == 1:
            if buttonpin.value() == False:
                state = 4
                starttime = time.time()
                theta1.put(3.14159)
                theta2.put(0)
                KP.put(0.018)
                KI.put(00.001)
                updatemotor.put(0b11)        
        elif state == 2:
            if updateang.get()==0b01:
                pos = position.get()
                print(oct(pos+int('10',8))[2:])
                yawang,pitchang = angle(pos)
                print("yaw: " +str(yawang)+"\npitch: "+str(pitchang))
                KP.put(0.008)
                KI.put(0.01)
                theta1.put(yawang)
                theta2.put(pitchang)
                updatemotor.put(0b11)
                updateang.put(0b0)
            if ready.get()== 0b11:
                state = 3
                ready.put(0b00)
                fire.put(0b01)
                
        elif state == 3:
            if (fire.get() == 0b00):
                print("fire!")
                state = 5
               
        elif state == 4:
            #rotate 180
            if (ready.get() == 0b11) & (time.time()-starttime > 5):
                state = 2
                updateang.put(0b11)
                ready.put(0)
        
        elif state ==5:
            if buttonpin.value() == False:
                updateang.put(0b11)
                fired.put(0b11)
                state = 1
        else:
            state = 0
            print("state out of range")
            
        if state != state1:
            print("Mastermind is at state "+str(state))
        state1 = state
        yield state
                    
                
        
