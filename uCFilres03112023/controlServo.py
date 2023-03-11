import machine
import time
from  motor_driver import MotorDriver
import pyb, time
# Set up PWM output pin

# Set up servo parameters
servo_frequency = 50  # Servo PWM frequency (Hz)
servo_duty_min = 2    # Duty cycle for 0 degrees
servo_duty_max = 12   # Duty cycle for 180 degrees

#Servo SG90 Pinning:
#yellow Signal (3.3V should be enought)
#red 5V
#brown ground
def pullTheTrigger():
    """!
        @brief	Pulls the Trigger of the gun as soon as the aiming is done

        @param Non

        @returns: non
    """
    while (1):
        if (task_share.Share.get()): #should get us some data
            set_servo_position(90)
            time.sleep(1)
            set_servo_position(0)
            time.sleep(1)
            print("one cycle")
            
        
        yield

# Cleanup PWM output pin
#servo_pwm.deinit()



def set_servo_position(position_degrees):
    """!
        @brief	Set the position of the servo motor.

        @param position_degrees (float): The desired position of the servo motor in degrees.

        @returns: non
    """
    # Convert position to duty cycle
    
            
    duty = (servo_duty_max - servo_duty_min) * position_degrees / 180 + servo_duty_min
    # Set duty cycle
    #servo_pwm.duty_u16(int(duty * 65535))
    Motor1=MotorDriver(pyb.Pin.board.PA10,pyb.Pin.board.PB4,pyb.Pin.board.PB5,3)
    Motor1.set_duty_cycle(int(duty * 65535))
    
    
# Example usage: move servo to 90 degrees and back to 0 degrees


if __name__ == "__main__":	
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")
    Motor1=MotorDriver(pyb.Pin.board.PA10,pyb.Pin.board.PB4,pyb.Pin.board.PB5,3)
    Motor1.set_duty_cycle(90)
    #pullTheTrigger()
#     while (1):
#         if (1):#task_share.Share.get()): #should get us some data
#             set_servo_position(90)
#             time.sleep(1)
#             set_servo_position(0)
#             time.sleep(1)
#             print("one cycle")