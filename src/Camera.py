import time

class cam:
    def __init__():
        pass
    
    def scan():
        return 8
    
    def poscalc(camscan):
        return camscan

def Camera(shares):
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