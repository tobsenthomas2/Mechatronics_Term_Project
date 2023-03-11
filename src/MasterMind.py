
#setting motor positions from the camera outputs
import mlx_cam.py
import motor2.py
import motor1.py

#these are the angles/ticks we need to move per each value of the 8x8 matrix
angle_yaw = 1
angle_pitch = 1   

state = 0

#value is the number set by the camera from the 8x8 "x" matrix
def getpos(value):
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
    motor_servo.fire()

#wait for inputs
if state == 1:
    

#get information from other tasks
elif state == 2:
    getpos()
    assignposvalue()
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



