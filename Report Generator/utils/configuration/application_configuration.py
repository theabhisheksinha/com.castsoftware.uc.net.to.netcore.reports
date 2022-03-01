from config_parser import ConfigParser
from utils.configuration.default_configuration import DefaultConfiguration


class ApplicationConfiguration:
    """
    Application configuration
    """

    def __init__(self):
        """
        Initialize with command line config and default config
        """
        self.config_parser = ConfigParser()
        self.default_config = DefaultConfiguration()

    def get_application(self) -> str:
        """
        Current Working directory
        :return:
        """
        default_val = self.default_config.get_value("default", "application")
        return self.config_parser.get_argument("APPLICATION", default_val)
