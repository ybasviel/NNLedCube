import serial
from pathlib import Path


class LedCube():
    def __init__(self, port:Path|str):
        self.ser = serial.Serial(port, 115200)
    
    def write(self, buff):
        send_str = ''.join(chr(int(bit)) for bit in buff)

        self.ser.write(send_str.encode())
        self.ser.flush()

    def reset(self):
        self.ser.write((chr(255)).encode())
        self.ser.flush()

    def close(self):
        self.ser.close()


if __name__ == '__main__':
    
    from time import sleep
    
    
    led = LedCube('/dev/ttyUSB0')
    sleep(2)

    for x in [0, 8, 16, 24, 32, 40, 48, 64, 72, 80, 88, 96, 104, 112, 127]:
        buff = np.ones(64)
        buff *= x

        print(f'intensity: {x}')
        
        led.write(buff)

        sleep(0.3)
