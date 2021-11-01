"""
support module continaing tool functions for mosk
"""

__author__ = '3Peso'
__all__ = ['get_userfolders', 'md5', 'run_terminal_command', 'str_to_bool', 'format_bytes',
           'validate_file_signature']


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
from logging import Logger

import chardet

from businesslogic.errors import MD5SupportError, NoStringResourcesError, NoCountryCodeError


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
    client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    socket_error = None
    t = None
    try:
        client.sendto(data, (ntpserver, 123))
        data, address = client.recvfrom(1024)
        if data:
            t = struct.unpack('!12I', data)[10]
            t -= REF_TIME_1970
    except socket.gaierror as so_err:
        socket_error = so_err
    finally:
        if client is not None:
            client.close()
        if socket_error is not None:
            raise socket_error

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
        raise MD5SupportError("You can only provide a file OR a data string to calculate the MD5 hash.")

    logger: Logger = logging.getLogger(__name__)
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
    countrycode, _ = locale.getdefaultlocale()
    resources = None
    resourcesfilepath = _get_resources_path(resourcespath, countrycode)
    resources = _load_resources(resourcesfilepath, countrycode)
    if resources is None:
        resourcesfilepath = _get_resources_path(resourcespath, 'None')
        resources = _load_resources(resourcesfilepath, countrycode)

    return resources


class ChangeToModuleRoot:
    def __init__(self):
        self._original_working_dir = os.getcwd()

    def __enter__(self):
        self._change_cwd_to_module_root()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.chdir(self._original_working_dir)

    @staticmethod
    def _change_cwd_to_module_root():
        basepath: str = os.path.dirname(sys.modules[__name__].__file__)
        os.chdir(basepath)
        os.chdir('..')


def _get_resources_path(resourcespath: str, countrycode: str):
    logger: Logger = logging.getLogger(__name__)
    if resourcespath == '':
        raise NoStringResourcesError('Resources path is empty.')
    if countrycode == '':
        raise NoCountryCodeError('Country code is empty.')
    resourcesfilepath = os.path.join(resourcespath, f"collector_text_{countrycode}.json")
    logger.debug("Trying to load text resources from '{} ...'".format(resourcesfilepath))
    # Do the following steps to ensure we are operating in the root directory of mosk
    # so that os.abspath works
    # Depends on support module stored one level above root
    with ChangeToModuleRoot():
        resourcesfilepath = os.path.abspath(resourcesfilepath)

    return resourcesfilepath


def _load_resources(resourcesfilepath: str, countrycode: str):
    if resourcesfilepath == '':
        raise NoStringResourcesError('Resourcefilepath is empty.')
    logger = logging.getLogger(__name__)
    resources = None
    if os.path.exists(resourcesfilepath):
        try:
            with open(resourcesfilepath) as rf:
                resources = json.load(rf)
        except json.decoder.JSONDecodeError as json_error:
            if json_error.msg == "Expecting value":
                logger.info(f'Resource file for country code {countrycode} is empty.')
        except FileNotFoundError:
            if countrycode is None:
                logger.warning('Default resources file not found.')
            else:
                logger.info(f'Resources file for country code {countrycode} not found.')

    return resources


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


def validate_file_signature(filepath: str) -> bool:
    """
    Takes a file path, calculates its MD5 hash and compares this hash to the provided hash
    the file should have.
    Expects that in the folder of the file to check also is a file called <file>.md5 which contains
    the expected hash.
    :param filepath:
    :return: Returns True if the hash of the file is the same as the implicitely provided hash.
    """
    file_, file_ext = os.path.splitext(filepath)

    signature_file:str = f"{file_}.md5"
    if not os.path.exists(signature_file):
        return False

    # MD5 hashes are 128 bit long. Just roughly check for the size 32,
    # for UTF8, for typical Windows encoding of textfiles,
    # or 16 ASCII encoding.
    if os.stat(signature_file).st_size != 32 and os.stat(signature_file).st_size != 16:
        return False
    with open(signature_file) as sig_file:
        signature = sig_file.read()
        if md5(filepath) != signature:
            return False

    return True
