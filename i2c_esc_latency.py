import serial
import numpy as np
import matplotlib.pyplot as plt
import time

latency_end = 0

ser = serial.Serial('/dev/cu.usbmodem14101',9600)
time.sleep(3)
ser.flushInput()
ser.flushOutput()

data = []
latency_flag = 1

ser.flushInput()
ser.flushOutput()
command = 20
print('write spin')
ser.write((str(command)+'\n').encode()) #spin motor
# test below
input_byte = ser.readline()
string = input_byte.decode()
print('string_spin = ' + string);
# test above

input("Press Enter to begin reading")
#read serial for 5 seconds
start = time.time()
while (time.time() - start) <  5:
    ser.flushInput()
    ser.flushOutput()
    input_byte = ser.readline()
    string = input_byte.decode()
    string = string.rstrip()
    RPM = float(string)
    data.append(RPM)
    print(RPM)

# spin motor at second speed
ser.flushInput()
ser.flushOutput()
command+=20
ser.write((str(command)+'\n').encode()) #spin motor
latency_begin = time.time()

start = time.time()
while (time.time() - start) <  5:
    ser.flushInput()
    ser.flushOutput()
    input_byte = ser.readline()
    string = input_byte.decode()
    string = string.rstrip()
    RPM = float(string)
    data.append(RPM)
    if RPM > 2000:
        if latency_flag:
            latency_end = time.time()
            latency_flag = 0
    print(RPM)

#stop motor
ser.flushInput()
ser.flushOutput()
command = 0
print(command)
print('\n')
ser.write((str(command)+'\n').encode()) #spin motor
time.sleep(0.25)

plt.plot(data)
plt.xlabel('Time')
plt.ylabel('RPM')
plt.title('I2C Data')
plt.show()

print("Latency = ", latency_end-latency_begin)
ser.close()