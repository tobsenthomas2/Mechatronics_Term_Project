import machine
import time

# Set up PWM output pin
servo_pin = machine.Pin('PA0')  # Servo output pin
servo_pwm = machine.PWM(servo_pin)  # PWM object for servo pin

# Set up servo parameters
servo_frequency = 50  # Servo PWM frequency (Hz)
servo_duty_min = 2    # Duty cycle for 0 degrees
servo_duty_max = 12   # Duty cycle for 180 degrees


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
        
        yield

# Cleanup PWM output pin
servo_pwm.deinit()



def set_servo_position(position_degrees):
    """!
        @brief	Set the position of the servo motor.

        @param position_degrees (float): The desired position of the servo motor in degrees.

        @returns: non
    """
    # Convert position to duty cycle
    duty = (servo_duty_max - servo_duty_min) * position_degrees / 180 + servo_duty_min
    # Set duty cycle
    servo_pwm.duty_u16(int(duty * 65535))

# Example usage: move servo to 90 degrees and back to 0 degrees
