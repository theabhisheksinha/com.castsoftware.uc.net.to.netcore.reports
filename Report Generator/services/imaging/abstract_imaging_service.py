from abc import ABC

from db.neo4j.neo4j_al import Neo4jAl
from utils.configuration.neo4j_connection_info import Neo4jConnectionConfiguration
from utils.configuration.working_directory_configuration import WorkingDirectoryConfiguration


class AbstractImagingService(ABC):

    def __init__(self):
        """
        Declare common variables for all services
        """
        self._neo4j_al = Neo4jAl()

        self._working_dir_conf = WorkingDirectoryConfiguration()
        self._neo4j_conf = Neo4jConnectionConfiguration()

    def get_working_dir(self):
        """
        Get the current workingg directory
        :return: The working directory
        """
        return self._working_dir_conf.get_workdir()

    def get_application_name(self):
        """
        Get the name of the application in the scope
        :return:  The application name
        """
        return self._neo4j_conf.get_application()
