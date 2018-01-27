import serial


def readorientation():
    with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as conn:
        conn.write(bytearray([0x13]))  # 16-bit direction
        dir_bytes = conn.read(2)
        return int.from_bytes(dir_bytes, byteorder='big') / 10


if __name__ == '__main__':
    print(readorientation())

