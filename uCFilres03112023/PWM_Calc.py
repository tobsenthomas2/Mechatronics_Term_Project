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
    
    def __init__(self):
        self.KP_set = 0
        self.Theta_Set = 0
        self.time = []
        self.position = []
        self.error = []
        self.pwm = []
        
   
    def set_KP(self, KP):
        """!set_KP

A function to set the proportional gain `KP` of the controller.

@param[in] `KP`: The proportional gain to set."""

     
        
        self.KP_set = float(KP)

        
    def set_setpoint(self, ThetaSet):
        """!#### set_setpoint

A function to set the setpoint `ThetaSet` of the controller.

@param[in] `ThetaSet`: The setpoint to set.
"""
        
        self.Theta_Set = float(ThetaSet)
        

        
    def Run(self, Theta_Act):
        """!#### Run

A function that runs the control loop and updates the stored `time`, `position`, `error`, and `pwm` values.

@param[in] `Theta_Act`: The current position measurement.

Returns, the control output, `PWM`, as a float.
"""
        
        PWM = ((self.Theta_Set - Theta_Act)*self.KP_set)
        
        #PWM needs to be between 0-1 (0*100%)
        
        error = self.Theta_Set - Theta_Act
        
        self.time.append(utime.ticks_ms())
        self.position.append(Theta_Act)
        self.error.append(error)
        self.pwm.append(PWM)
        
        return PWM
    

    
    def Print_Data(self):
        """! Print_Data

A function that prints the stored `time`, `position`, `error`, and
`pwm` values to the serial port. The data is sent as comma-separated
values, with each data point in a separate line. The function sends two
flags to indicate to the receiver when all the data has been sent.

##### Raises

An exception if an error occurs while sending the data."""

        
        try: 
            u2 = pyb.UART(2, baudrate=115200)      # Set up the second USB-serial port

            for i in range(len(self.time)):
                    t = self.time[i]-self.time[0]
                    x = self.position[i]
                    u2.write(f"{t},{x}\r\n")       #Write bytes, not a string
                
            #flag to tell PC last data point
            u2.write(f"99999,99999\r\n")
            
            #send double for flag2 to tell PC last dataset --> no more plots
            #u2.write(f"99999,99999\r\n")
        except:
            print("An exception occurred. Sending Data didnt work")


        
        
    