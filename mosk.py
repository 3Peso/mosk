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
    if loglevel.upper() in LOG_LEVEL.keys():
        logging.basicConfig(level=LOG_LEVEL[loglevel.upper()],
                            format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')
    else:
        raise KeyError("'{}' not a valid log level.".format(loglevel))

    if globalplaceholders is None or not os.path.exists(globalplaceholders):
        print(f"Globale placeholder file does not exist. Value of parameter 'globalplaceholders': {globalplaceholders}")
        sys.exit(2)

    if instructionsfile is None or not os.path.exists(instructionsfile):
        print(f"Instructions file does not exist. Value of parameter 'instructionsfile': {instructionsfile}")
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