import logging


LOG_LEVEL = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}
selected_loglevel = "WARNING"


def setup_logging(logger, loglevel=selected_loglevel):
    global LOG_LEVEL
    if loglevel in LOG_LEVEL.keys():
        logger.setLevel(LOG_LEVEL[loglevel])
        # Prevent the root logger from propagating from here on.
        # We use our own console logger from this point on.
        logger.propagate = False

        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(LOG_LEVEL[loglevel])

        formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
        consolehandler.setFormatter(formatter)

        logger.addHandler(consolehandler)
        logger.debug('Logging has been initialized.')
