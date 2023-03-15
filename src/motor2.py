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
def Motor2(shares):
    updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI = shares
    state = 0
    state1 = 0
    #reset=True
    while True:
        if state == 0:
            Motor2=MotorDriver(pyb.Pin.board.PC1,pyb.Pin.board.PA0,pyb.Pin.board.PA1,5)
            encoder2=EncoderClass(pyb.Pin.board.PC6,pyb.Pin.board.PC7,8)
            encoder2.zero()
            Theta_Set = 16000
            pwm2 = PWM_Calc()
            motflg1 = 0
            state = 2
            
        elif state == 1:
            Theta_Act = encoder2.read()
            PWM = pwm2.Run(Theta_Act)
            Motor2.set_duty_cycle(PWM)
            if abs(Theta_Set-Theta_Act)<0.04*encticperrad*8:
                readyflg = ready.get()
                ready.put(readyflg | 0b10)
                print("motor 2: "+str(Theta_Act/encticperrad/8))
                Motor2.set_duty_cycle(0)
                state = 2
                
        elif state == 2:
            if fired.get()>>1 == True:
                fired.put(fired.get()&0b01)
                state = 0
            motflg = updatemotor.get()
            if motflg >> 1 == True:
                pwm2.resetint()
                pwm2.set_KP_KI_KD(KP.get(),KI.get(),0)
                Theta_Set = theta2.get()*encticperrad*8
                pwm2.set_setpoint(Theta_Set)
                updatemotor.put(motflg&0b01)
                state=1

        if state != state1:
            print("Motor2 is at state "+str(state))
        state1 = state
                
        yield state

