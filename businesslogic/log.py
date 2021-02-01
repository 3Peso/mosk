import logging


LOG_LEVEL = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}
MOSK_LOGGER_NAME: str = 'mosk'
# Here implicitely the handler of the parent is used,
# which is the StreamHandler for console logging
# Don't use the root logger. Setup your own logger
mosk_logger = logging.getLogger(MOSK_LOGGER_NAME)


def setup_logging(loglevel, logger=mosk_logger):
    global mosk_logger, LOG_LEVEL
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
    else:
        logging.error(f"Cannot set log level '{loglevel}'. Log level does not exist.", exc_info=True)
        mosk_logger = logging.getLogger('mosk_fallbacklogging')
