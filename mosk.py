#!/usr/bin/env python3
import getopt
import sys

from businesslogic.log import LOG_LEVEL, setup_logging, mosk_logger
from instructionparsers.xmlparser import XmlParser
from businesslogic.collector import Collector
from protocol.logfileprotocol import LogFileProtocol


# TODO Refactoring run with logging in focus
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'i:l:e:', ['instructions=', 'loglevel=', 'examiner='])
    except getopt.GetoptError:
        print("mosk.py -i <instructionsfile> -l [CRITICAL")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-i', '--instructions'):
            instructionsfile = arg
        elif opt in ('-l', '--loglevel'):
            if arg in LOG_LEVEL.keys():
                setup_logging(arg)
            else:
                raise KeyError("'{}' not a valid log level.".format(arg))
        elif opt in ('-e', '--examiner'):
            examiner = arg

    try:
        collector = Collector.get_collector(instructionsfile=instructionsfile, examiner=examiner)
        collector.collect()
        mosk_logger.info("Collcetion complete.")
    except FileNotFoundError:
        print('Could not initialize parser.')
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
