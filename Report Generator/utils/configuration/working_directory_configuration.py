import os

from config_parser import ConfigParser
from utils.configuration.default_configuration import DefaultConfiguration
from utils.folder.folder_utils import FolderUtils


class WorkingDirectoryConfiguration:
    """
    Working directory configuration
    """

    def __init__(self):
        """
        Initialize with command line config and default config
        """
        self.config_parser = ConfigParser()
        self.default_config = DefaultConfiguration()

    def get_workdir(self) -> str:
        """
        Current Working directory
        :return:
        """
        default_val = self.default_config.get_value("default", "workdir")
        return self.config_parser.get_argument("WORKDIR", default_val)

    def verify(self) -> None:
        """
        Verify the validity of the path provided, and throw an error is it's not able to create it
        :return: None
        """
        path = self.get_workdir()
        FolderUtils.merge_folder(path)

        if not os.path.exists(path):
            raise PermissionError("Failed to create the working directory at {0}.".format(path))
