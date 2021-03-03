from collections import namedtuple

from baseclasses.artefact import ArtefactBase

from fritzconnection.lib.fritzhosts import FritzHosts
from fritzconnection.cli.utils import get_instance


class HostsRegisteredInFritzBox(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = "FritzBoxHosts"
        self.__collectionmethod = "fritzcollection.lib.hosts"
        self.__description = "Uses to Open Source Python module 'fritzconnection' by Klaus Bremer" \
                             "to collect the status of all registered hosts in a FritzBox network"

    def __str__(self):
        hosts = ""
        for host in self._collecteddata:
            hosts += "{}\n".format(host)
        return hosts

    # TODO Make parameters configurabel via XML and prompt for password if needed
    def collect(self):
        Args = namedtuple('Args', ['address', 'port', 'username', 'password', 'encrypt'])
        args = Args(address='192.168.178.1', port='49000', encrypt=False, username=None, password=input('Password: '))
        fho = get_instance(FritzHosts, args)
        self._collecteddata = self._get_status(fho)

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description

    @staticmethod
    def _get_status(fh):
        hosts = fh.get_hosts_info()
        for index, host in enumerate(hosts, start=1):
            status = 'active' if host['status'] else '-'
            ip = host['ip'] if host['ip'] else '-'
            mac = host['mac'] if host['mac'] else '-'
            hn = host['name']
            yield f'{index:>3}: {ip:<16} {hn:<28} {mac:<17}   {status}'

# TODO Implement a class to collect all FritzBox event logs and filter for certain signal words
