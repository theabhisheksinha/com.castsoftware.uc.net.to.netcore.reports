import os

from definitions import ROOT_DIR
from logger import Logger
from utils.configuration.yml_configuration import YMLConfiguration


class CostConfiguration(YMLConfiguration):
    """
    Loads the query from the configuration file
    """

    def get_configuration_folder(self) -> str:
        """
        Get the configuration folder
        :return:
        """
        return os.path.join(ROOT_DIR, 'configuration/time_estimation/')

    def __init__(self):
        super().__init__()
        self.__logger = Logger.get_logger("Cost Configuration")
