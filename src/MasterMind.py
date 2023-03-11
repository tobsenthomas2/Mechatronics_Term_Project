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
#setting motor positions from the camera outputs
import mlx_cam.py
import motor2.py
import motor1.py
import controlServo.py
import math

#these are the angles/ticks we need to move per each value of the 8x8 matrix
#each segment on table is 6" or 1.3 deg of rotation (X-Y sweep) for a 48" wide by 175" long range
# 0.03611 rev/1.3 deg
width_tot = 48
length_tot = 175

#the number of ticks/radians
encoderticks_rad = 1

#this is in rads; half the table
angle_init = (math.atan((width_tot/2)/length_tot))


#initializes the pitch positioning
yaw_init = [(3.14 - angle_init)*encoderticks_rad]
for j in range 7
    yaw_init.append(yaw_init(0)+ (angle_init*encoderticks_rad))

pitch_init = []
angle_yaw = 1
angle_pitch = 1   

state = 0


#value is the number set by the camera from the 8x8 "x" matrix
def getpos(value):
    """!
    This function takes data from the camera and sets the pitch and yaw positioning
    @param[in] value - value indicating the pitch and yaw finite positioning
    """
    #z = list[value]
    position = [int(i) for i in str(value)]
    yaw = position[0]
    pitch = position[1]

    return(yaw, pitch)

def assignposvalue(yaw, pitch):
    yaw_pos = yaw*angle_yaw
    pitch_pos = pitch*angle_pitch

    return(yaw_pos, pitch_pos)

def update_motors():
    motor1.Motor1()
    motor2.Motor2()


def fire():
    """!
    This function fires the gun using the servo motor functionality.
    """
    controlServo.pullTheTrigger()


#wait for inputs
if state == 1:
    

#get information from other tasks
elif state == 2:
    if updateangle == 1:
        getpos()
        assignposvalue()
        #PWM_Calc.set_setpoint()
        update_motors()

#fire gun
elif state == 3:
    fire()
#prompt error
elif state == 4:

else:


# if state == 1:
#     for i in range 8
#         if i == camera.pitch[posx]
#         return i
#     for j in range 8
#         if j == camera.yaw[posz]
#         return j

