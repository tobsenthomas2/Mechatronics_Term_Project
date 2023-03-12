import math
width_tot = 48
length_tot = 200
yaw_init = math.pi
pitch_init = 0
height_gun = 12
height_tot = 36
yaw = []
pitch = []
for i in range(8):
    yaw.append(yaw_init-math.atan((width_tot*(0.5+i)/8-width_tot/2)/length_tot))
    pitch.append(pitch_init+math.atan((height_tot*(0.5+i)/8-height_gun)/length_tot))
print(yaw)
print(pitch)
def angle(pos):
    posoct = oct(pos+int('10',8))[2:]
    position = [int(i) for i in posoct]
    yawindex = position[0]-1
    pitchindex = position[1]-1
    yawang = yaw[yawindex]
    pitchang = pitch[pitchindex]
    return(yawang, pitchang)

position = 10
posoct = oct(position+int('10',8))
print(posoct)
yawang,pitchang = angle(position)
print(yawang)
print(pitchang)