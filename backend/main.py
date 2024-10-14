from serial import Serial

# sudo systemctl stop serial-getty@ttyS0.service

ser = Serial("/dev/serial0", 115200)
ser.flushInput()
ser.flushOutput()
print("Starting")
while True:
    data = ser.readline()
    if data.decode() != "\n":
        print(data.decode()[:-1])