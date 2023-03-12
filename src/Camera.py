import time
"""!
@file Camera.py
@brief Implementation of the `cam` and `Camera` classes.

@author Toby Darci, Tobias Thomas, Sydney Gothenquist
@date   2023-Mar-11 
    """

class cam:
    """! 
    @brief A class for the thermal camera
    This class implements the thermal camera from the ME405 kit to scan for data.
    """
    
    def __init__():
        """!
     @brief initializes the camera
     """
        pass
    
    def scan():
        """!
        @brief Scans for data with the thermal camera

        @return The data scanned by the thermal camera
        """
        return 8
    
    def poscalc(camscan):
        """!
        @brief Calculates the position based on the data scanned by the thermal camera

        This method calculates the position based on the data scanned by the thermal camera.

        @param camscan The data scanned by the thermal camera
        @return The position calculated based on the data scanned by the thermal camera
        """
        return camscan

def Camera(shares):
    """!
    @brief A function for controlling the camera

    This function controls the camera and updates its state.

    @param shares The shared variables for controlling the camera
    @return The state of the camera
    """
    updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI = shares
    state = 0
    state1 = 0
    while True:
        if state == 0:
            state = 1
        elif state == 1:
            angflg = updateang.get()
            if angflg == 0b11:
                camscan = cam.scan()
                pos = cam.poscalc(camscan)
                position.put(pos)
                updateang.put(angflg & 0b01)
        else:
            state = 0
            print("state out of range")
        if state != state1:
            print("Camera is at state "+str(state))
        state1 = state
        yield state