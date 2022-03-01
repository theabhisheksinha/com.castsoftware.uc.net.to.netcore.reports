from typing import List

from neo4j.graph import Node

from enums.artifact_type import ArtifactType
from repository.AbstractRepository import AbstractRepository


class RawRepository(AbstractRepository):
    """
    Object Repository
    """

    def __init__(self, application: str):
        """
        Init  Object Service
        :param application:  Name of the application
        """
        super(RawRepository, self).__init__(application)
        self.__type = ArtifactType.RAW

    def get_transaction_in(self, node: Node) -> float:
        """
        Get the number of transaction
        :param node: Node to query
        :return: The line of code number
        """
        res = self.query_service.execute_query("raw", "get_transaction_number", anchors={
            "APPLICATION": self.get_application()
        }, params={
            "id": node.id
        })

        return res[0] if len(res) >= 1 else 0

    def get_sub_object_caller_by_type(self, node: Node) -> List[Node]:
        """
        Get calling object
        :param node: Node to query
        :return:
        """
        res = self.query_service.execute_query("raw", "get_sub_object_caller_by_type", anchors={
            "APPLICATION": self.get_application()
        }, params={
            "id": node.id
        })

        return res if len(res) >= 1 else []

    def get_parent(self, node: Node) -> Node or None:
        """
        Get the parent node of an artifact
        :param node: Node to get
        :return: Number of Artifact of the same type calling the element
        """
        # Get the query to link an net object
        query = self.query_service.get_query("raw", "get_parent")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id
        }

        # Execute
        res = self._neo4j_al.execute(query, parameters)
        return res[0] if len(res) >= 1 else None

    def get_property_value(self, node: Node, property_name: str, default: any) -> Node or None:
        """
        Get the parent node of an artifact
        :param default:
        :param property_name:
        :param node: Node to get
        :return: Number of Artifact of the same type calling the element
        """
        # Get the query to link an net object
        query = self.query_service.get_query("artifacts", "get_property")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id,
            "property": property_name
        }

        # Execute
        res = self._neo4j_al.execute(query, parameters)
        return res[0] if len(res) >= 1 else default

    def get_property_under(self, node: Node, property_name: str) -> []:
        """
        Get the list of value for the properties under the specified node
        :param property_name: Name of the property to get
        :param node: Node to get
        :return: List of value found for the properties
        """
        # Get the query to link an net object
        query = self.query_service.get_query("raw", "get_properties_under_raw")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id,
            "prop_value": property_name
        }

        # Execute
        debug = query.get_query().replace("$id", str(node.id)).replace("prop_value", "\"" + str(property_name) + "\"")
        res = self._neo4j_al.execute(query, parameters)
        ret_val = list(res[0]) if len(res) >= 1 and len(res[0]) >= 1 else []
        return ret_val