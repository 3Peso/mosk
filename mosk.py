#!/usr/bin/env python3
import logging
import getopt
import sys

import businesslogic.log
from businesslogic.log import LOG_LEVEL
from businesslogic.collector import Collector


module_logger = logging.getLogger(__name__)


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
                logging.basicConfig(level=LOG_LEVEL[arg])
            else:
                raise KeyError("'{}' not a valid log level.".format(arg))
        elif opt in ('-e', '--examiner'):
            examiner = arg

    try:
        collector = Collector.get_collector(instructionsfile=instructionsfile, examiner=examiner)
        collector.collect()
        module_logger.info("Collection complete.")
    except FileNotFoundError:
        print('Could not initialize parser.')
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
