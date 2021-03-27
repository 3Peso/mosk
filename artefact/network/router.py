"""
mosk network module for classes collecting router information through a network.
"""

__version__ = '0.0.3'
__author__ = '3Peso'
__all__ = ['HostsRegisteredInFritzBox']

import requests.exceptions
import getpass
from collections import namedtuple

from baseclasses.artefact import ArtefactBase
from businesslogic.support import str_to_bool

from fritzconnection.lib.fritzhosts import FritzHosts
from fritzconnection.cli.utils import get_instance


Host = namedtuple('Host', ['Index', 'IP', 'HostName', 'MacAddress', 'Status'])


class HostsRegisteredInFritzBox(ArtefactBase):
    """
    Retrieve a list of all hosts currently registered at a FritzBox router using the provided
    API and the OpenSource Python module "fritzconnection", https://pypi.org/project/fritzconnection/.
    """
    ADDRESS_PARAMETER = 'address'
    PORT_PARAMETER = 'port'
    USERNAME_PARAMETER = 'username'
    ENCRYPT_PARAMETER = 'encrypt'

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

    def __str__(self):
        hosts = ''

        if self.data[0].collecteddata is not None:
            for host in self.data[0].collecteddata:
                hosts += f'{host.Index:>3}: {host.IP:<16} {host.HostName:<28} {host.MacAddress:<17}   {host.Status}\n'
        else:
            hosts += "No hosts retrieved."
        hosts = self.data[0].get_metadata_as_str(hosts)

        return hosts

    # TODO Make parameters configurabel via XML and prompt for password if needed
    # TODO Currently encrypted transfare of credentials to fritzbox does not work
    def collect(self):
        Args = namedtuple('Args', ['address', 'port', 'username', 'password', 'encrypt'])
        params = self._get_parameters()

        username = None
        if HostsRegisteredInFritzBox.USERNAME_PARAMETER in params.keys():
            username = params[HostsRegisteredInFritzBox.USERNAME_PARAMETER]

        args = Args(address=params[HostsRegisteredInFritzBox.ADDRESS_PARAMETER],
                    port=params[HostsRegisteredInFritzBox.PORT_PARAMETER],
                    encrypt=str_to_bool(params[HostsRegisteredInFritzBox.ENCRYPT_PARAMETER]),
                    username=username,
                    password=getpass.getpass('Password: '))
        try:
            fho = get_instance(FritzHosts, args)
        except requests.exceptions.ConnectionError:
            self.data = None
        else:
            self.data = self._get_status(fho)

    def _get_parameters(self):
        params = [HostsRegisteredInFritzBox.ADDRESS_PARAMETER, HostsRegisteredInFritzBox.USERNAME_PARAMETER,
                  HostsRegisteredInFritzBox.PORT_PARAMETER, HostsRegisteredInFritzBox.ADDRESS_PARAMETER,
                  HostsRegisteredInFritzBox.ENCRYPT_PARAMETER]
        return {k: self.get_parameter(k) for k in params if k in self._parameters.keys()}

    @staticmethod
    def _get_status(fh):
        hosts = fh.get_hosts_info()
        for index, host in enumerate(hosts, start=1):
            status = 'active' if host['status'] else '-'
            ip = host['ip'] if host['ip'] else '-'
            mac = host['mac'] if host['mac'] else '-'
            hn = host['name']
            yield Host(Index=index, IP=ip, MacAddress=mac, HostName=hn, Status=status)
