import sys
import threading
import serial

def reader(s):
    print("Reader", s)
    while 1:
        r = s.read(1024)
        if r:
            print(r.decode())

def main(dev):
    s = serial.Serial(dev, baudrate=115200, rtscts=1, timeout=0.1)
    t = threading.Thread(target=reader, args=(s,))
    t.setDaemon(True)
    t.start()

    s.write(b"\x05")
    s.flush()

    while 1:
        line = input() + "\r\n"
        s.write(line.encode())
        s.flush()
        print("wrote", repr(line))

if __name__ == "__main__":
    main(*sys.argv[1:])
