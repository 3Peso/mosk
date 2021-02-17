#!/usr/bin/env python3
import logging
import getopt
import sys

from businesslogic.collector import Collector


LOG_LEVEL = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}


# TODO Refactoring run with logging in focus.
# Use https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/ as basis.
# TODO doctest tests with doctest file (see "How the Tombola subclasses were tested" in the Python books
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
                logging.basicConfig(level=LOG_LEVEL[arg], format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')
            else:
                raise KeyError("'{}' not a valid log level.".format(arg))
        elif opt in ('-e', '--examiner'):
            examiner = arg

    try:
        logger = logging.getLogger(__name__)
        collector = Collector.get_collector(instructionsfile=instructionsfile, examiner=examiner)
        collector.collect()
        logger.info("Collection complete.")
    except FileNotFoundError:
        print('Could not initialize parser.')
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
