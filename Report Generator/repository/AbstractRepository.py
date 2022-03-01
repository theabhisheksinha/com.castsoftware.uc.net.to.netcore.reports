from abc import ABC

from db.neo4j.neo4j_al import Neo4jAl
from utils.query_loader import QueryLoader


class AbstractRepository(ABC):
    """
    Abstract repository
    """

    def __init__(self, application: str):
        """
        Declare common variables for all services
        """
        self._neo4j_al = Neo4jAl()
        self.query_service = QueryLoader()

        self.__application = application

    def get_application(self) -> str:
        """
        Get the application name linked to the repositoru
        :return: Name of the application
        """
        return self.__application
