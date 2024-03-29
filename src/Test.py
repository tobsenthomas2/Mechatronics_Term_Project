"""!
@file test.py
    File used to test various timesteps, KP/KI gain values, and other user
    set inputs for the functionality of the "launcher"

@author Toby Darci, Tobias Thomas, Sydney Gothenquist
@date   2023-Mar-11 
    """

from PWM_Calc import PWM_Calc
import pyb, time
from encoder_reader import EncoderClass
from  motor_driver import MotorDriver
#com6 for shoe
#com5 for stm32

if __name__ == "__main__":
    """!
        This is our main, from here we can call MotorDriver() and EncoderClass()
        classes and specify the specific parameters based on what pins we are 
        using.
        From EncoderClass() we call: In1pin and In2pin to define the pins (B6/B7 or C6/C7). 
        And the TimerNR for the timer channel based on the In pins (TCh 4 or 8)
        From MotorDriver() we call: the pin to enable to motor (EN_Pin)
        and set the torque control pins (PB4/5 or PA0/1) as well as the corresponding
        timer (3 or 5)
        We can also call the set_duty_cycle() class to set a specific duty cycle that will
        run the motor in the correct direction at a specific speed
        """
    
    Motor1=MotorDriver(pyb.Pin.board.PA10,pyb.Pin.board.PB4,pyb.Pin.board.PB5,3)
    #Motor1.set_duty_cycle(0)
    #encoder=EncoderClass(pyb.Pin.board.PB6,pyb.Pin.board.PB7,4)
    #encoder.zero()
    #pwm = PWM_Calc()
    
    #Theta_Set = input("set position: ")
    #KP = input("set KP: ")
    #KP = 0.025 for decent data
    time_step = 0.01
    
    #pwm.set_setpoint(Theta_Set)
    #pwm.set_KP(KP)

    count=0
    for i in range (40000):
         #Theta_Act = encoder.read()
         #PWM = pwm.Run(Theta_Act)
         count=count+1
         #Motor1.set_duty_cycle(0)
         #print("26")
         time.sleep(3) #updates 0.01s
         #Motor1.set_duty_cycle(15)
         print(count)
         Motor1.set_duty_cycle(count)
        
         
    #Motor1.set_duty_cycle(0)       
    #pwm.Print_Data()
    
    
    
    
