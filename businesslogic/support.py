"""
support module continaing tool functions for mosk
"""

__author__ = '3Peso'

import json
import locale
import logging
import os
import socket
import sys
import time
import struct
import hashlib
import subprocess


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
def get_time(ntpserver: str = DEFAULT_TIME_SERVER):
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


def str_to_bool(boolstring: str):
    """
    Translate a string into a real boolean value.
    :param boolstring:
    Any string. But original intention was the usage of the strings "False" and "True".
    :return:
    Returns True for the string "True" and False for the string "False".
    Returns True for any nonempty string and False for an empty string or for None.
    """
    if isinstance(boolstring, str) or boolstring is None:
        if boolstring == 'True':
            return True
        if boolstring == 'False':
            return False
        elif boolstring == '' or boolstring is None:
            return False
        else:
            return True
    else:
        raise TypeError('Only strings and None are supported.')


# From https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def md5(fpath: str = "", data: str = ""):
    """
    Calculates the the MD5 hash of a file.
    You can only provide a file path OR a data string, not both.
    :param fpath: Path of the file for which the MD5 hash is required.
    :param data: Data string for which the MD5 hash should be calculated.
    :return: Returns the string representation of the MD5 hash.
    """
    if fpath is not None and fpath != "" and data is not None and data != "":
        raise ValueError("You can only provide a file OR a data string to calculate the MD5 hash.")

    logger = logging.getLogger(__name__)
    hash_md5 = hashlib.md5()
    if fpath is not None and fpath != "":
        logger.debug(f"Calculating MD5 hash for '{fpath}'.")
        with open(fpath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    elif data is not None and data != "":
        logger.debug(f"Calculating MD5 hash for string '{data}'.")
        bvalue = data.encode('ascii')
        chunks = _chunkstring(bvalue, 4096)
        for chunk in chunks:
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def _chunkstring(string: str, length: int):
    return (string[0 + i:length + i] for i in range(0, len(string), length))


def get_collector_resources(resourcespath: str = "./resources"):
    logger = logging.getLogger(__name__)
    countrycode, _ = locale.getdefaultlocale()
    resources = None

    resourcesfilepath = os.path.join(resourcespath, f"collector_text_{countrycode}.json")
    logger.debug("Trying to load text resources from '{} ...'".format(resourcesfilepath))
    # TODO Move into a contextmanager
    # HACK
    # Do the following steps to ensure we are operating in the root directory of mosk
    # so that os.abspath works
    # IMPORTANT: Depends on support module stored one level above root
    old_wd = _change_cwd_to_module_root()
    resourcesfilepath = os.path.abspath(resourcesfilepath)
    os.chdir(old_wd)

    if os.path.exists(resourcesfilepath):
        try:
            with open(resourcesfilepath) as rf:
                resources = json.load(rf)
        except FileNotFoundError:
            if countrycode is None:
                logger.warning('Default resources file not found.')
            else:
                logger.info(f'Resources file for country code {countrycode} not found.')

    return resources


def _change_cwd_to_module_root():
    basepath = os.path.dirname(sys.modules[__name__].__file__)
    old = os.getcwd()
    os.chdir(basepath)
    os.chdir('..')
    return old


def run_terminal_command(arguments: list):
    process = subprocess.Popen(arguments,
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    return process.communicate()[0]


def format_bytes(size: int):
    """
    Calculate more human readable values for byte sizes
    :param size: Will support sizes up to terra bytes. Afterwards all is returned as terra bytes.
    :return: string <calculatedsize><unit> for example "1MB"
    """
    power = 1024
    n = 0
    max_unit = 4
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size >= power and n < max_unit:
        size /= power
        n += 1
    return f"{round(size,2)}{power_labels[n]+'B'}"
