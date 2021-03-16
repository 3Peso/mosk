import os
import socket
import time
import struct

REF_TIME_1970 = 2208988800  # Reference time
DEFAULT_TIME_SERVER = '0.de.pool.ntp.org'


def get_userfolders():
    """
    Generator which returns all user folders of the localhost.
    ONLY WORKS ON MAC
    """
    for f in os.scandir('/Users'):
        if f.is_dir():
            yield f


# from : https://stackoverflow.com/questions/36500197/python-get-time-from-ntp-server
def get_time(ntpserver=DEFAULT_TIME_SERVER):
    """
    Retrieves the current time from an NTP server.
    :param ntpserver: NTP Server to use. Default is 0.de.pool.ntp.org.
    :return: The current time.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, (ntpserver, 123))
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
    return time.ctime(t)
