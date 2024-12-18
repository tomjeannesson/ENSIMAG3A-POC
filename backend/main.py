import json
from pathlib import Path

from serial import Serial

# sudo systemctl stop serial-getty@ttyS0.service
# /etc/systemd/system/poc.service
# sudo systemctl start poc.service

ser = Serial("/dev/serial0", 115200)
ser.flushInput()
ser.flushOutput()
print("Starting")

data_file_path = Path(__file__).parent / "data.json"
with open(data_file_path, "w") as f:
    json.dump(0, f)
while True:
    data = ser.readline()
    if data.decode() != "\n":
        with open(data_file_path, "w") as f:
            json.dump(data.decode()[:-2], f)
            print(data.decode()[:-2])
