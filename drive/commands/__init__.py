"""Just the basic commands for now."""
def forward(speed=0x10):
    return bytearray([
        0x86, 0x87,  # coast enabled
        0x8d, speed,  # right forward at speed
        0x89, speed  # left forward at speed
    ])


def stop():
    return bytearray([
        0x86, 0x87, # coast enabled
        0x8d, 0x0,  # right stop
        0x89, 0x0  # left stop
    ])
