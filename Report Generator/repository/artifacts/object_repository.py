from typing import List

from neo4j.graph import Node

from enums.artifact_type import ArtifactType
from repository.AbstractRepository import AbstractRepository


class ObjectRepository(AbstractRepository):
    """
    Object Repository
    """

    def __init__(self, application: str):
        """
        Init  Object Service
        :param application:  Name of the application
        """
        super(ObjectRepository, self).__init__(application)
        self.__type = ArtifactType.OBJECT

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

    def get_inner_essential_complexity(self, node: Node) -> float:
        """
        Get the line of code number
        :param node: Node to query
        :return: The line of code number
        """
        res = self.query_service.execute_query("object", "get_inner_complexity", anchors={
            "APPLICATION": self.get_application()
        }, params={
            "id": node.id,
            "complexity": "Essential Complexity"
        })

        return res[0] if len(res) >= 1 else 0

    def get_callees_by_type(self, node: Node, object_type: str) -> List[Node]:
        """
        Get the line of code number
        :param object_type: Type of the callee
        :param node: Node to query
        :return: The line of code number
        """
        res = self.query_service.execute_query("object", "get_callees_by_type", anchors={
            "APPLICATION": self.get_application()
        }, params={
            "id": node.id,
            "type": object_type
        })

        return res

    def get_object_by_type(self, object_type: str) -> List[Node]:
        """
        Get object by tyype
        :param object_type: Type of the object
        :return:
        """
        res = self.query_service.execute_query("object", "get_by_type", anchors={
            "APPLICATION": self.get_application()
        }, params={
            "type": object_type
        })

        return res if len(res) >= 1 else []
