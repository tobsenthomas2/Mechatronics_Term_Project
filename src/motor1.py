#Motor 1 initialization set up
from PWM_Calc import PWM_Calc
import pyb, time
from encoder_reader import EncoderClass
from  motor_driver import MotorDriver
import math

encticperrad = 16000/(2*math.pi)
"""!The function initializes and runs the motor 1
@param[in] reset - boolean value indicating if the motor should be reset or not
This sets four states, 0, 1, 2, and 3. State 0 initializes the motor 1 and encoder ports.
It also hardcodes in the KP and position. State 1 runs the encoder and PWM based on the KP and
positional inputs. This will run for 400ms. State 2 turns off the motor and begins to print data. State 3
is used when data is done being transmitted. 
"""
def Motor1(shares):
    updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI = shares
    state = 0
    state1 = 0
    #reset=True
    while True:
        if state == 0:
            Motor1=MotorDriver(pyb.Pin.board.PA10,pyb.Pin.board.PB4,pyb.Pin.board.PB5,3)
            encoder1=EncoderClass(pyb.Pin.board.PB6,pyb.Pin.board.PB7,4)
            encoder1.zero()
            Theta_Set = 16000
            pwm1 = PWM_Calc(20,5)
            motflg1 = 0
            state = 2
            
        elif state == 1:
            Theta_Act = encoder1.read()
            PWM = pwm1.Run(Theta_Act)
            Motor1.set_duty_cycle(PWM)
            if abs(Theta_Set-Theta_Act)<0.04*encticperrad*250/30:
                readyflg = ready.get()
                ready.put(readyflg | 0b01)
                print("motor 1: "+str(Theta_Act/encticperrad/250*30))
                Motor1.set_duty_cycle(0)
                state = 2
                
        elif state == 2:
            motflg = updatemotor.get()
            if fired.get()&0b01 == True:
                state = 0
                fired.put(fired.get()&0b10)
            if motflg & 0b01==True:
                pwm1.resetint()
                pwm1.set_KP_KI_KD(KP.get(),KI.get(),0)
                Theta_Set = theta1.get()*encticperrad*250/30
                pwm1.set_setpoint(Theta_Set)
                updatemotor.put(motflg&0b10)
                state=1

        if state != state1:
            print("Mator1 is at state "+str(state))
        state1 = state
                
        yield state

