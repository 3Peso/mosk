"""
support module continaing tool functions for mosk
"""

__version__ = '0.0.1'
__author__ = '3Peso'

import os
import socket
import time
import struct
import hashlib

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


def str_to_bool(boolstring):
    """
    Translate a string into a real boolean value.
    :param boolstring:
    Any string. But original intention was the usage of the strings "False" and "True".
    :return:
    Returns True for the string "True" and False for the string "False".
    Returns True for any nonempty string and False for an empty string or for None.
    """
    if boolstring == 'True':
        return True
    if boolstring == 'False':
        return False
    elif boolstring == '' or boolstring is None:
        return False
    else:
        return True


# From https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def md5(fpath):
    """
    Calculates the the MD5 hash of a file.
    :param fpath: Path of the file for which the MD5 hash is required.
    :return: Returns the string representation of the MD5 hash.
    """
    hash_md5 = hashlib.md5()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
