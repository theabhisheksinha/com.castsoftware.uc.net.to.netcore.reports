from config_parser import ConfigParser
from metaclass.SingletonMeta import SingletonMeta
from utils.configuration.default_configuration import DefaultConfiguration


class Neo4jConnectionConfiguration(metaclass=SingletonMeta):
    """
    Connection informations
    """

    def __init__(self):
        self.config_parser = ConfigParser()
        self.default_config = DefaultConfiguration()

    def get_host(self) -> str:
        """
        Imaging host server
        :return:
        """
        default_val = self.default_config.get_value("neo4j", "bolt_url")
        return self.config_parser.get_argument("URL", default_val)

    def get_url(self) -> str:
        """
        Get the BOLT URL
        :return:
        """
        bolt_url = self.default_config.get_value("neo4j", "bolt_url")
        try:
            url = self.config_parser.get_argument("URL", "localhost")
            port = self.config_parser.get_argument("PORT", "7687")

            if not (url is None or port is None):
                bolt_url = "bolt://{0}:{1}".format(url, port)

        except Exception as ignored:
            pass

        return bolt_url

    def get_user(self) -> str:
        """
            Get Imaging user
            :return:
        """
        default_val = self.default_config.get_value("neo4j", "username")
        return self.config_parser.get_argument("USER", default_val)

    def get_password(self) -> str:
        """
        Get Imaging neo4j password
        :return:
        """
        default_val = self.default_config.get_value("neo4j", "password")
        return self.config_parser.get_argument("PASSWORD", default_val)

    def get_encryption_level(self) -> bool:
        """
        Get neo4j encryption level
        :return:
        """
        default_val = self.default_config.get_value("neo4j", "encryption")
        ret = self.config_parser.get_argument("ENCRYPTION", default_val)
        return ret == 'True'

    def get_application(self) -> str:
        """
            Get the name of the imaging application
           :return:
        """
        default_val = self.default_config.get_value("default", "application")
        return self.config_parser.get_argument("APPLICATION", default_val)
