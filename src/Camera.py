def Camera(shares)
    stuff = shares
    state = 0
    while True:
        if state == 0:
            state = 1
            picarray = []
            imgsize = 24*32
            camscan = cam.scan()
        elif state == 1:
            #Off
            if cameraon.get == True:
                state = 2
        elif state == 2:
            #Getting image
            camchunk = next(camscan)
            picarray.append(camchunk)
            if len(picarray)==imgsize:
                state = 3
        elif state == 3:
            pos = cam.poscalc(picarray)
            if pos != position.get()
                updateang.put(0b01)
                position.put(pos)
            if cameraon.get == False:
                state = 1
        else
            state = 0
            print("state out of range")
            
        yield state