import serial
ser = serial.Serial('/dev/ttyACM0',9600)


def read():
    read_serial = ser.readline()
    val1 = read_serial.split()      
    ret = [float(val1[0]), float(val1[1]), int(val1[2])]
    print(ret)
    return ret