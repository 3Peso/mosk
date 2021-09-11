#!/usr/bin/env python3
import logging
import sys
import os

import click

from businesslogic.collector import Collector


LOG_LEVEL = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}


def is_globalplaceholder_valid(placeholderpath):
    return os.path.exists(placeholderpath)


@click.command()
@click.option('--globalplaceholders', '-g', help='json file that contains the key value tuples to fill in placeholders '
                                                 'like "!@examiner@!" in the instructions file. Default is:'
                                                 ' "./global_placeholders.json"',
              default='./global_placeholders.json')
@click.option('--examiner', '-e', default='not provided',
              help='The name or abbreviation of the examiner running the script.')
@click.option('--loglevel', '-l', default='INFO',
              help='Controls which log messages will be written to stdout. Default is "INFO". Other allowed values are:'
                   ' CRITICAL, ERROR, WARNING, DEBUG.')
@click.option('--instructionsfile', '-i', help='The XML instructions file which tells mosk what to collect.')
def main(globalplaceholders: str, instructionsfile: str, examiner: str, loglevel: str):
    #argv = sys.argv[1:]

    #try:
    #    opts, args = getopt.getopt(argv, 'i:l:e:g:', ['instructions=', 'loglevel=', 'examiner=', 'globalplaceholders='])
    #except getopt.GetoptError:
    #    print("mosk.py -i <instructionsfile> -l [CRITICAL]")
    #    sys.exit(2)

    #for opt, arg in opts:
    #    if opt in ('-i', '--instructions'):
    #        instructionsfile = arg
    #    elif opt in ('-l', '--loglevel'):
    #        if arg.upper() in LOG_LEVEL.keys():
    #            logging.basicConfig(level=LOG_LEVEL[arg.upper()], format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')
    #        else:
    #            raise KeyError("'{}' not a valid log level.".format(arg))
    #    elif opt in ('-e', '--examiner'):
     #       examiner = arg
        #elif opt in ('-g', '--globalplaceholders'):
        #    if is_globalplaceholder_valid(arg):
        #        globalplaceholders = arg
        #    else:
        #        print(f"Globale placeholder file '{arg}' does not exist.")
        #        sys.exit(2)

    if loglevel.upper() in LOG_LEVEL.keys():
        logging.basicConfig(level=LOG_LEVEL[loglevel.upper()],
                            format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')
    else:
        raise KeyError("'{}' not a valid log level.".format(loglevel))

    if not is_globalplaceholder_valid(globalplaceholders):
        print(f"Globale placeholder file '{globalplaceholders}' does not exist.")
        sys.exit(2)

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
        print(f"Could not initialize parser. Instructions file '{instructionsfile}' does not exist.")
        sys.exit(2)


if __name__ == '__main__':
    main()