#!/usr/bin/env python3
import logging
import sys
import os

import click

from businesslogic.collector import Collector, get_logfilename_pattern


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
@click.option('--protocollogfile', '-p', help=f"Use this parameter to log out collection messages into your own log "
                                              f"file with your own custom path. If this is not set mosk will create a "
                                              f"protocol in the current working directory with format "
                                              f"'<Counter>_<Examiner>_<DateTime Stamp>.txt' "
                                              f"RegEx Pattern: {get_logfilename_pattern()}'."
                                              f"Example: '00001_amr_2021-09-11.txt'")
def mosk_main(globalplaceholders: str, instructionsfile: str, examiner: str, loglevel: str, protocollogfile: str):
    if loglevel.upper() in LOG_LEVEL.keys():
        logging.basicConfig(level=LOG_LEVEL[loglevel.upper()],
                            format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')
    else:
        print(f"'{loglevel}' not a valid log level.")
        return 2

    if globalplaceholders is None or not os.path.exists(globalplaceholders):
        print(f"Globale placeholder file does not exist. Value of parameter 'globalplaceholders': {globalplaceholders}")
        return 2

    if instructionsfile is None or not os.path.exists(instructionsfile):
        print(f"Instructions file does not exist. Value of parameter 'instructionsfile': {instructionsfile}")
        return 2

    logger = logging.getLogger(__name__)
    collector = Collector.get_collector(instructionsfile=instructionsfile, examiner=examiner,
                                        placeholderfile=globalplaceholders, protocollogfile=protocollogfile)
    collector.collect()
    logger.info("Collection complete.")

    return 0


if __name__ == '__main__':
    sys.exit(mosk_main())