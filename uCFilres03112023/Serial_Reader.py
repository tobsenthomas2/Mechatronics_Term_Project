import serial
import matplotlib.pyplot as plt

def main():
    with serial.Serial ('COM3', baudrate=115200) as s_port:
        #input1 = input('kp Value ')
            while (True):
                s_port.write(b'something')
                print("cycled")
        
        #x = s_port.readline()
        #print(x)
        
'''
    while (True):              
        try:
            with serial.Serial ('COM3', 115200) as s_port:     
                data_array.append(s_port.readline().replace(b" ", b"").strip().split(b","))
        
        except UnicodeError: #run and see what error happens
            break
                     
    float_array = []
    float_list = []

    for line in data_array:
        for val in line:
            try:
                data_float = float(val)
                float_list.append(data_float)
            except ValueError:
                break
            except IndexError:
                break
        if(len(float_list) > 1):
            float_array.append(float_list) 
        float_list = []
    
    x_data = [row[0] for row in float_array]
    y_data = [row[1] for row in float_array]
    
    plt.plot(x_data, y_data)
    plt.suptitle('Proportional Control Response')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.show()
'''

if __name__ == "__main__":
    main()