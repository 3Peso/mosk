"""
support module continaing tool functions for mosk
"""

__version__ = '0.0.6'
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


def get_collector_resources(resourcespath="./resources"):
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


def run_terminal_command(command, arguments):
    process = subprocess.Popen([command, arguments],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    return process.communicate()[0]
