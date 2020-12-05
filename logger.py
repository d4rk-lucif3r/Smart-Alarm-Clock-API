"""This module is responsible for saving logs to the logs.log file."""

import logging
FILENAME = 'logs.log'
FORMAT = '%(levelname)s: %(asctime)s %(message)s'


def info_log(message: str) -> None:
    """
    Logs info such as an alarm going off, weather change , a new
    news story or a covid update.
    """
    logging.basicConfig(filename=FILENAME, level=logging.DEBUG,
                        format=FORMAT)
    logging.info(message)


def warning_log(message: str) -> None:
    """
    logs warnings such as attempting to load an empty json file or requests call
    getting failed.
    """
    logging.basicConfig(filename=FILENAME, level=logging.DEBUG,
                        format=FORMAT)
    logging.warning(message)


def error_log(message: str) -> None:
    """
    Logs known potential errors such as a RuntimeError while text to
    speech is in use.
    """
    logging.basicConfig(filename=FILENAME, level=logging.DEBUG,
                        format=FORMAT)
    logging.error(message)



