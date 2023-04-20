import os

def is_raspberry_pi():
    """
    Returns True if the current platform is a Raspberry Pi, otherwise False.
    """
    return False
    #return os.uname().nodename == 'raspberrypi'
