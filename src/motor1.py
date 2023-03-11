#Motor 1 initialization set up
from PWM_Calc import PWM_Calc
import pyb, time
from encoder_reader import EncoderClass
from  motor_driver import MotorDriver
import MasterMind.py

"""!The function initializes and runs the motor 1
@param[in] reset - boolean value indicating if the motor should be reset or not
This sets four states, 0, 1, 2, and 3. State 0 initializes the motor 1 and encoder ports.
It also hardcodes in the KP and position. State 1 runs the encoder and PWM based on the KP and
positional inputs. This will run for 400ms. State 2 turns off the motor and begins to print data. State 3
is used when data is done being transmitted. 
"""
def Motor1(reset):
    updatemotor,ready,fired,theta1 = shares
    state = 0
    #reset=True
    while True:
        if state == 0:
            Motor1=MotorDriver(pyb.Pin.board.PA10,pyb.Pin.board.PB4,pyb.Pin.board.PB5,3)
            encoder1=EncoderClass(pyb.Pin.board.PB6,pyb.Pin.board.PB7,4)
            encoder1.zero()
            Theta_Set = 0
            KP = 0.01
            pwm1 = PWM_Calc()
            pwm1.set_setpoint(Theta_Set)
            pwm1.set_KP(KP)
            state = 1 
            
        elif state == 1:
            motflg = updatemotor.get()
            if motflg & 0b01==True:
                Theta_Set = theta1.get()
                pwm1.set_setpoint(Theta_Set)
                updatemotor.put(motflg&0b10)
            Theta_Act = encoder1.read()
            PWM = pwm1.Run(Theta_Act)
            Motor1.set_duty_cycle(PWM)
            if abs(Theta_Set-Theta_Act)<10
                state = 2
                readyflg = ready.get()
                ready.put(readyflg | 0b01)
                Motor1.set_duty_cycle(0)
                
        elif state == 2:
            if fired.get()==True
                state = 1
                
        yield state

