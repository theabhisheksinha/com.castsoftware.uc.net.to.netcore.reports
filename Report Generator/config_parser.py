import argparse
import logging

from metaclass.SingletonMeta import SingletonMeta


class ConfigParser(metaclass=SingletonMeta):
    """
        Parse the configuration from command line and return it
    """

    def parse_arguments(self):
        """
        Parse arguments from command line
        :return: The list of argument passed
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('--APPLICATION', dest='APPLICATION',
                            help="Name of the application to process in CAST IMAGING", required=False)
        parser.add_argument('--WORKDIR', dest='WORKDIR', help="Working directory where the files will be created",
                            required=False)
        parser.add_argument('--URL', dest='URL', help="Neo4j URL", required=False)
        parser.add_argument('--PORT', dest='PORT', help="Neo4j Bolt Port", required=False)
        parser.add_argument('--USER', dest='USER', help="Neo4j instance user", required=False)
        parser.add_argument('--PASSWORD', dest='PASSWORD', help="Neo4j instance password", required=False)
        parser.add_argument('--ENCRYPTION', dest='ENCRYPTION', help="Use SSL to connect to neo4j (True or False)",
                            required=False)

        return parser.parse_args()

    def load_arguments(self) -> None:
        """
        Process Argument of the commandline and populate definitions.py
        :return: Configuration discovered
        """
        self.__configuration = self.parse_arguments()  # Parse arguments

    def is_loaded(self):
        """
        Check if the configuration has been done
        :return: Is loaded
        """
        return self.__configuration is None

    def get_argument(self, arg_name: str, default="") -> str or None:
        """
        Get argument from the configuration file, return default value if specified, or None
        :param default: Default value to return if nothing matched
        :param arg_name:  Name of the argument
        :return: The value or an error if the key doesn't exist
        """
        if self.__configuration is None:
            raise ValueError("Configuration has not been initialized.")

        if arg_name not in self.__configuration:
            logging.warning("'{0}' key doesn't exist in the configuration.".format(arg_name))
            return default if default != "" else None

        ret_val = vars(self.__configuration).get(arg_name)
        return str(ret_val) if ret_val is not None else default

    def __init__(self, lazy_load=False):
        super(ConfigParser, self).__init__()
        self.__configuration = argparse.Namespace()

        if not lazy_load:  # Load the args by default
            self.load_arguments()
