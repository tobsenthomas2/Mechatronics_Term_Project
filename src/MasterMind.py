"""!
@file MasterMind.py
    This file contains a demonstration program that checks the specific states of the gun. This is the hub for all of our
    motor positioning/firing, and mainly interfaces with our thermal camera to get positioning and set the position and 
    fire if needed. This sets four states, 0, 1, 2, and 3. State 0 initializes.
    It also hardcodes in the KP and KI position. State 1 waits for data from the other code. State 2 gets positional data. State 3
    fires the gun. State 4 is an error state. 

@author Toby Darci, Tobias Thomas, Sydney Gothenquist
@date   2023-Mar-11 
    """

import time

yaw = [3.2462093112223127, 3.21645250130056, 3.1865623154421208, 3.1565915287416435, 3.1265937784379427, 3.0966229917374655, 3.066732805879026, 3.0369759959572735]
pitch = [-0.04871143583454709, -0.02624397319463619, -0.0037499824220233137, 0.01874780319774436, 0.04122662737298013, 0.06366384864918946, 0.08603707651884827, 0.1083243037649297]
#value is the number set by the camera from the 8x8 "x" matrix
def angle(pos):
    """!
    @brief Calculates the yaw and pitch angles from the given position.
    @param pos The number set by the camera from the 8x8 "x" matrix.
    @return The yaw and pitch angles in radians.
    """

    posoct = oct(pos+int('10',8))[2:]
    position = [int(i) for i in posoct]
    yawindex = position[0]-1
    pitchindex = position[1]-1
    yawang = yaw[yawindex]
    pitchang = pitch[pitchindex]
    return(yawang, pitchang)

def mastermind(shares):
    """!
    @brief The main function that controls the gun's states.
    @param shares A list of shared variables.
    """
    
    updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI = shares
    state = 0
    state1 = 0
    while True:
        if state == 0:
            state = 1
            KP.put(0)
            KI.put(0)
            ready.put(0b00)
        elif state == 1:
            #password = input("enter password: ")
            password = "2t1s"
            if password == "2t1s":
                print("starting...")
                state = 4
                starttime = time.time()
                theta1.put(3.14159)
                theta2.put(0.3)
                KP.put(0.02)
                KI.put(0)
                updatemotor.put(0b11)
            else:
                print("wrong Password!!")
                
        elif state == 2:
            if updateang.get()==0b01:
                pos = position.get()
                yawang,pitchang = angle(pos)
                KP.put(0.025)
                KI.put(0.005)
                theta1.put(yawang)
                theta2.put(pitchang)
                updatemotor.put(0b11)
                updateang.put(0b0)
            if ready.get()== 0b11:
                state = 3
                ready.put(0b00)
                fire.put(0b01)
                
        elif state == 3:
            firedflg = 1
            fire.put(0)
            if (firedflg&0b01 == True)&(fire.get() == 0b00):
                fired.put(firedflg & ~0b01)
                print("fire!")
                state = 2
                updateang.put(0b01)
                
        elif state == 4:
            #rotate 180
            if (ready.get() == 0b11) & (time.time()-starttime > 5):
                state = 2
                updateang.put(0b01)
              
        else:
            state = 0
            print("state out of range")
            
        if state != state1:
            print("Mastermind is at state "+str(state))
        state1 = state
        yield state
                    
                
        
