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



def getvalArr (inputArr):
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

# def initArrVal(initValues):
#     initAver=456
#     deviArr=initValues
#     index=0
#     for val in initValues:
#         deviArr[index]=val-440
#         index=index+1
#     return deviArr
#         
#         
def getPositionIndex(image):
    """!
    @brief   calculates the index to get the right position for our 64 different options
    @details This function calculates with a fixed offset the position we want to go
    @param   camera image
    @return position we want to aim 
    """
    #average of the deviation per pixle block
    deviArr=[151,155,139,125,127,128,140,157,142,132,124,128,127,128,140,125,133,124,122,117,118,101,142,129,133,133,114,121,132,116,116,122,137,123,123,118,102,106,102,114,133,126,115,120,128,8,12,10,125,136,105,109,113,113,115,104,115,114,118,112,110,114,110,113]
    array=camera.get_2DArray(image.v_ir, limits=(0, 99))
    valArray=getvalArr(array)
    index=0
    for val in valArray:
        valArray[index]=val-deviArr[index]
        index=index+1
    print (valArray)
    return valArray.index(max(valArray))


def printDataWithSTM32(data):
    """!
    @brief   sends sata over the stm32 serial port
    @details sends sata over the stm32 serial port and not over te serial port of the shoe
    @param   string you want to send
     
    """
    try: 
                u2 = pyb.UART(2, baudrate=115200)      # Set up the second USB-serial port

                u2.write(data)       #Write bytes, not a string
               
                
    except:
                print("An exception occurred. Sending Data didnt work")

def printDirection(index_max):
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

    def ascii_image(self, array, pixel="██", textcolor="0;180;0"):
        """!
        @brief   Show low-resolution camera data as shaded pixels on a text
                 screen.
        @details The data is printed as a set of characters in columns for the
                 number of rows in the camera's image size. This function is
                 intended for testing an MLX90640 thermal infrared sensor.

                 A pair of extended ACSII filled rectangles is used by default
                 to show each pixel so that the aspect ratio of the display on
                 screens isn't too smushed. Each pixel is colored using ANSI
                 terminal escape codes which work in only some programs such as
                 PuTTY.  If shown in simpler terminal programs such as the one
                 used in Thonny, the display just shows a bunch of pixel
                 symbols with no difference in shading (boring).

                 A simple auto-brightness scaling is done, setting the lowest
                 brightness of a filled block to 0 and the highest to 255. If
                 there are bad pixels, this can reduce contrast in the rest of
                 the image.

                 After the printing is done, character color is reset to a
                 default of medium-brightness green, or something else if
                 chosen.
        @param   array An array of (self._width * self._height) pixel values
        @param   pixel Text which is shown for each pixel, default being a pair
                 of extended-ASCII blocks (code 219)
        @param   textcolor The color to which printed text is reset when the
                 image has been finished, as a string "<r>;<g>;<b>" with each
                 letter representing the intensity of red, green, and blue from
                 0 to 255
        """
        minny = min(array)
        scale = 255.0 / (max(array) - minny)
        for row in range(self._height):
            for col in range(self._width):
                pix = int((array[row * self._width + (self._width - col - 1)]
                           - minny) * scale)
                print(f"\033[38;2;{pix};{pix};{pix}m{pixel}", end='')
            print(f"\033[38;2;{textcolor}m")


    ## A "standard" set of characters of different densities to make ASCII art
    asc = " -.:=+*#%@"

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
                        pix=pix #this is a hardware specific fix, because there are dead pixles
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
    #print(f"I2C Scan: {scanhex}")

    # Create the camera object and set it up in default mode
    camera = MLX_Cam(i2c_bus)
    
    #24x32 Pixel
    #Idea--> 3x4 Pixel arrays (8 fixed positions) --> calculating the average and aim to thqt point
    #enemy can move for 5 s then freeze for 10s
    #we should do the calc every second and if nobody is moving it should be in the same pixle array and we can start shooting as often as we can
    #should we do fixed positions? would be the easiest and less calculation.
    
    #code to init the val array:
    #image = camera.get_image()
    #array=getvalArr(camera.get_2DArray(image.v_ir, limits=(0, 99)))
    #deviArr=initArrVal(array)
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

            
            index_max = getPositionIndex(image)
            #print(array)
            print ("thats the highest index! " )
            print(index_max)
            #print (valArray)
            printDirection(index_max)
          
                
            show_image=True
            if show_image:
                 camera.ascii_image(image.buf)
 
            time.sleep_ms(1000)

        except KeyboardInterrupt:
            break

    print ("Done.")
    
    

## @endcond End the block which Doxygen should ignore


