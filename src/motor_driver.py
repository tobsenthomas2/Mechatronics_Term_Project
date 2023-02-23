import pyb
import time

class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin (There will be several pin parameters)
        @param en_pin: the pin number for the enable pin, used to enable or disable the motor.
        @param in1pin: the pin number for the IN1 pin, used to control the direction of the motor.
        @param in2pin: the pin number for the IN2 pin, used to control the direction of the motor.
        @param timer: the timer number for the PWM timer, used to control the duty cycle of the motor.


        From EncoderClass() we call: In1pin and In2pin to define the pins (B6/B7 or C6/C7). 
        And the TimerNR for the timer channel based on the In pins (TCh 4 or 8)
        From MotorDriver() we call: the pin to enable to motor (EN_Pin)
        and set the torque control pins (PB4/5 or PA0/1) as well as the corresponding
        timer (3 or 5)
        """
        self.enable_pin=en_pin
        self.IN1_Pin=in1pin
        self.IN2_Pin=in2pin
        self.pwmTim=timer
       
        """! This enables the EN pin to be high to run the motor
        and sets it as an output
        """
        pinEN = pyb.Pin (self.enable_pin, pyb.Pin.OUT_PP) #enable
        pinEN.value(1)
        
        """! This enables the In pins to be an output and sets the 
        timer frequency
        """
        pinIn1 = pyb.Pin (self.IN1_Pin, pyb.Pin.OUT_PP) 
        pinIn2 = pyb.Pin (self.IN2_Pin, pyb.Pin.OUT_PP) 
        
        tim = pyb.Timer (self.pwmTim, freq=20000)
        
        """! For the assigned duty cycle, we can set this to a specific
        output pin, so that the duty cycle outputs the correct voltage
        to the correct port, and runs the motor based on this input duty cycle
        """
        self.ch1 = tim.channel (1, pyb.Timer.PWM, pin=pinIn1)
        self.ch2 = tim.channel (2, pyb.Timer.PWM, pin=pinIn2)
        
        
        print ("Creating a motor driver")

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level to specify the motor speed.
        Positive values cause torque in one direction, negative values
        in the opposite direction.
        @@param level: a signed integer representing the duty cycle of the
        voltage sent to the motor. Positive values cause the motor to turn
        in one direction, negative values cause the motor to turn in
        """
        """! For a negative input, we can run CH 1 so it spins one way
        and for a positive input we can run CH 2 so it spins the 
        opposite direction for multidirectional capabilities
        """
        
        """This will saturate the motor to 0-100% for PWM"""
        
        if (level<0):
            if(level<=-100):
                self.ch1.pulse_width_percent (100)
                self.ch2.pulse_width_percent (0)
            else:
                self.ch1.pulse_width_percent (abs(level))
                self.ch2.pulse_width_percent (0)
        else:
            if(level>=100):
                self.ch1.pulse_width_percent (0)
                self.ch2.pulse_width_percent (100)
            else:
                self.ch1.pulse_width_percent (0)
                self.ch2.pulse_width_percent (abs(level))
            