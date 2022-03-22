import logging

class LoggingFactory:
    logger = logging.getLogger("polyhymnia")
    logger.setLevel(logging.WARNING)
    logger.propagate = False
    if (logger.hasHandlers()):
        logger.handlers.clear()
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[Polyhnmnia] %(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)

    @classmethod
    def set_verbose(cls, verbose=True):
        logging.basicConfig()
        cls.logger.setLevel(logging.DEBUG if verbose else logging.WARNING)

    @classmethod
    def set_level(cls, level):
        cls.logger.setLevel(level)