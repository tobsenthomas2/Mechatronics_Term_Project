"""!
@file mlx_cam.py
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

def printDataWithSTM32(data):
    try: 
                u2 = pyb.UART(2, baudrate=115200)      # Set up the second USB-serial port

                u2.write(data)       #Write bytes, not a string
               
                
    except:
                print("An exception occurred. Sending Data didnt work")


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
        self._image = self._camera.image


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
                if row==15:
                    if col==30 or col==29 or col==27 or col==25 or col==22 or col==23:
                        pix=47 #this is a hardware specific fix, because there are dead pixles
                dataArray[rowix][colix]=pix

                colix=colix+1
            rowix=rowix+1
        return dataArray




    def get_image(self):
        """!
        @brief   Get one image from a MLX90640 camera.
        @details Grab one image from the given camera and return it. Both
                 subframes (the odd checkerboard portions of the image) are
                 grabbed and combined. This assumes that the camera is in the
                 ChessPattern (default) mode as it probably should be.
        @returns A reference to the image object we've just filled with data
        """
        for subpage in (0, 1):
            while not self._camera.has_data:
                time.sleep_ms(50)
                print('.', end='')
            self._camera.read_image(subpage)
            state = self._camera.read_state()
            image = self._camera.process_image(subpage, state)

        return image


## @cond NO_DOXY don't document the test code in the driver documentation
if __name__ == "__main__":

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
    
    #24x32 Pixel
    #Idea--> 3x4 Pixel arrays (8 fixed positions) --> calculating the average and aim to thqt point
    #enemy can move for 5 s then freeze for 10s
    #we should do the calc every second and if nobody is moving it should be in the same pixle array and we can start shooting as often as we can
    #should we do fixed positions? would be the easiest and less calculation.
    while True:
        try:
            # Get and image and see how long it takes to grab that image
            #print("Click.", end='')
            #begintime = time.ticks_ms()
            image = camera.get_image()
            #print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")

            # Can show image.v_ir, image.alpha, or image.buf; image.v_ir best?
            # Display pixellated grayscale or numbers in CSV format; the CSV
            # could also be written to a file. Spreadsheets, Matlab(tm), or
            # CPython can read CSV and make a decent false-color heat plot.

            array=camera.get_2DArray(image.v_ir, limits=(0, 99))
            valArray=[0]*8
            for arrNr in range(8):              
                for row in range(3):
                    for col in range (4):
                        valArray[arrNr]=valArray[arrNr]+array[row][col+(4*arrNr)]
            index_max = valArray.index(max(valArray))
            #print(array)
            print ("thats the highest index! " )
            print(index_max)
            print (valArray)

 
            time.sleep_ms(1000)

        except KeyboardInterrupt:
            break

    print ("Done.")
    
    

## @endcond End the block which Doxygen should ignore


