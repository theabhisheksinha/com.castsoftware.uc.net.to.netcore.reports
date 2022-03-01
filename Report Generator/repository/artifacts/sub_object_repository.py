from neo4j.graph import Node

from enums.artifact_type import ArtifactType
from repository.AbstractRepository import AbstractRepository


class SubObjectRepository(AbstractRepository):

    def __init__(self, application: str):
        """
        Init Sub Object Service
        :param application:  Name of the application
        """
        super(SubObjectRepository, self).__init__(application)
        self.__type = ArtifactType.SUB_OBJECT

    def get_loc(self, node: Node) -> int:
        """
        Get the line of code number
        :param node: Node to query
        :return: The line of code number
        """
        res = self.query_service.execute_query("properties", "get_loc_value", anchors={
            "APPLICATION": self.get_application()
        }, params={
            "id": node.id
        })

        return res[0] if len(res) >= 1 else 0

    def get_essential_complexity(self, node: Node) -> float:
        """
        Get the essential complexity of a subobject
        :param node: Node to query
        :return: The essential complexity of the
        """
        res = self.query_service.execute_query("properties", "get_essential_complexity", anchors={
            "APPLICATION": self.get_application()
        }, params={
            "id": node.id
        })

        return res[0] if len(res) >= 1 else 0