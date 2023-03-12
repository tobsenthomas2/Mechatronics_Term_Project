#Motor 1 initialization set up

from PWM_Calc import PWM_Calc
import pyb, time
from encoder_reader import EncoderClass
from  motor_driver import MotorDriver
"""!
@file motor2.py
    This file contains all of the set up for the second motor that controls the pitch of the launcher.

@author Toby Darci, Tobias Thomas, Sydney Gothenquist
@date   2023-Mar-11 
    """


"""!The function initializes and runs the motor 1
@param[in] reset - boolean value indicating if the motor should be reset or not
This sets four states, 0, 1, 2, and 3. State 0 initializes the motor 1 and encoder ports.
It also hardcodes in the KP and position. State 1 runs the encoder and PWM based on the KP and
positional inputs. This will run for 400ms. State 2 turns off the motor and begins to print data. State 3
is used when data is done being transmitted.
"""

def Motor2(reset):
    state = 0
    while True:
        if state == 0:
            Motor2=MotorDriver(pyb.Pin.board.PC1,pyb.Pin.board.PA0,pyb.Pin.board.PA1,5)
            encoder2=EncoderClass(pyb.Pin.board.PC6,pyb.Pin.board.PC7,8)
            encoder2.zero()
            time_step = 0.01
            #Theta_Set = 100000
            #pitch position
            Theta_Set = MasterMind.getpos(pitch)
            KP = 0.025
            pwm2 = PWM_Calc()
            pwm2.set_setpoint(Theta_Set)
            pwm2.set_KP(KP)
            state = 1
            start = time.time_ns() // 1_000_000 #time in ms
            yield state
            
        elif state == 1:
            Theta_Act = encoder2.read()
            PWM = pwm2.Run(Theta_Act)
            Motor2.set_duty_cycle(PWM)
            time.sleep(time_step) #updates 0.01s
            stop = time.time_ns() // 1_000_000
            duration=(stop-start)
            if (int(duration)) >= 4000:#time in ms
                state = 2
            yield state
            
        elif state == 2:
            Motor2.set_duty_cycle(0)
            pwm2.Print_Data(False)
            state = 3
            
            yield state
            
        elif state == 3:
            if reset == True:
                state = 0
            yield state

