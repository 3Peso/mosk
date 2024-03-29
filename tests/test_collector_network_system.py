import logging
import platform
from unittest import TestCase


from artefact.network.system import TimeFromNTPServer


class TestTimeFromNTPServerCollect(TestCase):
    def test__collect_invalid_ntp_server_address(self):
        """
        Should give back data object with the message informing about a runtime exception.
        :return:
        """
        expected_ntp_server = 'invalid.address.invi'
        expected_data = "Could not retrieve network time because of a runtime exception. " \
                        "socket.gaierror message: nodename nor servname provided, or not known"
        if platform.system() == "Windows":
            expected_data = "Could not retrieve network time because of a runtime exception. " \
                            "socket.gaierror message: getaddrinfo failed"

        actual_colletor = TimeFromNTPServer(parameters={}, parent=None)
        actual_colletor.timeserver = expected_ntp_server

        try:
            logging.disable(logging.ERROR)
            actual_colletor._collect()
        finally:
            logging.disable(logging.NOTSET)

        self.assertEqual(str(actual_colletor.data[0].collecteddata), expected_data)

    def test__collect_no_network_connection(self):
        """
        Should raise exception.
        :return:
        """
        import socket

        _ = socket.socket
        try:
            # Monkey patch the socket to simulate a broken network connection.
            def guard(*args, **kwargs):
                raise socket.error("Connection down")
            socket.socket = guard

            expected_ntp_server = '0.de.pool.ntp.org'
            actual_collector = TimeFromNTPServer(parameters={}, parent=None)
            actual_collector.timeserver = expected_ntp_server

            self.assertRaises(socket.error, actual_collector._collect)
        finally:
            socket.socket = _
