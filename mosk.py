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

if __name__ == '__main__':
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, 'i:l:e:g:', ['instructions=', 'loglevel=', 'examiner=', 'globalplaceholders='])
    except getopt.GetoptError:
        print("mosk.py -i <instructionsfile> -l [CRITICAL]")
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
        elif opt in ('-g', '--globalplaceholders'):
            globalplaceholders = arg

    try:
        logger = logging.getLogger(__name__)
        collector = Collector.get_collector(instructionsfile=instructionsfile, examiner=examiner,
                                            placeholderfile=globalplaceholders)
        collector.collect()
        logger.info("Collection complete.")
    except NameError:
        print("The arguments 'instructionsfile', and 'examiner' are mandatory.")
        sys.exit(2)
    except FileNotFoundError:
        print('Could not initialize parser.')
        sys.exit(2)
