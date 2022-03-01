import logging
import os
from logging.handlers import RotatingFileHandler

from metaclass.SingletonMeta import SingletonMeta
from utils.configuration.default_configuration import DefaultConfiguration


class Logger(metaclass=SingletonMeta):

    def __init__(self):
        """
        Initialize logging and display information
        :return: None
        """
        configuration = DefaultConfiguration()
        log_folder = str(configuration.get_value("logging", "log_folder"))
        log_level = str(configuration.get_value("logging", "log_level"))

        log_path = os.path.join(log_folder)
        os.chmod(log_path, 0o777)

        # Print log files and level
        message = "Logs will be saved to {0}. Log level is: {1}".format(log_folder, log_level)
        logging.debug(message)

        timestamp = ""

        # define logs files and folders
        info_file = "Net_to_Net_Core" + timestamp + ".log"
        self.__log_file = os.path.join(log_folder, info_file)

        error_file = "Net_to_Net_Core_error" + timestamp + ".log"
        self.__error_file = os.path.join(log_folder, error_file)

        self.__log_handler = RotatingFileHandler(info_file, maxBytes=1048576, backupCount=5)
        self.__log_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s ' '[in %(pathname)s:%(lineno)d]'))

    def get(self, name) -> logging.Logger:
        """
        Get a logger with a prefixed name
        :param name:  Name of the logger
        :return: The logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.__log_handler)
        return logger

    @staticmethod
    def get_logger(name):
        logger = Logger()
        return logger.get(name)
