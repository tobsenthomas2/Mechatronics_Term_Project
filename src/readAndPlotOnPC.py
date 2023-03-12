import sys
sys.path.append('c:/users/admin/anaconda3/lib/site-packages')
#issue: serial module not found --> pip show pyserial and add the path
import serial
import time
from matplotlib import pyplot

"""!
@file readAndPlotOnPC.py
This file contains functions which allows for the plotting of data that we read on our PC

@author Toby Darci, Tobias Thomas, Sydney Gothenquist
@date   2023-Mar-11 
"""

#cant start program from "usaual" python terminal --> use thonny python and use the following command
#& 'C:\Program Files (x86)\Thonny\python.exe' .\readAndPlotOnPC.py

"""!
 * @brief Plots data received from the serial port.
 * @param[in] input the data to be plotted.
"""
def plot_data(inputData):
    x = []
    y = []
    print("plot datat now")
    for dataToPlot in inputData:
        dataBuf=dataToPlot

        for line in dataBuf:
            #print(line)
            #data = line.split(',')
            data=line
            try:
                x_val = float(data[0])
                y_val = float(data[1])
                x.append(x_val)
                y.append(y_val)
            except ValueError:
                # ignore row if data is not a float
                pass
        if plot_data.plotNr%4==0 and plot_data.plotNr!=0:
            inputData()
            pyplot.figure()
            
        if  plot_data.plotNr%4==0:
            pyplot.plot(x, y,color='g',label="period=10")#label=str(plot_data.plotNr))
        elif plot_data.plotNr%4==1:
            pyplot.plot(x, y,color='b',label="period=40")#label=str(plot_data.plotNr))
        elif plot_data.plotNr%4==2:
            pyplot.plot(x, y,color='r',label="period=50")#label=str(plot_data.plotNr))
        elif plot_data.plotNr%4==3:
            pyplot.plot(x, y,color='y',label="period=60")#label=str(plot_data.plotNr))
        pyplot.legend(loc="upper left")
        pyplot.title("Plot")
        pyplot.xlabel("time [ms]")
        pyplot.ylabel("position [encoder ticks]")
        print("MAX Value: "+ str(max(y)))
        
        
            
        print("plot nr: " + str(plot_data.plotNr))
        plot_data.plotNr+=1
    pyplot.ion()
    pyplot.show()
    pyplot.pause(0.1)
    #sec = input('press Enter to receive a new dataset\n')
plot_data.plotNr=0

"""!
 Main function that reads and plots data from the serial port.
 """

with (serial.Serial("COM5",115200) as ser):

    morePlots=True
    plotCounter=0
    dataStorage=[]
    while morePlots:
        
        ser.flushInput()
        ser.flushOutput()
        data=[]
        dataStream=True
        while dataStream:
            buf=ser.readline ().split (b',')

            data.append(buf)
            if(buf==[b'99998', b'99998\r\n']):
                print("last plot. you can stop now")
                morePlots=False
            if buf==[b'99999', b'99999\r\n']:
                dataStream=False
                print("end this data set!")
                data.pop()
            
            #print(buf)
        dataStorage.append(data)
        plot_data(dataStorage)
        dataStorage=[]
        
    
    print("last dataset was sent! will stop listening now")
    input("press enter to exit")  



