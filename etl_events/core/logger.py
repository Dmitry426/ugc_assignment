import logging


def get_logger(name):
    formatter = logging.Formatter(
        fmt=f"%(asctime)s - [%(levelname)s] - %(name)s - "
            f"(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
