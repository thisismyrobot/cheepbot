"""Just the basic commands for now."""
def forward(speed=0x10):
    return bytearray([0x8d, speed, 0x89, speed])


def stop():
    return bytearray([0x8d, 0x0, 0x89, 0x0])
