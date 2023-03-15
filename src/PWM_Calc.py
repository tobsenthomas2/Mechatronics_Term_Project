import pyb
import time
import utime
#import serial
"""!Supply as an input the setpoint, the desired location of the motor.

Subtract the measured location of the motor from the setpoint; the difference is the error signal, a signed number indicating which way the motor is off and how far.

Multiply the error signal by a control gain called KP to produce a result called the actuation signal. The larger the error, the larger the actuation, so the harder the controller will push. The formula is
\mathrm{PWM} = K_p * (\theta_{setpoint} - \theta_{actual})

Send the actuation signal to the motor driver which you have already written to control the magnitude and direction of motor torque."""



class PWM_Calc:
    """!Class PWM_Calc: A class to implement a Proportional-Windup Controller.
The class stores the time, position, error, and PWM values and has functions
to set the controller's parameters, run the control loop, and print the stored
data to the serial port.

The constructor initializes the instance variables `KP_set`, `Theta_Set`, `time`, `position`, `error`, and `pwm` to 0.
"""
    
    def __init__(self,PWMmin,PWMcutoff):
        self.KP_set = 0
        self.KI_set = 0
        self.KD_set = 0
        self.Theta_Set = 0
        self.timelast = 0
        self.error_int = 0
        self.error_der = 0
        self.PWMmin = PWMmin
        self.PWMcutoff = PWMcutoff
   
    def set_KP_KI_KD(self, KP, KI, KD):
        """!set_KP

A function to set the proportional gain `KP` of the controller.

@param[in] `KP`: The proportional gain to set."""

     
        
        self.KP_set = float(KP)
        self.KI_set = float(KI)
        self.KD_set = float(KD)
        
    def set_setpoint(self, ThetaSet):
        """!#### set_setpoint

A function to set the setpoint `ThetaSet` of the controller.

@param[in] `ThetaSet`: The setpoint to set.
"""
        
        self.Theta_Set = float(ThetaSet)
        
    def resetint(self):
        self.error_int = 0
            
    def Run(self, Theta_Act):
        """!#### Run

A function that runs the control loop and updates the stored `time`, `position`, `error`, and `pwm` values.

@param[in] `Theta_Act`: The current position measurement.

Returns, the control output, `PWM`, as a float.
"""

        if self.timelast == 0:
            self.timelast = time.time()
        deltat = time.time()-self.timelast
        self.timelast = time.time()
        error = self.Theta_Set - Theta_Act
        #errorind = 0
        #self.error_der = (error-self.error[errorind])/0.05
        self.error_int += error*deltat
        PWM = (error)*self.KP_set + self.error_int*self.KI_set #- self.error_der*self.KD_set
        if PWM>self.PWMcutoff:
            PWM+=self.PWMmin-self.PWMcutoff
        elif PWM<-self.PWMcutoff:
            PWM-=self.PWMmin+self.PWMcutoff
        elif PWM ==0:
            PWM = 0
        else:
            PWM=PWM*self.PWMmin/self.PWMcutoff
        #PWM needs to be between 0-1 (0*100%)
        
        return PWM
        
        
    