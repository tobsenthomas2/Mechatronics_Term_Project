"""!
@file mlx_cam.py

RAW VERSION
This version uses a stripped down MLX90640 driver which produces only raw data,
not calibrated data, in order to save memory.

This file contains a wrapper that facilitates the use of a Melexis MLX90640
thermal infrared camera for general use. The wrapper contains a class MLX_Cam
whose use is greatly simplified in comparison to that of the base class,
@c class @c MLX90640, by mwerezak, who has a cool fox avatar, at
@c https://github.com/mwerezak/micropython-mlx90640

To use this code, upload the directory @c mlx90640 from mwerezak with all its
contents to the root directory of your MicroPython device, then copy this file
to the root directory of the MicroPython device.

There's some test code at the bottom of this file which serves as a beginning
example.

@author mwerezak Original files, Summer 2022
@author JR Ridgely Added simplified wrapper class @c MLX_Cam, January 2023
@copyright (c) 2022 by the authors and released under the GNU Public License,
    version 3.
"""

import utime as time
from machine import Pin, I2C
from mlx90640 import MLX90640
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern



class MLX_Cam:
    """!
    @brief   Class which wraps an MLX90640 thermal infrared camera driver to
             make it easier to grab and use an image.
    """

    def __init__(self, i2c, address=0x33, pattern=ChessPattern,
                 width=NUM_COLS, height=NUM_ROWS):
        """!
        @brief   Set up an MLX90640 camera.
        @param   i2c An I2C bus which has been set up to talk to the camera;
                 this must be a bus object which has already been set up
        @param   address The address of the camera on the I2C bus (default 0x33)
        @param   pattern The way frames are interleaved, as we read only half
                 the pixels at a time (default ChessPattern)
        @param   width The width of the image in pixels; leave it at default
        @param   height The height of the image in pixels; leave it at default
        """
        ## The I2C bus to which the camera is attached
        self._i2c = i2c
        ## The address of the camera on the I2C bus
        self._addr = address
        ## The pattern for reading the camera, usually ChessPattern
        self._pattern = pattern
        ## The width of the image in pixels, which should be 32
        self._width = width
        ## The height of the image in pixels, which should be 24
        self._height = height

        # The MLX90640 object that does the work
        self._camera = MLX90640(i2c, address)
        self._camera.set_pattern(pattern)
        self._camera.setup()

        ## A local reference to the image object within the camera driver
        self._image = self._camera.raw
    
    def get_2DArray(self, array, limits=None):
        """!
        @brief   Generate a 2D Array with data
        @details This function generates a 2D-Array, with all the data with the right offset and scale. The lines can
                 be printed or saved to a file using a @c for loop.
        @param   array The array of data to be presented
        @param   limits A 2-iterable containing the maximum and minimum values
                 to which the data should be scaled, or @c None for no scaling
        """
        if limits and len(limits) == 2:
            scale = (limits[1] - limits[0]) / (max(array) - min(array))
            offset = limits[0] - min(array)
        else:
            offset = 0.0
            scale = 1.0
        dataArray=[[0 for j in range(32)] for i in range(24)]
        
        rowix=0
        for row in range(self._height):
            colix=0
            for  col in range(self._width):
                pix = int((array[row * self._width + (self._width - col - 1)]
                          * scale) + offset)
                dataArray[rowix][colix]=pix
                colix=colix+1
            rowix=rowix+1
        return dataArray


    def get_image(self):
        """!
        @brief   Get one image from a MLX90640 camera.
        @details Grab one image from the given camera and return it. Both
                 subframes (the odd checkerboard portions of the image) are
                 grabbed and combined (maybe; this is the raw version, so the
                 combination is sketchy and not fully tested). It is assumed
                 that the camera is in the ChessPattern (default) mode as it
                 probably should be.
        @returns A reference to the image object we've just filled with data
        """
        for subpage in (0, 1):
            while not self._camera.has_data:
                time.sleep_ms(50)
                print('.', end='')
                                            
            image = self._camera.read_image(subpage)
                                                              

        return image
    def printDirection(self,index_max):
        """!
        @brief   prints a map with the position the object stands
        @details prints out a map with the position. X is the location and 0s are the other options we could aim to
        @param   position index
         
        """
        #the map is morrowed --> on the right hand site means the object is on the left hand side
        aiming=""
        
        for x in range(index_max-1):
            if x%8 ==0:
                aiming=aiming+"\n"
            aiming=aiming+"0"
        aiming=aiming+"X"
        for x in range(index_max,64):
            if x%8 ==0 and x>0:
                aiming=aiming+"\n"
            aiming=aiming+"0"
        print(aiming)
        return

    def getvalArr (self,inputArr):
        """!
        @brief   Generate a Array with Values of the average 3x4 Pixel block
        @details This function generates a 2D-Array, with all the data with the right offset and scale. There are 64 different values with the values
        of the whole Pixel block to get the position
        @param   array The array of data to be added
        @return value Array with size 64 with the sum of the Pixel Block 
        """
        valArray=[0]*64
        for arrNr in range(64):              
            for row in range(3):
                for col in range (4):
                    valArray[arrNr]=valArray[arrNr]+inputArr[row+((int(arrNr/8))*3)][col+(4*(arrNr%8))]
                                
        return valArray

    def getPositionIndex(self,image):
        """!
        @brief   calculates the index to get the right position for our 64 different options
        @details This function calculates with a fixed offset the position we want to go
        @param   camera image
        @return position we want to aim 
        """
        #average of the deviation per pixle block
        deviArr=[151,155,139,125,127,128,140,157,142,132,124,128,127,128,140,125,133,124,122,117,118,101,142,129,133,133,114,121,132,116,116,122,137,123,123,118,102,106,102,114,133,126,115,120,128,8,12,10,125,136,105,109,113,113,115,104,115,114,118,112,110,114,110,113]
        array=self.get_2DArray(image)#, limits=(0, 99))
       
        valArray=self.getvalArr(array)
        index=0
        for val in valArray:
            valArray[index]=val-deviArr[index]
            index=index+1
        return valArray.index(max(valArray))

def cameraFN (shares):
    
    updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI = shares
    
    # The following import is only used to check if we have an STM32 board such
    # as a Pyboard or Nucleo; if not, use a different library
    try:
        from pyb import info

    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)

    print("MXL90640 Easy(ish) Driver Test")

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    print(f"I2C Scan: {scanhex}")

    # Create the camera object and set it up in default mode
    camera = MLX_Cam(i2c_bus)
    state = 0
    state1 = 0
    while True:
        if state == 0:
            state = 1
        elif state == 1:
            angflg = updateang.get()
            if angflg == 0b11:
                image = camera.get_image()
                pos = camera.getPositionIndex(image)                
                #camera.printDirection(pos)#for debug
                position.put(pos)
                updateang.put(angflg & 0b01)
        else:
            state = 0
            print("state out of range")
        if state != state1:
            print("Camera is at state "+str(state))
        state1 = state
        yield state
    


## @endcond End the block which Doxygen should ignore


